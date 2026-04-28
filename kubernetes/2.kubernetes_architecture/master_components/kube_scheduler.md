Here’s a **clear, interview-style deep dive** on the **Kubernetes Scheduler (kube-scheduler)** with real-world flow 👇

---

# 🔹 Kubernetes Scheduler (kube-scheduler)

## ✅ Definition

The **Scheduler** is a control-plane component in **Kubernetes** responsible for:

👉 **Assigning Pods to Nodes**

⚠️ Important:

* Scheduler **does NOT create pods**
* It only decides **where the pod should run**

---

## 🧠 Core Responsibility

👉 Finds the **best node** for a pod based on:

* Resource availability (CPU, Memory)
* Constraints (taints, affinity, policies)
* Cluster conditions

---

## ⚙️ How It Works (Step-by-Step)

### 1️⃣ Watch for Unscheduled Pods

* Scheduler continuously watches API Server
* Looks for pods with:

```yaml id="6t80tq"
nodeName: <none>
```

---

### 2️⃣ Select Candidate Nodes (Filtering Phase)

👉 Removes nodes that **cannot run the pod**

Checks:

* Enough CPU / Memory?
* Node is Ready?
* Taints tolerated?
* Node selector matches?

✔️ Output: List of valid nodes

---

### 3️⃣ Rank Nodes (Scoring Phase)

👉 Assigns scores to remaining nodes

Criteria:

* Least resource usage (balanced)
* Data locality
* Affinity rules
* Spreading pods across nodes

✔️ Highest score = best node

---

### 4️⃣ Bind Pod to Node

Scheduler updates API Server:

```yaml id="f0v3xg"
nodeName: worker-node-2
```

✔️ Pod is now assigned

---

### 5️⃣ Kubelet Executes

* Kubelet on that node:

  * Pulls image
  * Starts container

---

# 🔁 Full Flow Summary

```text id="xw1n2y"
Pod Created → API Server → Scheduler → Node Selected → Kubelet → Pod Running
```

---

# 🧩 Key Scheduling Concepts

---

## 🔸 1. Filtering (Predicates)

👉 Removes unsuitable nodes

Examples:

* Insufficient CPU
* Node not ready
* Port conflicts

---

## 🔸 2. Scoring (Priorities)

👉 Ranks nodes

Examples:

* Least loaded node gets higher score
* Even distribution across nodes

---

## 🔸 3. Binding

👉 Final assignment to node

---

# 🌍 Real-World Example (Very Important)

## 🎬 Scenario: OTT Streaming App

You deploy:

```yaml id="d93r6c"
replicas: 3
```

---

### Cluster State:

| Node  | CPU Available |
| ----- | ------------- |
| Node1 | 80%           |
| Node2 | 40%           |
| Node3 | 20%           |

---

### What Scheduler Does:

1. Filters nodes → all valid
2. Scores nodes → prefers balanced usage

✔️ Result:

* Pod1 → Node2
* Pod2 → Node3
* Pod3 → Node1

👉 Ensures **load distribution**

---

# ⚡ Advanced Scheduling Features

---

## 🔹 1. Node Selector

```yaml id="l6c3mh"
nodeSelector:
  disktype: ssd
```

👉 Pod runs only on matching nodes

---

## 🔹 2. Taints & Tolerations

* Taint → restrict nodes
* Toleration → allow pods

👉 Used for:

* Dedicated nodes
* GPU workloads

---

## 🔹 3. Affinity / Anti-Affinity

### Node Affinity

* Place pods on specific nodes

### Pod Affinity

* Place pods together

### Pod Anti-Affinity

* Spread pods across nodes

---

## 🔹 4. Resource Requests & Limits

```yaml id="ycb6q3"
resources:
  requests:
    cpu: "500m"
```

👉 Scheduler uses **requests** for decision

---

# 💥 Failure Scenario

## ❌ No Suitable Node

👉 Pod status:

```text id="hw0c0k"
Pending
```

Reason:

* Insufficient resources
* No matching node

---

## ❌ Node Goes Down After Scheduling

👉 Controller Manager:

* Detects failure
* Reschedules pod

---

# 🔐 Scheduler Does NOT:

❌ Run containers
❌ Monitor health
❌ Store data

✔️ Only decides placement

---

# 🆚 Scheduler vs Controller Manager

| Feature | Scheduler   | Controller Manager |
| ------- | ----------- | ------------------ |
| Role    | Assign node | Maintain state     |
| Action  | Placement   | Create/delete pods |
| Trigger | New pod     | State mismatch     |

---

# ⚡ Interview Key Points

* Scheduler works in **2 phases**:

  * Filtering
  * Scoring
* Uses **resource requests (not limits)**
* Only handles **unscheduled pods**
* Updates **nodeName field**
* Works via API Server

---

# 🧠 One-Line Summary

👉 **Scheduler = Decision maker that chooses the best node for each pod**

---

# 🔥 Follow-up Questions You Might Get

1. Difference between requests and limits?
2. What is taint vs toleration?
3. How does scheduler handle large clusters?
4. Can we customize scheduler?

---

If you want next deep dive:
👉 **“Kubelet in detail (what happens inside node)”**
👉 OR
👉 **“Service + kube-proxy (how traffic reaches pods)”**

Just tell 👍
