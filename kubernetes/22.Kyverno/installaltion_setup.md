# Kyverno — Complete Guide
### Policy Engine for Kubernetes | What · Why · How

---

## Table of Contents

1. [What is Kyverno?](#1-what-is-kyverno)
2. [Why Do We Need Kyverno?](#2-why-do-we-need-kyverno)
3. [How Kyverno Works — Architecture Deep Dive](#3-how-kyverno-works--architecture-deep-dive)
4. [Kyverno Policy Types](#4-kyverno-policy-types)
5. [Installation via Helm](#5-installation-via-helm)
6. [Writing Your First Policies](#6-writing-your-first-policies)
7. [Real-World Policy Examples](#7-real-world-policy-examples)
8. [Policy Reports](#8-policy-reports)
9. [Kyverno CLI for Testing](#9-kyverno-cli-for-testing)
10. [Best Practices](#10-best-practices)
11. [Kyverno vs. OPA Gatekeeper](#11-kyverno-vs-opa-gatekeeper)

---

## 1. What is Kyverno?

### The Simple Analogy

Think of Kubernetes as a **large apartment building**. Tenants (developers) can move in (deploy workloads) freely. Without rules, some tenants might:

- Leave their doors unlocked (run containers as root)
- Use too much electricity (no resource limits)
- Put up illegal signage (missing required labels)
- Sub-let without permission (use unapproved images)

**Kyverno is the building management system** — a set of rules enforced at the entrance that every tenant must comply with before moving in, and ongoing inspections that audit existing tenants.

### Technical Definition

**Kyverno** (Greek for "govern") is a **policy engine designed natively for Kubernetes**. It is a CNCF (Cloud Native Computing Foundation) graduated project that allows platform and security teams to:

| Capability | Description |
|---|---|
| **Validate** | Reject resources that don't meet rules |
| **Mutate** | Automatically modify resources to add/change fields |
| **Generate** | Auto-create additional resources when a resource is created |
| **Verify Images** | Ensure container images are signed and from trusted registries |
| **Cleanup** | Automatically delete stale resources based on rules |

Kyverno policies are written in **pure YAML** — there is no new language to learn (unlike OPA Gatekeeper which requires Rego).

---

## 2. Why Do We Need Kyverno?

### The Problem Without a Policy Engine

In a typical Kubernetes cluster, a developer can apply almost any manifest. Consider this perfectly valid but dangerous deployment:

```yaml
# A developer can deploy this without any restrictions
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
        - name: app
          image: nginx:latest          # ❌ Mutable 'latest' tag — unpredictable
          securityContext:
            runAsRoot: true            # ❌ Runs as root — security risk
          # ❌ No resource requests/limits — can starve other pods
          # ❌ No labels — cannot be monitored or tracked
```

This gets deployed successfully. Now multiply this by 50 developers and 200 services — chaos.

### What Goes Wrong Without Policies

```
┌─────────────────────────────────────────────────────────────┐
│                   Problems in Production                    │
├─────────────────────────────┬───────────────────────────────┤
│ Security Issues             │ Operational Issues            │
├─────────────────────────────┼───────────────────────────────┤
│ • Containers running as     │ • Pods evicted for lacking    │
│   root (privilege escalation│   resource limits             │
│   risk)                     │ • No labels = no monitoring   │
│ • Untrusted/unsigned images │ • 'latest' tag = inconsistent │
│ • Privileged containers     │   deployments                 │
│ • Host network access       │ • Missing network policies    │
│ • Exposed secrets in env    │ • No PodDisruptionBudgets     │
└─────────────────────────────┴───────────────────────────────┘
```

### How Kyverno Solves This

Kyverno intercepts every API request to the Kubernetes API server **before** the resource is persisted to etcd. It can:

1. **Block** the request if it violates a policy (Validate + enforce mode)
2. **Automatically fix** common issues before saving (Mutate)
3. **Alert** teams about violations without blocking (Validate + audit mode)
4. **Create companion resources** automatically (Generate)

### Who Should Use Kyverno?

| Role | Use Case |
|---|---|
| **Platform/SRE Teams** | Enforce cluster-wide standards across all tenant teams |
| **Security Teams** | Implement Pod Security Standards, image signing |
| **DevOps Teams** | Auto-inject sidecar containers, labels, annotations |
| **Compliance Teams** | Audit-mode reporting for regulatory compliance |

---

## 3. How Kyverno Works — Architecture Deep Dive

### The Admission Webhook Mechanism

Every time you run `kubectl apply`, `kubectl create`, or a CI/CD pipeline deploys something, the request goes to the **Kubernetes API Server**. The API Server has a hook mechanism called **Admission Controllers** — checkpoints that can inspect, modify, or reject requests.

Kyverno registers itself as two types of webhooks:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        kubectl apply -f deployment.yaml                  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Kubernetes API Server                             │
│                                                                          │
│  ┌───────────────┐    ┌──────────────────────────────────────────────┐  │
│  │ Authentication│───▶│         Admission Control Pipeline           │  │
│  └───────────────┘    │                                              │  │
│                        │  Step 1: MutatingAdmissionWebhook           │  │
│                        │  ┌──────────────────────────────────┐       │  │
│                        │  │  Kyverno Mutation Webhook        │       │  │
│                        │  │  • Add labels                    │       │  │
│                        │  │  • Set resource limits           │       │  │
│                        │  │  • Inject sidecars               │       │  │
│                        │  └──────────────────────────────────┘       │  │
│                        │             │                                │  │
│                        │             ▼  (modified resource)           │  │
│                        │  Step 2: ValidatingAdmissionWebhook          │  │
│                        │  ┌──────────────────────────────────┐       │  │
│                        │  │  Kyverno Validation Webhook      │       │  │
│                        │  │  • Check required labels         │       │  │
│                        │  │  • Verify image registry         │       │  │
│                        │  │  • Enforce security contexts     │       │  │
│                        │  └──────────────────────────────────┘       │  │
│                        └──────────────────────┬───────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
                    ▼                            ▼
           ✅ ALLOWED                    ❌ REJECTED
      Saved to etcd                  Error returned to user
      Resource created
```

### Kyverno's Internal Components

When you install Kyverno, it deploys the following in the `kyverno` namespace:

```
kyverno namespace
├── kyverno (main admission controller)          ← Handles webhook calls
│    ├── MutatingWebhookConfiguration            ← Registered with API Server
│    └── ValidatingWebhookConfiguration          ← Registered with API Server
│
├── kyverno-background-controller                ← Handles generate + cleanup policies
│    └── Watches cluster for existing resources
│
├── kyverno-cleanup-controller                   ← Handles TTL-based cleanup policies
│
└── kyverno-reports-controller                   ← Generates PolicyReport CRDs
      └── Stores audit results as Kubernetes objects
```

### The Policy Matching Process

When Kyverno receives a webhook call, it:

1. Looks at the **resource kind** (Pod, Deployment, ConfigMap, etc.)
2. Looks at the **namespace** (is this namespace selected by the policy?)
3. Looks at the **operation** (CREATE, UPDATE, DELETE)
4. Evaluates **match/exclude** rules
5. Applies the policy logic (validate/mutate/generate)

```yaml
# Policy matching works like a filter chain:
spec:
  rules:
    - name: my-rule
      match:
        any:
          - resources:
              kinds: [Pod]           # ← Match only Pods
              namespaces: [prod]     # ← In the "prod" namespace
              operations: [CREATE]   # ← Only on creation
      exclude:
        any:
          - resources:
              namespaces: [kube-system]  # ← But NOT in kube-system
```

---

## 4. Kyverno Policy Types

### 4.1 ClusterPolicy vs Policy

| | `ClusterPolicy` | `Policy` |
|---|---|---|
| **Scope** | Entire cluster (all namespaces) | Single namespace only |
| **Use case** | Platform-wide standards | Namespace-specific rules |
| **Who creates** | Platform/SRE teams | App teams (if RBAC allows) |

### 4.2 Validate Policies

**What:** Check that a resource meets your rules. If it doesn't, either block it (`Enforce`) or log it (`Audit`).

```
                  validateFailureAction: Enforce
                         │
         ┌───────────────┴───────────────┐
         │                               │
    Rule PASSES                     Rule FAILS
         │                               │
    ✅ Resource Created            ❌ Request Rejected
                                   (error shown to user)

                  validateFailureAction: Audit
                         │
         ┌───────────────┴───────────────┐
         │                               │
    Rule PASSES                     Rule FAILS
         │                               │
    ✅ Resource Created            ✅ Resource Created
                                   + PolicyReport entry created
                                   (no blocking)
```

### 4.3 Mutate Policies

**What:** Automatically change the resource before it is saved. The user doesn't even notice — the resource is silently corrected.

Common use cases:
- Add required labels automatically
- Set default resource limits if missing
- Add imagePullPolicy: Always
- Inject init containers or sidecars

### 4.4 Generate Policies

**What:** When resource A is created, automatically create resource B. Think of it as automation triggered by Kubernetes events.

Example: When a new namespace is created → automatically create:
- A default NetworkPolicy
- A ResourceQuota
- A LimitRange
- An RBAC RoleBinding

### 4.5 Verify Image Policies

**What:** Ensure container images have valid cryptographic signatures (using Sigstore/Cosign or Notary). Prevents unsigned or tampered images from running.

### 4.6 Cleanup Policies

**What:** Automatically delete resources older than a certain age or matching certain conditions. Think of it as garbage collection with rules.

---

## 5. Installation via Helm

### Prerequisites

```bash
# Verify your cluster is accessible
kubectl cluster-info

# Check kubectl version
kubectl version --client

# Ensure Helm is installed
helm version
# Should output: version.BuildInfo{Version:"v3.x.x", ...}
```

### Step 1 — Add the Kyverno Helm Repository

```bash
# Add the official Kyverno Helm repo
helm repo add kyverno https://kyverno.github.io/kyverno/

# Update your local Helm repo cache
helm repo update

# Verify the repo was added
helm repo list
# NAME      URL
# kyverno   https://kyverno.github.io/kyverno/

# (Optional) Browse available chart versions
helm search repo kyverno
# NAME                            CHART VERSION   APP VERSION   DESCRIPTION
# kyverno/kyverno                 3.x.x           v1.x.x        Kubernetes Native Policy Management
# kyverno/kyverno-policies        3.x.x           v1.x.x        Pod Security Policies
```

### Step 2 — Create a Namespace

```bash
# Create dedicated namespace for Kyverno
kubectl create namespace kyverno
```

### Step 3 — Install Kyverno

#### Option A: Standard Install (Recommended for most clusters)

```bash
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --version 3.2.6
```

#### Option B: High Availability Install (Recommended for Production)

```bash
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --version 3.2.6 \
  --set admissionController.replicas=3 \
  --set backgroundController.replicas=2 \
  --set cleanupController.replicas=2 \
  --set reportsController.replicas=2
```

#### Option C: Custom values.yaml (Best Practice for GitOps)

Create a file `kyverno-values.yaml`:

```yaml
# kyverno-values.yaml
# ─────────────────────────────────────────────
# Kyverno Helm Values — Production Configuration
# ─────────────────────────────────────────────

admissionController:
  replicas: 3                    # HA: 3 replicas for admission controller
  # (Critical: this MUST be available or all API requests may fail
  #  when failurePolicy is set to Fail)

  resources:
    limits:
      memory: 384Mi
      cpu: 500m
    requests:
      memory: 128Mi
      cpu: 100m

  # Anti-affinity to spread pods across nodes
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app.kubernetes.io/component: admission-controller
          topologyKey: kubernetes.io/hostname

backgroundController:
  replicas: 2

cleanupController:
  replicas: 2

reportsController:
  replicas: 2

# Webhook configuration
config:
  # Exclude kyverno's own namespace from policy enforcement
  # (prevents deadlock during startup)
  webhooks:
    - name: mutating
      failurePolicy: Ignore        # Don't block if Kyverno is down (use 'Fail' for strict security)
    - name: validating
      failurePolicy: Ignore

# Enable metrics for Prometheus
features:
  policyExceptions:
    enabled: true                  # Allow exceptions to policies

# Grafana dashboard ConfigMap
grafana:
  enabled: false                   # Set true if you have Grafana installed
```

Apply with:

```bash
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --version 3.2.6 \
  --values kyverno-values.yaml
```

### Step 4 — Verify Installation

```bash
# Check that all Kyverno pods are Running
kubectl get pods -n kyverno
# NAME                                              READY   STATUS    RESTARTS   AGE
# kyverno-admission-controller-7d8b9f6d5-abc12      1/1     Running   0          2m
# kyverno-admission-controller-7d8b9f6d5-def34      1/1     Running   0          2m
# kyverno-admission-controller-7d8b9f6d5-ghi56      1/1     Running   0          2m
# kyverno-background-controller-5c7d9b8f-jkl78      1/1     Running   0          2m
# kyverno-cleanup-controller-6f8b9d7c-mno90         1/1     Running   0          2m
# kyverno-reports-controller-4d6c8b9a-pqr12         1/1     Running   0          2m

# Check Kyverno CRDs were installed
kubectl get crd | grep kyverno
# clusterpolicies.kyverno.io
# policies.kyverno.io
# policyreports.wgpolicyk8s.io
# clusterpolicyreports.wgpolicyk8s.io
# updaterequests.kyverno.io
# ...

# Check Kyverno services
kubectl get svc -n kyverno
# NAME                        TYPE        CLUSTER-IP       PORT(S)
# kyverno-svc                 ClusterIP   10.100.xx.xx     443/TCP
# kyverno-background-svc      ClusterIP   10.100.xx.xx     8000/TCP

# Check webhooks are registered
kubectl get mutatingwebhookconfigurations | grep kyverno
kubectl get validatingwebhookconfigurations | grep kyverno
```

### Step 5 — (Optional) Install Kyverno Pod Security Policies

Kyverno ships a separate chart with pre-built Pod Security Standard policies:

```bash
helm install kyverno-policies kyverno/kyverno-policies \
  --namespace kyverno \
  --set podSecurityStandard=baseline \    # 'privileged', 'baseline', or 'restricted'
  --set validationFailureAction=Audit     # Start with Audit, switch to Enforce later
```

### Upgrade Kyverno

```bash
# Pull latest chart info
helm repo update

# Upgrade (always check release notes for breaking changes first)
helm upgrade kyverno kyverno/kyverno \
  --namespace kyverno \
  --values kyverno-values.yaml
```

### Uninstall Kyverno

```bash
# Remove Kyverno
helm uninstall kyverno --namespace kyverno

# Clean up CRDs (Helm does NOT delete CRDs automatically)
kubectl delete crd $(kubectl get crd | grep kyverno | awk '{print $1}')
kubectl delete crd $(kubectl get crd | grep wgpolicyk8s | awk '{print $1}')
```

---

## 6. Writing Your First Policies

### Anatomy of a Kyverno Policy

Every Kyverno policy follows this structure:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy                    # ClusterPolicy (all namespaces) or Policy (one namespace)
metadata:
  name: my-first-policy
  annotations:
    policies.kyverno.io/title: "Human-readable title"
    policies.kyverno.io/category: "Security"
    policies.kyverno.io/severity: "medium"         # low | medium | high | critical
    policies.kyverno.io/description: >-
      Describe what this policy does and why.

spec:
  # ─── What happens when a resource FAILS this policy? ───
  validationFailureAction: Enforce     # Enforce (block) or Audit (log only)

  # ─── Should existing resources also be checked? ───
  background: true                     # true = audit existing resources too

  rules:
    - name: rule-name                  # Unique name for each rule
      
      # ─── Which resources does this rule apply to? ───
      match:
        any:
          - resources:
              kinds:
                - Pod                  # Resource kind(s)
              namespaces:
                - default              # (optional) limit to namespaces
              operations:
                - CREATE               # CREATE | UPDATE | DELETE | CONNECT
      
      # ─── Which resources should be EXCLUDED? ───
      exclude:
        any:
          - resources:
              namespaces:
                - kube-system          # Never touch system namespaces

      # ─── The actual policy logic (ONE of these) ───
      validate:    # OR
      mutate:      # OR
      generate:    # OR
      verifyImages:
```

### Understanding `match` and `exclude`

```
Incoming Resource
        │
        ▼
   Does it match ANY of the match.any[] conditions?
        │
        ├── NO  ──▶  Policy SKIPPED (resource not affected)
        │
        └── YES ──▶  Is it excluded by ANY exclude.any[] condition?
                          │
                          ├── YES ──▶  Policy SKIPPED
                          │
                          └── NO  ──▶  Policy APPLIED ✓
```

---

## 7. Real-World Policy Examples

### Policy 1: Require Labels on All Deployments (Validate)

**Why:** Labels are essential for monitoring, cost allocation, and incident response. Without them, you cannot identify what a workload is, who owns it, or what environment it runs in.

```yaml
# File: require-labels.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-deployment-labels
  annotations:
    policies.kyverno.io/title: "Require Standard Labels"
    policies.kyverno.io/category: "Best Practices"
    policies.kyverno.io/severity: "medium"
    policies.kyverno.io/description: >-
      Every Deployment must have 'app', 'owner', and 'environment' labels
      for observability, cost tracking, and incident response.

spec:
  validationFailureAction: Enforce       # Block deployments without labels
  background: true                       # Also audit existing deployments

  rules:
    - name: check-required-labels
      match:
        any:
          - resources:
              kinds: [Deployment]
              operations: [CREATE, UPDATE]

      validate:
        message: >-
          Deployment '{{ request.object.metadata.name }}' is missing required labels.
          Must have: app, owner, environment.
          Example: app=payment-service, owner=team-payments, environment=prod

        # Pattern: all listed fields must be present and non-empty
        pattern:
          metadata:
            labels:
              app: "?*"           # ?* means: at least one character (non-empty)
              owner: "?*"
              environment: "?*"
```

**Testing:**

```bash
# Apply the policy
kubectl apply -f require-labels.yaml

# ❌ This will be REJECTED (missing labels)
kubectl create deployment nginx-bad --image=nginx
# Error: admission webhook "validate.kyverno.svc" denied the request:
# Deployment 'nginx-bad' is missing required labels...

# ✅ This will be ACCEPTED
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-good
  labels:
    app: nginx
    owner: team-platform
    environment: prod
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        owner: team-platform
        environment: prod
    spec:
      containers:
        - name: nginx
          image: nginx:1.25.3
EOF
```

---

### Policy 2: Disallow `latest` Image Tag (Validate)

**Why:** The `latest` tag is mutable — it points to whatever the latest build was. If a new build breaks the image, all pods will pull broken code on restart. Pinned tags ensure reproducibility.

```yaml
# File: disallow-latest-tag.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
  annotations:
    policies.kyverno.io/title: "Disallow Latest Image Tag"
    policies.kyverno.io/category: "Best Practices"
    policies.kyverno.io/severity: "medium"
    policies.kyverno.io/description: >-
      The 'latest' tag is mutable and leads to unpredictable deployments.
      All images must use a specific, immutable tag (e.g., nginx:1.25.3).

spec:
  validationFailureAction: Enforce
  background: true

  rules:
    - name: require-image-tag
      match:
        any:
          - resources:
              kinds: [Pod]

      exclude:
        any:
          - resources:
              namespaces: [kube-system, kyverno]

      validate:
        message: >-
          Image '{{ element.image }}' must not use the 'latest' tag.
          Use a specific tag: e.g., nginx:1.25.3 or nginx@sha256:abc123...

        # Iterate over each container and check the image tag
        foreach:
          - list: "request.object.spec.containers"
            deny:
              conditions:
                any:
                  # Deny if tag is exactly 'latest'
                  - key: "{{ element.image }}"
                    operator: Equals
                    value: "*:latest"
                  # Deny if no tag is specified at all (defaults to latest)
                  - key: "{{ element.image }}"
                    operator: NotContains
                    value: ":"
```

---

### Policy 3: Auto-Add Labels to Pods (Mutate)

**Why:** Even if developers forget to add certain labels, we want pods to always have a `managed-by: kyverno` label for tracking purposes. Mutation silently fixes this without bothering developers.

```yaml
# File: mutate-add-labels.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
  annotations:
    policies.kyverno.io/title: "Add Default Labels"
    policies.kyverno.io/category: "Best Practices"
    policies.kyverno.io/description: >-
      Automatically adds managed-by label to all pods.
      Also adds the creator's username from the request for audit purposes.

spec:
  rules:
    - name: add-managed-by-label
      match:
        any:
          - resources:
              kinds: [Pod]
              operations: [CREATE]

      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              # Add a fixed label
              managed-by: "kyverno"
              # Add dynamic label from the request context
              # (who submitted this request)
              created-by: "{{ request.userInfo.username }}"
```

---

### Policy 4: Set Default Resource Limits (Mutate)

**Why:** Pods without resource limits can consume all available CPU/memory on a node, starving other pods. We auto-set sensible defaults if none are provided.

```yaml
# File: set-default-resources.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: set-default-resources
  annotations:
    policies.kyverno.io/title: "Set Default Resource Limits"
    policies.kyverno.io/category: "Resource Management"
    policies.kyverno.io/description: >-
      If a container does not specify resource requests/limits, automatically
      set conservative defaults. This prevents noisy-neighbor issues.

spec:
  rules:
    - name: set-default-resource-limits
      match:
        any:
          - resources:
              kinds: [Pod]
              operations: [CREATE]

      mutate:
        foreach:
          - list: "request.object.spec.containers"
            patchStrategicMerge:
              spec:
                containers:
                  - name: "{{ element.name }}"
                    resources:
                      requests:
                        # Only set if not already present (+(request)) conditional)
                        memory: "64Mi"
                        cpu: "50m"
                      limits:
                        memory: "256Mi"
                        cpu: "200m"
```

---

### Policy 5: Auto-Create NetworkPolicy for New Namespaces (Generate)

**Why:** By default, Kubernetes allows all traffic between all pods. When a new namespace is created, you want to ensure it has a default deny-all NetworkPolicy immediately — before any pods are created in it.

```yaml
# File: generate-network-policy.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-default-network-policy
  annotations:
    policies.kyverno.io/title: "Generate Default NetworkPolicy"
    policies.kyverno.io/category: "Security"
    policies.kyverno.io/severity: "high"
    policies.kyverno.io/description: >-
      When a new namespace is created (excluding system namespaces),
      automatically create a default deny-all NetworkPolicy.
      Teams must then explicitly allow the traffic they need.

spec:
  rules:
    - name: generate-deny-all-network-policy
      match:
        any:
          - resources:
              kinds: [Namespace]
              operations: [CREATE]

      exclude:
        any:
          - resources:
              names:
                - kube-system
                - kube-public
                - kube-node-lease
                - kyverno

      generate:
        # What kind of resource to create
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy

        # Name of the generated resource
        name: default-deny-all

        # Create it in the same namespace that was just created
        namespace: "{{ request.object.metadata.name }}"

        # synchronize: true means if the policy changes, existing generated
        # resources are updated. Also, if someone deletes the NetworkPolicy,
        # Kyverno will recreate it.
        synchronize: true

        data:
          metadata:
            labels:
              generated-by: kyverno
          spec:
            podSelector: {}        # Selects ALL pods in this namespace
            policyTypes:
              - Ingress
              - Egress
            # No ingress/egress rules = deny everything
```

**Testing Generate Policies:**

```bash
# Apply the policy
kubectl apply -f generate-network-policy.yaml

# Create a new namespace
kubectl create namespace my-new-app

# Kyverno should have auto-created a NetworkPolicy in it
kubectl get networkpolicies -n my-new-app
# NAME               POD-SELECTOR   AGE
# default-deny-all   <none>         2s   ← Auto-created by Kyverno! ✓
```

---

### Policy 6: Enforce Pod Security — No Root Containers (Validate)

**Why:** Running containers as root gives them the same privileges as root on the host (if the container breaks out). Always run as a non-root user.

```yaml
# File: disallow-root-containers.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-root-containers
  annotations:
    policies.kyverno.io/title: "Disallow Root Containers"
    policies.kyverno.io/category: "Pod Security"
    policies.kyverno.io/severity: "high"

spec:
  validationFailureAction: Enforce
  background: true

  rules:
    - name: check-runAsNonRoot
      match:
        any:
          - resources:
              kinds: [Pod]

      exclude:
        any:
          - resources:
              namespaces: [kube-system]

      validate:
        message: >-
          Containers must not run as root. Set securityContext.runAsNonRoot: true
          and securityContext.runAsUser to a value > 0.

        pattern:
          spec:
            # Check spec-level securityContext
            securityContext:
              runAsNonRoot: true

            # Check each container's securityContext
            containers:
              - name: "*"
                securityContext:
                  runAsNonRoot: true
                  # Optionally: also enforce a specific UID range
                  # runAsUser: ">0"
```

---

### Policy 7: Disallow Privileged Containers (Validate)

**Why:** Privileged containers have nearly full host system access — they can mount host filesystems, manipulate network interfaces, and more. This is almost never needed for application containers.

```yaml
# File: disallow-privileged.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
  annotations:
    policies.kyverno.io/title: "Disallow Privileged Containers"
    policies.kyverno.io/category: "Pod Security"
    policies.kyverno.io/severity: "critical"

spec:
  validationFailureAction: Enforce
  background: true

  rules:
    - name: privileged-containers
      match:
        any:
          - resources:
              kinds: [Pod]

      validate:
        message: >-
          Privileged containers are not allowed.
          Remove securityContext.privileged: true from your container spec.

        pattern:
          spec:
            containers:
              - name: "*"
                =(securityContext):        # =(field) means: if field exists, validate it
                  =(privileged): "false"   # privileged must be false or absent
```

---

## 8. Policy Reports

Kyverno generates **PolicyReport** and **ClusterPolicyReport** Kubernetes objects. These are standard resources you can query with kubectl.

```bash
# View all policy reports in a namespace
kubectl get policyreports -n default

# Detailed view
kubectl get policyreports -n default -o yaml

# View cluster-wide policy reports
kubectl get clusterpolicyreports

# Count violations by policy
kubectl get policyreports -A -o json | \
  jq '.items[].results[] | select(.result == "fail") | .policy' | \
  sort | uniq -c | sort -rn
```

### Sample PolicyReport output:

```yaml
apiVersion: wgpolicyk8s.io/v1alpha2
kind: PolicyReport
metadata:
  name: cpol-disallow-latest-tag
  namespace: default
results:

  # PASS result
  - message: "validation rule 'require-image-tag' passed."
    policy: disallow-latest-tag
    result: pass
    rule: require-image-tag
    source: kyverno
    resources:
      - apiVersion: v1
        kind: Pod
        name: nginx-good
        namespace: default

  # FAIL result
  - message: "Image 'nginx:latest' must not use the 'latest' tag."
    policy: disallow-latest-tag
    result: fail
    rule: require-image-tag
    source: kyverno
    resources:
      - apiVersion: v1
        kind: Pod
        name: nginx-bad
        namespace: default

summary:
  pass: 8
  fail: 2
  warn: 0
  error: 0
  skip: 0
```

---

## 9. Kyverno CLI for Testing

The Kyverno CLI lets you **test policies locally** without needing a cluster.

### Install the CLI

```bash
# macOS (Homebrew)
brew install kyverno

# Linux (direct binary)
curl -LO https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_x86_64.tar.gz
tar -xf kyverno-cli_linux_x86_64.tar.gz
chmod +x kyverno
sudo mv kyverno /usr/local/bin/

# Verify
kyverno version
```

### Test a Policy Against a Resource

```bash
# Structure
kyverno apply <policy-file> --resource <resource-file>

# Example: Test the "disallow latest tag" policy
kyverno apply disallow-latest-tag.yaml --resource test-pod.yaml

# Output:
# Applying 1 policy rule(s) to 1 resource(s)...
#
# policy disallow-latest-tag -> resource default/Pod/nginx-test
#   FAILED
#   require-image-tag: Image 'nginx:latest' must not use the 'latest' tag.
#
# pass: 0, fail: 1, warn: 0, error: 0, skip: 0
```

### Write a Formal Test Suite

Create a `kyverno-test.yaml` file:

```yaml
# kyverno-test.yaml
name: test-disallow-latest-tag
policies:
  - disallow-latest-tag.yaml
resources:
  - test-resources/
results:
  - policy: disallow-latest-tag
    rule: require-image-tag
    resource: pod-with-latest
    namespace: default
    result: fail           # We expect this to fail

  - policy: disallow-latest-tag
    rule: require-image-tag
    resource: pod-with-version
    namespace: default
    result: pass           # We expect this to pass
```

Run the test suite:

```bash
kyverno test .
# Loading test ( kyverno-test.yaml ) ...
#   Test Results:  2 tests
#   Passed: 2
#   Failed: 0
```

---

## 10. Best Practices

### 1. Start with Audit Mode, Then Enforce

```yaml
# Phase 1: Learn what would be blocked without actually blocking
spec:
  validationFailureAction: Audit     # Just log violations

# Phase 2: After reviewing PolicyReports and fixing violations, switch to:
spec:
  validationFailureAction: Enforce   # Now actually block
```

### 2. Always Exclude System Namespaces

```yaml
exclude:
  any:
    - resources:
        namespaces:
          - kube-system
          - kube-public
          - kube-node-lease
          - kyverno
          - monitoring    # prometheus/grafana
          - cert-manager
```

### 3. Use PolicyExceptions for Legitimate Exceptions

Instead of weakening a policy for everyone, create a targeted exception:

```yaml
# File: exception-privileged-node-agent.yaml
apiVersion: kyverno.io/v2beta1
kind: PolicyException
metadata:
  name: allow-fluentd-privileged
  namespace: logging                  # Exception is namespace-scoped
spec:
  exceptions:
    - policyName: disallow-privileged-containers
      ruleNames:
        - privileged-containers
  match:
    any:
      - resources:
          kinds: [Pod]
          namespaces: [logging]
          names: ["fluentd-*"]        # Only fluentd pods, not everything
```

### 4. Use Annotations for Documentation

```yaml
metadata:
  annotations:
    policies.kyverno.io/title: "Short, clear title"
    policies.kyverno.io/category: "Security | Best Practices | Resource Management"
    policies.kyverno.io/severity: "low | medium | high | critical"
    policies.kyverno.io/minversion: "1.6.0"
    policies.kyverno.io/description: >-
      Why this policy exists. What problem it solves.
      What developers need to do to comply.
    policies.kyverno.io/subject: "Pod, Deployment"
```

### 5. Use `background: false` for Expensive Policies

If a policy uses external calls or complex logic, setting `background: false` prevents Kyverno from scanning all existing resources (only new/updated resources are evaluated):

```yaml
spec:
  background: false   # Don't scan existing resources, only new ones
```

### 6. HA Deployment Considerations

```
⚠️  IMPORTANT: webhookFailurePolicy
─────────────────────────────────────────────────────────────────────────
If Kyverno goes down AND webhookFailurePolicy is "Fail":
  → ALL API requests will be rejected (cluster appears broken)

If Kyverno goes down AND webhookFailurePolicy is "Ignore":
  → Resources are allowed through without policy checks

Recommendation:
  Production with strict security: Fail (but ensure HA with 3+ replicas)
  Production with availability priority: Ignore (with HA + alerting on Kyverno health)
```

---

## 11. Kyverno vs. OPA Gatekeeper

Both are CNCF policy engines for Kubernetes. Here's a detailed comparison:

| Dimension | Kyverno | OPA Gatekeeper |
|---|---|---|
| **Policy Language** | YAML (no new language) | Rego (dedicated logic language) |
| **Learning Curve** | Low — if you know YAML, you can write policies | High — Rego has a steep learning curve |
| **Mutating Policies** | ✅ Native, first-class | ⚠️ Limited, complex to implement |
| **Generate Policies** | ✅ Native | ❌ Not supported |
| **Image Verification** | ✅ Native (Cosign/Notary) | ❌ Requires additional tools |
| **Cleanup Policies** | ✅ Native | ❌ Not supported |
| **Policy Reports** | ✅ PolicyReport CRD | ✅ PolicyReport CRD |
| **Testing** | ✅ Kyverno CLI | ✅ OPA CLI / conftest |
| **Community** | CNCF Graduated | CNCF Graduated |
| **Flexibility** | Moderate (YAML-constrained) | High (Turing-complete language) |
| **Complex Logic** | Moderate (JMESPath expressions) | High (full Rego programs) |
| **Typical Users** | Platform teams wanting simplicity | Security teams needing advanced logic |

**When to choose Kyverno:** You want a quick, intuitive setup with YAML-native policies and need mutation/generation capabilities.

**When to choose Gatekeeper:** You need very complex, conditional policy logic that goes beyond what YAML expressions can express, and your team is comfortable with Rego.

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────────────┐
│                    KYVERNO CHEAT SHEET                               │
├──────────────────────────────────────────────────────────────────────┤
│  POLICY TYPES                                                        │
│  validate    → Block or audit non-compliant resources                │
│  mutate      → Auto-modify resources before saving                   │
│  generate    → Auto-create resources when a trigger resource appears │
│  verifyImages→ Enforce image signing                                  │
│  cleanup     → Auto-delete stale resources                           │
├──────────────────────────────────────────────────────────────────────┤
│  FAILURE ACTIONS                                                     │
│  Enforce → Block (use for production-ready policies)                 │
│  Audit   → Log only (use when introducing new policies)              │
├──────────────────────────────────────────────────────────────────────┤
│  KEY COMMANDS                                                        │
│  kubectl get clusterpolicies                                         │
│  kubectl get policyreports -A                                        │
│  kubectl describe clusterpolicy <name>                               │
│  kyverno apply policy.yaml --resource resource.yaml                  │
│  kyverno test .                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  HELM INSTALL (QUICK)                                                │
│  helm repo add kyverno https://kyverno.github.io/kyverno/            │
│  helm install kyverno kyverno/kyverno -n kyverno --create-namespace  │
└──────────────────────────────────────────────────────────────────────┘
```

---

*Guide version: Kyverno 1.12.x / Helm Chart 3.2.x*
*Reference: https://kyverno.io/docs/*