---

# 1️⃣ What happens if Jenkins Controller crashes?

### 📌 Answer:

If the **Controller** in **Jenkins** crashes:

### What will happen?

* Running builds will fail
* New builds cannot be scheduled
* UI becomes inaccessible
* Agents lose connection

---

### Why?

Controller is responsible for:

* Job scheduling
* Managing build queue
* Storing configuration
* Maintaining pipeline state

Without controller → orchestration stops.

---

### How to Handle in Production?

✔ Regular backups of:

* `$JENKINS_HOME`
* Job configurations
* Plugins

✔ High Availability setup:

* Run Jenkins on VM with snapshot backup
* Use external database (advanced setup)
* Use Kubernetes + Persistent Volume

✔ Monitoring:

* Prometheus
* Alerts on controller health

---

### Interview One-Line Answer:

> If the Jenkins controller crashes, build scheduling stops and running builds fail because the controller manages orchestration. In production, we handle it using backups, monitoring, and high-availability setups.

---

# 2️⃣ Difference Between Node and Agent?

### 📌 Definition

| Node                             | Agent                             |
| -------------------------------- | --------------------------------- |
| Any machine connected to Jenkins | Worker machine that executes jobs |
| Controller is also a node        | Agent excludes controller         |
| Logical term                     | Functional term                   |

---

### Simple Explanation:

* **Node** = Generic machine in Jenkins
* **Agent** = Node that executes builds

👉 Controller is technically a node, but not typically called an agent.

---

### Interview One-Line:

> A node is any machine part of Jenkins, including the controller. An agent is a worker node specifically used to execute builds.

---

# 3️⃣ How Jenkins Handles Parallel Builds?

Parallel builds are handled using:

* Multiple executors
* Multiple agents
* `parallel` pipeline step

---

### Internally:

1️⃣ Controller checks available executors
2️⃣ Assigns parallel branches to different executors
3️⃣ Each branch runs independently

If:

* Agent has 2 executors → 2 parallel builds
* If no executor → build waits in queue

---

### Example:

```groovy
parallel {
    stage('Test1') {
        steps { sh 'run-test1.sh' }
    }
    stage('Test2') {
        steps { sh 'run-test2.sh' }
    }
}
```

---

### Interview One-Line:

> Jenkins handles parallel builds using multiple executors on agents. Each parallel branch is assigned to a separate executor.

---

# 4️⃣ How Do You Secure Jenkins?

Security is very important in enterprise environments.

---

## 🔐 1. Authentication

* Enable Role-Based Access Control (RBAC)
* Integrate with LDAP / Active Directory

---

## 🔐 2. Authorization

* Matrix-based security
* Role strategy plugin

---

## 🔐 3. Secure Credentials

Use:

* Jenkins Credentials Manager
* Store secrets as:

  * Secret text
  * SSH key
  * Username/password

Never hardcode passwords in Jenkinsfile.

---

## 🔐 4. Secure Agents

* Use SSH keys
* Disable anonymous access
* Restrict agent-to-controller communication

---

## 🔐 5. HTTPS

Always run Jenkins behind:

* NGINX reverse proxy
* SSL certificate

---

### Interview One-Line:

> Jenkins can be secured using authentication, role-based authorization, credentials management, HTTPS configuration, and secure agent communication.

---

# 5️⃣ How Rollback Works in Jenkins?

Jenkins itself does not perform rollback automatically. Rollback is handled using deployment strategy.

---

## 🔁 Common Rollback Methods:

### 1️⃣ Redeploy Previous Artifact

* Jenkins stores build artifacts
* Re-run previous successful build
* Deploy older version

---

### 2️⃣ Blue-Green Deployment

Two environments:

* Blue (Current)
* Green (New)

If issue → switch traffic back to Blue.

---

### 3️⃣ Canary Deployment

Deploy small percentage of traffic.
If issue → stop rollout.

---

### 4️⃣ Docker-Based Rollback

```bash
docker run previous-image-tag
```

---

### Interview One-Line:

> Rollback in Jenkins is typically done by redeploying a previous successful artifact or using deployment strategies like blue-green or canary.

---

# 🔥 Final Quick Rapid-Fire Summary

| Question          | Short Answer                                |
| ----------------- | ------------------------------------------- |
| Controller crash? | Scheduling stops, builds fail               |
| Node vs Agent?    | Node = any machine, Agent = executes builds |
| Parallel builds?  | Uses multiple executors                     |
| Secure Jenkins?   | RBAC + credentials + HTTPS                  |
| Rollback?         | Redeploy previous artifact                  |

---
