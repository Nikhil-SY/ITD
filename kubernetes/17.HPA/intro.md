# Horizontal Pod Autoscaler (HPA) — Complete Guide

> **Who this is for:** Anyone learning Kubernetes — from complete beginners to engineers who want production-grade depth.
> This guide follows the **What → Why → How** structure throughout.

---

## Table of Contents

1. [The Big Picture — What Problem Does HPA Solve?](#1-the-big-picture)
2. [What Is HPA?](#2-what-is-hpa)
3. [How HPA Works Internally](#3-how-hpa-works-internally)
4. [Metrics HPA Can Use](#4-metrics-hpa-can-use)
5. [Your First HPA — CPU-Based Scaling](#5-your-first-hpa)
6. [Memory-Based Scaling](#6-memory-based-scaling)
7. [Custom Metrics Scaling](#7-custom-metrics-scaling)
8. [External Metrics Scaling](#8-external-metrics-scaling)
9. [Scaling Behavior — Stabilization & Policies](#9-scaling-behavior)
10. [Scale-to-Zero and KEDA](#10-scale-to-zero-and-keda)
11. [HPA vs VPA vs Cluster Autoscaler](#11-hpa-vs-vpa-vs-cluster-autoscaler)
12. [Resource Requests — The Non-Negotiable Prerequisite](#12-resource-requests)
13. [Cooldown Periods and the Stabilization Window](#13-cooldown-periods)
14. [Common Pitfalls and How to Avoid Them](#14-common-pitfalls)
15. [Observability — Monitoring Your HPA](#15-observability)
16. [Production Checklist](#16-production-checklist)
17. [Complete Real-World Example](#17-complete-real-world-example)

---

## 1. The Big Picture

### The Problem — Why Do We Need Autoscaling?

Imagine you run an e-commerce website. Traffic looks like this throughout the day:

```
Requests/sec

500 |                        ████
400 |                      ████████
300 |                    ████████████
200 |              ██  ████████████████  ██
100 | ████████████████████████████████████████████
  0 +-------------------------------------------> Time
     12am  4am  8am  12pm  4pm  8pm  10pm  12am
```

**Without autoscaling**, you have two bad choices:

| Option | Problem |
|--------|---------|
| Provision for **peak** (500 req/s) | You run 10 pods 24/7 — wasteful and expensive. At 4am you need maybe 2 pods |
| Provision for **average** (200 req/s) | At peak you're overwhelmed — slow responses, timeouts, angry users |

**With autoscaling**, Kubernetes watches your actual load and adjusts pod count automatically:
- 4 AM → 2 pods
- 12 PM sale event → 10 pods
- 11 PM → back to 2 pods

This is exactly what HPA does.

---

## 2. What Is HPA?

**HPA (Horizontal Pod Autoscaler)** is a Kubernetes controller that automatically increases or decreases the number of **pod replicas** in a Deployment, ReplicaSet, or StatefulSet based on observed metrics.

### Horizontal vs Vertical — What's the Difference?

```
HORIZONTAL SCALING (HPA)          VERTICAL SCALING (VPA)
────────────────────────          ──────────────────────
Add/remove pods                   Make existing pods bigger/smaller

  [Pod] [Pod]                        [  Pod  ]
       ↓ scale out                        ↓ scale up
  [Pod] [Pod] [Pod]                 [    Pod    ]

More instances of same size        Same instance with more resources
```

Think of a restaurant:
- **Horizontal**: Open more checkout counters (more cashiers)
- **Vertical**: Replace a cashier with a faster, stronger one

HPA is almost always preferred for stateless web applications because adding more identical pods is fast, safe, and doesn't require downtime.

### What HPA Can Scale

HPA works with any resource that has a `scale` subresource:

- `Deployment` ✅ (most common)
- `ReplicaSet` ✅
- `StatefulSet` ✅
- `ReplicationController` ✅ (legacy)
- Custom resources that implement scale subresource ✅

---

## 3. How HPA Works Internally

### The Control Loop

HPA is a **controller** — it runs a reconciliation loop every **15 seconds** (configurable) performing:

```
┌─────────────────────────────────────────────────────────┐
│                    HPA Control Loop                      │
│                                                         │
│  Every 15 seconds:                                      │
│                                                         │
│  1. OBSERVE  ──► Query metrics server for current usage │
│                                                         │
│  2. CALCULATE ─► Compute desired replica count          │
│                  using the scaling formula              │
│                                                         │
│  3. ACT ───────► Update Deployment's replicas field     │
│                  if needed (and within stabilization    │
│                  window)                                │
└─────────────────────────────────────────────────────────┘
```

### The Scaling Formula

This is the core algorithm HPA uses:

```
                    currentMetricValue
desiredReplicas = ⌈ currentReplicas × ──────────────────── ⌉
                    desiredMetricValue
```

`⌈ ⌉` means ceiling (round up).

**Example — Scaling Up:**
- Current replicas: `3`
- Current CPU usage: `90%`
- Target CPU usage: `50%`

```
desiredReplicas = ⌈ 3 × (90 / 50) ⌉
               = ⌈ 3 × 1.8 ⌉
               = ⌈ 5.4 ⌉
               = 6
```

HPA will scale from 3 → 6 pods.

**Example — Scaling Down:**
- Current replicas: `6`
- Current CPU usage: `20%`
- Target CPU usage: `50%`

```
desiredReplicas = ⌈ 6 × (20 / 50) ⌉
               = ⌈ 6 × 0.4 ⌉
               = ⌈ 2.4 ⌉
               = 3
```

HPA will scale from 6 → 3 pods (after the stabilization window).

### Multi-Metric Scaling

When multiple metrics are configured, HPA computes the desired replica count **for each metric independently** and takes the **maximum**:

```
CPU metric    → wants 6 replicas
Memory metric → wants 4 replicas
Custom metric → wants 8 replicas

Final decision: 8 replicas  ← always the maximum
```

This ensures no single metric is a bottleneck.

### The Metrics Pipeline

```
┌──────────────┐    ┌──────────────────┐    ┌─────────────┐
│  Your Pods   │───►│  cAdvisor        │───►│  Kubelet    │
│  (app code)  │    │  (on each node)  │    │  (on node)  │
└──────────────┘    └──────────────────┘    └──────┬──────┘
                                                   │
                                                   ▼
                                          ┌────────────────┐
                                          │ Metrics Server │
                                          │ (aggregates    │
                                          │  all nodes)    │
                                          └───────┬────────┘
                                                  │
                                                  ▼
                                          ┌────────────────┐
                                          │  HPA Controller│
                                          │  (reads every  │
                                          │   15 seconds)  │
                                          └───────┬────────┘
                                                  │
                                                  ▼
                                          ┌────────────────┐
                                          │   Deployment   │
                                          │  .spec.replicas│
                                          │  (gets updated)│
                                          └────────────────┘
```

**Metrics Server** must be installed in your cluster for CPU/Memory HPA to work. It is NOT installed by default in most clusters.

```bash
# Install metrics-server (required for CPU/Memory HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify it's working
kubectl top nodes
kubectl top pods
```

---

## 4. Metrics HPA Can Use

HPA supports four types of metrics:

```
┌─────────────────────────────────────────────────────────────────┐
│                     HPA Metric Types                            │
├──────────────────┬──────────────────────────────────────────────┤
│ Resource         │ CPU and Memory of pods (built-in)            │
│                  │ Source: metrics-server                        │
├──────────────────┼──────────────────────────────────────────────┤
│ ContainerResource│ CPU/Memory of a SPECIFIC container in a pod  │
│                  │ Useful for multi-container pods               │
├──────────────────┼──────────────────────────────────────────────┤
│ Pods             │ App-specific metric per pod                   │
│                  │ Example: requests-per-second per pod          │
│                  │ Source: custom metrics API                    │
├──────────────────┼──────────────────────────────────────────────┤
│ Object           │ Metric from a Kubernetes object               │
│                  │ Example: Ingress hits per second              │
│                  │ Source: custom metrics API                    │
├──────────────────┼──────────────────────────────────────────────┤
│ External         │ Metric from outside Kubernetes entirely       │
│                  │ Example: SQS queue depth, Kafka lag           │
│                  │ Source: external metrics API                  │
└──────────────────┴──────────────────────────────────────────────┘
```

### Metric Target Types

Each metric can have one of three target types:

| Target Type | Meaning | Example |
|-------------|---------|---------|
| `Utilization` | Percentage of the requested resource | 70% of CPU request |
| `AverageValue` | Average raw value across all pods | 500m CPU per pod |
| `Value` | Total value (not per-pod average) | Used for Object/External metrics |

---

## 5. Your First HPA — CPU-Based Scaling

### Step 1: Create a Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: default
spec:
  replicas: 2                      # Starting replica count
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "200m"            # ← CRITICAL: HPA REQUIRES this
            memory: "256Mi"        # Request = what pod needs at minimum
          limits:
            cpu: "500m"            # Limit = max it can use
            memory: "512Mi"
```

> **Why are `requests` mandatory?**
> HPA calculates CPU utilization as:
> `current_cpu_usage / cpu_request × 100%`
> Without a request, HPA has no denominator — it literally cannot compute a percentage.

### Step 2: Create the HPA (Declarative — Recommended)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2                # Use v2, not v1
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: default
spec:
  # ── Target: what to scale ─────────────────────────────────────
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app                         # Must match Deployment name exactly

  # ── Boundaries: safety rails ──────────────────────────────────
  minReplicas: 2                          # Never go below this
  maxReplicas: 10                         # Never exceed this

  # ── Metrics: when to scale ────────────────────────────────────
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70            # Scale when avg CPU > 70%
```

```bash
# Apply both
kubectl apply -f deployment.yaml
kubectl apply -f hpa.yaml

# Check HPA status
kubectl get hpa web-app-hpa

# Detailed view
kubectl describe hpa web-app-hpa
```

### Step 3: Observe HPA in Action

```bash
# Watch HPA in real time
kubectl get hpa web-app-hpa --watch

# Output columns explained:
# NAME          REFERENCE        TARGETS         MINPODS  MAXPODS  REPLICAS
# web-app-hpa   Deployment/...   <unknown>/70%   2        10       2

# <unknown> means metrics-server hasn't sent data yet
# Wait ~30 seconds, it should show actual values:
# web-app-hpa   Deployment/...   45%/70%         2        10       2
#                                 ↑
#                           current usage / target
```

### Step 4: Generate Load and Watch Scaling

```bash
# Open a second terminal and run a load generator
kubectl run load-gen --image=busybox --restart=Never -- \
  /bin/sh -c "while true; do wget -q -O- http://web-app; done"

# In first terminal, watch HPA respond
kubectl get hpa web-app-hpa --watch
# You'll see REPLICAS climb: 2 → 4 → 6 → ...
```

### The Imperative Way (Quick Testing Only)

```bash
# Quick HPA creation without YAML (not recommended for production)
kubectl autoscale deployment web-app \
  --min=2 \
  --max=10 \
  --cpu-percent=70
```

---

## 6. Memory-Based Scaling

Memory scaling is trickier than CPU because memory doesn't "release" the way CPU does — a pod that used 500Mi might still show 500Mi even after the load drops (due to caching, GC patterns, etc.).

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa-memory
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 400Mi         # Scale when avg pod memory > 400Mi
                                    # (not Utilization % — raw value works
                                    #  better for memory)
```

> **Why `AverageValue` instead of `Utilization` for memory?**
> Memory utilization % = `current / request × 100`.
> If your request is only 256Mi but pods actually need 400Mi, you'll hit 156% quickly.
> Using `AverageValue` (e.g., 400Mi) is more predictable and maps to actual
> observed behavior rather than an artificial request baseline.

---

## 7. Custom Metrics Scaling

Custom metrics let you scale on **application-level signals** — requests per second, queue depth, active connections, etc.

### Architecture for Custom Metrics

```
┌──────────────┐    ┌──────────────┐    ┌───────────────────────┐
│  Your App    │───►│  Prometheus  │───►│  Prometheus Adapter   │
│  /metrics    │    │  (scrapes)   │    │  (translates to       │
│  endpoint    │    │              │    │   custom metrics API) │
└──────────────┘    └──────────────┘    └──────────┬────────────┘
                                                   │
                                                   ▼
                                        ┌──────────────────┐
                                        │   HPA Controller │
                                        │   (queries       │
                                        │   custom API)    │
                                        └──────────────────┘
```

### Example: Scale on HTTP Requests Per Second

Assuming your app exposes `http_requests_total` to Prometheus and you have prometheus-adapter installed:

```yaml
# prometheus-adapter ConfigMap (simplified)
# This tells the adapter how to translate a Prometheus query
# into a Kubernetes custom metric

rules:
- seriesQuery: 'http_requests_total{namespace!="",pod!=""}'
  resources:
    overrides:
      namespace: {resource: "namespace"}
      pod: {resource: "pod"}
  name:
    matches: "http_requests_total"
    as: "http_requests_per_second"     # The metric name HPA will use
  metricsQuery: 'rate(http_requests_total[2m])'
```

```yaml
# hpa-custom.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa-rps
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Pods                          # Pods = per-pod average metric
    pods:
      metric:
        name: http_requests_per_second  # Must match name in adapter config
      target:
        type: AverageValue
        averageValue: "100"             # Scale when avg > 100 req/s per pod
```

**How the formula works here:**
- 3 pods, each handling 250 req/s → average = 250 req/s per pod
- Target = 100 req/s per pod
- `desiredReplicas = ⌈ 3 × (250/100) ⌉ = ⌈ 7.5 ⌉ = 8`
- HPA scales to 8 pods

### Object Metrics — Scale on Ingress Load

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa-ingress
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Object                        # Object = metric from a K8s object
    object:
      metric:
        name: requests-per-second
      describedObject:
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        name: web-app-ingress           # The Ingress object to read metric from
      target:
        type: Value                     # Total value, not per-pod average
        value: "1000"                   # Scale when ingress hits > 1000 req/s total
```

---

## 8. External Metrics Scaling

External metrics come from systems **outside** Kubernetes — like AWS SQS, GCP Pub/Sub, Kafka, RabbitMQ.

### Architecture

```
   AWS SQS Queue                Kubernetes
   ────────────           ─────────────────────────
   ┌──────────┐           ┌─────────────────────┐
   │ Messages │           │  External Metrics   │
   │ in queue │──────────►│  Adapter            │
   │  (5000)  │           │  (e.g., KEDA or    │
   └──────────┘           │   custom adapter)   │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   HPA Controller    │
                          │   queries external  │
                          │   metrics API       │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   Worker Deployment │
                          │   (scales based on  │
                          │    queue depth)     │
                          └─────────────────────┘
```

### Example: Scale Workers Based on SQS Queue Depth

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: message-worker
  minReplicas: 1
  maxReplicas: 50
  metrics:
  - type: External                      # External = metric from outside K8s
    external:
      metric:
        name: sqs_messages_visible      # Name exposed by external metrics adapter
        selector:
          matchLabels:
            queue: "order-processing"   # Which queue
      target:
        type: AverageValue
        averageValue: "30"              # Each worker should handle ~30 messages
```

**Meaning:** If there are 300 messages in the queue:
- `desiredReplicas = ⌈ 300 / 30 ⌉ = 10 workers`

> **Note:** For external metrics, KEDA (Kubernetes Event-Driven Autoscaling) is often
> a better solution. See [Section 10](#10-scale-to-zero-and-keda).

---

## 9. Scaling Behavior

By default HPA scales conservatively to avoid flapping (rapidly scaling up and down). The `behavior` field gives you fine-grained control.

### Default Behavior

| Direction | Default |
|-----------|---------|
| Scale Up | Can add unlimited pods, but waits 0s stabilization window |
| Scale Down | Waits **5 minutes** (300s) stabilization window before shrinking |

The 5-minute scale-down delay is intentional — it prevents a sudden traffic drop from prematurely killing pods while more requests are still arriving.

### Customizing Behavior

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa-behavior
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

  # ─── Scaling Behavior ───────────────────────────────────────────
  behavior:

    scaleUp:
      stabilizationWindowSeconds: 30    # Wait 30s before scaling up again
                                        # (prevents rapid over-scaling)
      policies:
      - type: Pods                      # Policy 1: Add at most 4 pods at once
        value: 4
        periodSeconds: 60
      - type: Percent                   # Policy 2: Add at most 100% of current count
        value: 100                      #           (doubles the deployment)
        periodSeconds: 60
      selectPolicy: Max                 # Use whichever policy allows MORE pods
                                        # Options: Max (default), Min, Disabled

    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scaling down (default)
      policies:
      - type: Pods                      # Remove at most 2 pods per minute
        value: 2
        periodSeconds: 60
      - type: Percent                   # Or remove at most 10% per minute
        value: 10
        periodSeconds: 60
      selectPolicy: Min                 # Use whichever policy allows FEWER removals
                                        # (more conservative = more stable)
```

### Understanding selectPolicy

```
selectPolicy: Max  →  picks the policy that results in MORE replicas
                      (aggressive scale-up / slow scale-down)

selectPolicy: Min  →  picks the policy that results in FEWER replicas
                      (slow scale-up / aggressive scale-down)

selectPolicy: Disabled  →  disables scaling in this direction entirely
```

### Stabilization Window Explained

The stabilization window is a **lookback window**. HPA looks at all desired replica counts calculated over the window and picks:
- **Scale Up**: The **minimum** recommended count in the window (conservative)
- **Scale Down**: The **maximum** recommended count in the window (conservative)

```
Time:          t=0   t=1m  t=2m  t=3m  t=4m  t=5m
Calculated:     8     6     7     5     4     3
                                                 ↑
                                           current time

Scale-Down window = 5 min
Max in window = 8
→ HPA keeps 8 replicas (won't scale down yet)
```

This prevents thrashing when load fluctuates.

---

## 10. Scale-to-Zero and KEDA

### The Limitation of Native HPA

Native HPA cannot scale to **zero** replicas. `minReplicas` must be at least 1. This is a problem for:
- Batch workloads that only run occasionally
- Dev/staging environments that should sleep when idle
- Event-driven workers that only need to run when events arrive

### KEDA — Kubernetes Event-Driven Autoscaling

**KEDA** is an open-source project (CNCF) that extends Kubernetes with:
- Scale-to-zero capability (0 replicas when idle)
- Native integration with 60+ event sources (Kafka, RabbitMQ, SQS, Azure Service Bus, etc.)
- Works alongside HPA (KEDA creates/manages an HPA under the hood)

```
Without KEDA:   minReplicas: 1  →  Always 1 pod running
With KEDA:      minReplicas: 0  →  0 pods when no events, scales up on demand
```

### KEDA ScaledObject Example

```yaml
# Install KEDA first:
# kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.13.0/keda-2.13.0.yaml

apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: kafka-consumer-scaler
spec:
  scaleTargetRef:
    name: kafka-consumer             # Deployment to scale
  minReplicaCount: 0                 # ← Can go to zero!
  maxReplicaCount: 30
  pollingInterval: 15                # Check every 15 seconds
  cooldownPeriod: 300                # Wait 5 min before scaling to zero

  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka:9092
      consumerGroup: my-consumer-group
      topic: orders
      lagThreshold: "50"             # 1 replica per 50 messages of lag
```

---

## 11. HPA vs VPA vs Cluster Autoscaler

These three autoscalers work at different levels and complement each other.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Three Layers of Autoscaling                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Cluster Autoscaler                            │   │
│  │   Adds/removes NODES (VMs) from the cluster            │   │
│  │   Triggers: Pods are Pending (not enough node space)   │   │
│  └─────────────────────────────────────────────────────────┘   │
│         ↑ If HPA adds pods but no room on nodes                │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────────────────────┐  │
│  │       HPA        │    │             VPA                  │  │
│  │  Scales Pods     │    │  Scales Pod SIZE                 │  │
│  │  horizontally    │    │  (adjusts requests/limits)       │  │
│  │  (add/remove)    │    │  vertically                      │  │
│  └──────────────────┘    └──────────────────────────────────┘  │
│         ↑ Works on pods                ↑ Works on pods         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Your Pods                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Comparison Table

| Feature | HPA | VPA | Cluster Autoscaler |
|---------|-----|-----|-------------------|
| What it scales | Number of pods | Pod CPU/Memory requests | Number of nodes |
| Scaling direction | Horizontal (more copies) | Vertical (bigger pod) | Infrastructure level |
| Downtime required? | No | Yes (restarts pods) | No |
| Good for | Stateless apps, web servers | Stateful apps, ML training | When pods can't fit on nodes |
| Can scale to zero? | No (min 1, unless KEDA) | No | Removes empty nodes |
| Latency of scaling | Seconds to minutes | Minutes (requires restart) | Minutes to tens of minutes |

### Can HPA and VPA Run Together?

**Generally no** — not on the same metric. If both target CPU:
- HPA says "add more pods to reduce CPU per pod"
- VPA says "give each pod more CPU"
- They fight each other → chaos

**The workaround:** Use VPA in recommendation-only mode (`updateMode: "Off"`) to get sizing suggestions, apply them manually, then let HPA handle replica count.

---

## 12. Resource Requests — The Non-Negotiable Prerequisite

This is the most common reason HPA doesn't work.

### What Happens Without Requests

```bash
kubectl describe hpa web-app-hpa

# You'll see:
# Events:
#   Warning  FailedGetScale  unable to get metrics for resource cpu:
#            unable to get metrics; no metrics returned from resource
#            metrics API
```

### Setting Proper Requests

```yaml
containers:
- name: app
  resources:
    requests:
      cpu: "200m"       # 200 millicores = 0.2 CPU cores
      memory: "256Mi"
    limits:
      cpu: "1000m"      # 1 full CPU core
      memory: "512Mi"
```

### How to Choose the Right Request Value

1. Run your app without resource limits
2. Observe actual usage under normal load: `kubectl top pods`
3. Set requests to ~70% of the observed average
4. Set limits to ~150-200% of requests (room to burst)

```bash
# Example output:
kubectl top pods

NAME              CPU(cores)   MEMORY(bytes)
web-app-7d9f8-x   180m         210Mi
web-app-7d9f8-y   195m         220Mi
web-app-7d9f8-z   170m         195Mi

# Average CPU ≈ 182m → set request: 200m, limit: 500m
# Average Mem ≈ 208Mi → set request: 256Mi, limit: 512Mi
```

---

## 13. Cooldown Periods

### Why Cooldown Exists

Without cooldown, HPA would react to every tiny metric fluctuation:

```
Without cooldown (bad):
Metric:   80%  20%  80%  20%  80%  20%
Replicas:  6    2    6    2    6    2    ← constant churn

With cooldown (good):
Metric:   80%  20%  80%  20%  80%  20%
Replicas:  6    6    6    6    4    4    ← stable, scales down slowly
```

### Scale-Up Cooldown (stabilizationWindowSeconds for scaleUp)

Default: 0 seconds (scale up immediately when needed). This is aggressive but intentional — you don't want to wait when traffic is hitting your app.

Recommended for production: 30–60 seconds (prevents over-provisioning during transient spikes).

### Scale-Down Cooldown (stabilizationWindowSeconds for scaleDown)

Default: 300 seconds (5 minutes). This is conservative and safe for most apps.

```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 180   # Override to 3 min for faster scale-down
```

---

## 14. Common Pitfalls and How to Avoid Them

### Pitfall 1: Missing Metrics Server

**Symptom:** `TARGETS: <unknown>/70%`

```bash
# Fix: install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify
kubectl get deployment metrics-server -n kube-system
kubectl top pods
```

### Pitfall 2: No Resource Requests on Pods

**Symptom:** HPA shows `FailedGetScale` error

```bash
# Check if requests are set
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].resources}'

# Fix: add requests to your Deployment spec
```

### Pitfall 3: HPA and Manual Replica Edits

If you manually `kubectl scale deployment web-app --replicas=5` while HPA is active, HPA will **override your change** within 15 seconds. Don't mix manual scaling with HPA.

### Pitfall 4: Min and Max Set to Same Value

```yaml
minReplicas: 5
maxReplicas: 5   # ← HPA is effectively disabled; always 5 replicas
```

This is technically valid but defeats the purpose of HPA.

### Pitfall 5: Target Too High or Too Low

| Target | Problem |
|--------|---------|
| `averageUtilization: 95%` | Almost no headroom — any spike overloads pods before HPA responds |
| `averageUtilization: 20%` | Always over-provisioned — wasteful and expensive |

**Recommended starting points:**
- CPU: 60–70%
- Memory: 70–80% (memory scales slower)
- RPS: 60–70% of pod's comfortable capacity

### Pitfall 6: Ignoring Pod Startup Time

If your app takes 60 seconds to start, HPA needs to account for this. Add readiness probes and consider pre-scaling before known traffic events:

```yaml
# In your Deployment
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30        # Give app time to start
  periodSeconds: 10
  failureThreshold: 3
```

### Pitfall 7: Using v1 HPA API

The `autoscaling/v1` API only supports CPU. Always use `autoscaling/v2` which supports all metric types.

```yaml
# ❌ Old — CPU only
apiVersion: autoscaling/v1

# ✅ New — all metrics
apiVersion: autoscaling/v2
```

---

## 15. Observability — Monitoring Your HPA

### Key kubectl Commands

```bash
# Quick status — shows current vs target and replica count
kubectl get hpa

# Detailed view — events, conditions, metric values
kubectl describe hpa web-app-hpa

# Watch live
kubectl get hpa web-app-hpa -w

# Get raw metrics HPA is seeing
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/namespaces/default/pods" | jq .

# Get custom metrics
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq .
```

### Reading `kubectl describe hpa` Output

```
Name:                                                  web-app-hpa
Namespace:                                             default
Reference:                                             Deployment/web-app
Metrics:                       ( current / target )
  resource cpu on pods         ( as a percentage of request ):
                               65% (130m) / 70%          ← currently at 65% (below target, stable)
Min replicas:                  2
Max replicas:                  10
Deployment pods:               4 current / 4 desired     ← 4 pods, stable
Conditions:
  Type            Status  Reason              Message
  ──────────────  ──────  ──────────────────  ───────────────────────────────────────
  AbleToScale     True    ReadyForNewScale    recommended size matches current size
  ScalingActive   True    ValidMetricFound    the HPA was able to successfully calculate
  ScalingLimited  False   DesiredWithinRange  the desired count is within the acceptable range
Events:
  Type    Reason             Age    Message
  ──────  ─────────────────  ─────  ─────────────────────────────────────────────────
  Normal  SuccessfulRescale  5m     New size: 4; reason: cpu resource utilization
                                    (percentage of request) above target
```

**Conditions to watch:**

| Condition | Meaning |
|-----------|---------|
| `AbleToScale: True` | HPA can successfully scale the target |
| `ScalingActive: True` | HPA found valid metrics and is working |
| `ScalingLimited: True` | HPA wants more/fewer replicas but is bounded by min/max |

### Prometheus Metrics for HPA

If you have Prometheus, HPA exposes these metrics:

```
kube_horizontalpodautoscaler_spec_min_replicas    # Configured min
kube_horizontalpodautoscaler_spec_max_replicas    # Configured max
kube_horizontalpodautoscaler_status_current_replicas  # Actual pods
kube_horizontalpodautoscaler_status_desired_replicas  # What HPA wants
kube_horizontalpodautoscaler_metadata_generation
```

---

## 16. Production Checklist

Before deploying HPA in production, verify:

```
□ metrics-server is installed and working (kubectl top pods works)
□ All containers have cpu and memory requests defined
□ Resource requests are based on observed real-world usage
□ minReplicas ≥ 2 (for availability — 1 is a single point of failure)
□ maxReplicas is set to a safe upper limit (not unlimited)
□ Target utilization has headroom (not 95%+)
□ Readiness probes are configured so HPA doesn't count unready pods
□ Pod Disruption Budgets (PDB) protect against too many pods being killed at once
□ Scaling behavior is tuned for your traffic pattern
□ HPA events are being monitored/alerted
□ Using autoscaling/v2 API, not v1
□ Tested scale-up and scale-down behavior with load testing
```

### Pod Disruption Budget (Works with HPA)

```yaml
# Ensure at least 2 pods are always running, even during scale-down or node drain
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app-pdb
spec:
  minAvailable: 2           # Always keep at least 2 pods up
  selector:
    matchLabels:
      app: web-app
```

---

## 17. Complete Real-World Example

A production-grade HPA setup for a web API that scales on both CPU and RPS:

```yaml
# ──────────────────────────────────────────────────────────────────
# Deployment — the app being scaled
# ──────────────────────────────────────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api
  namespace: production
  labels:
    app: payment-api
    version: "1.0"
spec:
  replicas: 3                          # Baseline; HPA will adjust this
  selector:
    matchLabels:
      app: payment-api
  template:
    metadata:
      labels:
        app: payment-api
    spec:
      containers:
      - name: payment-api
        image: myregistry/payment-api:1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "250m"                # Based on load testing observations
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        readinessProbe:
          httpGet:
            path: /healthz/ready
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 5
          failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /healthz/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
---
# ──────────────────────────────────────────────────────────────────
# HPA — the autoscaler
# ──────────────────────────────────────────────────────────────────
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-api

  minReplicas: 3                       # HA: 3 pods minimum across 3 AZs
  maxReplicas: 30                      # Cost ceiling; tune based on budget

  metrics:
  # Metric 1: CPU — keeps pods from being overwhelmed
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65         # Scale at 65% CPU (35% headroom for spikes)

  # Metric 2: Memory — for memory-sensitive workloads
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 768Mi            # ~75% of 1Gi request

  # Metric 3: RPS per pod (requires Prometheus + prometheus-adapter)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "150"            # Each pod handles up to 150 req/s

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 45  # Wait 45s before scaling up again
      policies:
      - type: Pods
        value: 5                       # Add at most 5 pods per minute
        periodSeconds: 60
      - type: Percent
        value: 50                      # Or add 50% of current count per minute
        periodSeconds: 60
      selectPolicy: Max                # Whichever adds more pods

    scaleDown:
      stabilizationWindowSeconds: 300 # Wait 5 min before scaling down
      policies:
      - type: Pods
        value: 3                       # Remove at most 3 pods per minute
        periodSeconds: 60
      - type: Percent
        value: 20                      # Or remove 20% per minute
        periodSeconds: 60
      selectPolicy: Min                # Whichever removes fewer pods (conservative)
---
# ──────────────────────────────────────────────────────────────────
# PodDisruptionBudget — protects availability during scale-down
# ──────────────────────────────────────────────────────────────────
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: payment-api-pdb
  namespace: production
spec:
  minAvailable: 3                      # Always keep 3 pods running
  selector:
    matchLabels:
      app: payment-api
```

### Verification Commands for This Setup

```bash
# Deploy everything
kubectl apply -f deployment.yaml
kubectl apply -f hpa.yaml
kubectl apply -f pdb.yaml

# Wait for pods to be ready
kubectl rollout status deployment/payment-api -n production

# Check HPA is picking up metrics (wait ~60s)
kubectl get hpa payment-api-hpa -n production

# Expected output when healthy:
# NAME               REFERENCE                  TARGETS                      MINPODS  MAXPODS  REPLICAS
# payment-api-hpa    Deployment/payment-api     65%/65%, 450Mi/768Mi         3        30       3

# Simulate load and verify scaling
kubectl run load --image=busybox -n production --restart=Never -- \
  /bin/sh -c "while true; do wget -q -O- http://payment-api:8080/; done"

# Watch HPA respond
kubectl get hpa payment-api-hpa -n production -w

# Check events
kubectl describe hpa payment-api-hpa -n production | grep -A 20 Events
```

---

## Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                     HPA at a Glance                             │
├─────────────────────────────────────────┬────────────────────────┤
│ What it is                              │ K8s controller that    │
│                                         │ auto-adjusts pod count │
├─────────────────────────────────────────┼────────────────────────┤
│ How often it checks                     │ Every 15 seconds       │
├─────────────────────────────────────────┼────────────────────────┤
│ Core formula                            │ ⌈ current × (now/target) ⌉ │
├─────────────────────────────────────────┼────────────────────────┤
│ Metric types                            │ CPU, Memory, Custom,   │
│                                         │ External               │
├─────────────────────────────────────────┼────────────────────────┤
│ Must-have prerequisite                  │ Resource requests set  │
│                                         │ on all containers      │
├─────────────────────────────────────────┼────────────────────────┤
│ Default scale-down wait                 │ 5 minutes              │
├─────────────────────────────────────────┼────────────────────────┤
│ Can scale to zero?                      │ No (use KEDA)          │
├─────────────────────────────────────────┼────────────────────────┤
│ API version to use                      │ autoscaling/v2         │
├─────────────────────────────────────────┼────────────────────────┤
│ Best for                                │ Stateless apps, APIs,  │
│                                         │ web servers            │
└─────────────────────────────────────────┴────────────────────────┘
```

---

*References:*
- *[Kubernetes HPA docs](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)*
- *[autoscaling/v2 API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/horizontal-pod-autoscaler-v2/)*
- *[KEDA project](https://keda.sh/)*
- *[metrics-server](https://github.com/kubernetes-sigs/metrics-server)*
- *[prometheus-adapter](https://github.com/kubernetes-sigs/prometheus-adapter)*