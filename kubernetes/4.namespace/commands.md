Here’s a **complete, interview-style guide** to **all important Namespace commands in Kubernetes** 👇

---

# 🔹 Namespace Commands in Kubernetes

## 🧠 Basic Idea

👉 Namespace commands are used to:

* Create
* View
* Switch
* Delete
* Manage resources inside namespaces

---

# ⚙️ 1. List Namespaces

```bash
kubectl get namespaces
```

👉 Short form:

```bash
kubectl get ns
```

✔️ Output:

* default
* kube-system
* kube-public
* kube-node-lease

---

# ⚙️ 2. Create Namespace

```bash
kubectl create namespace dev
```

✔️ Creates a new namespace called `dev`

---

## 🔹 Create using YAML

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

```bash
kubectl apply -f namespace.yaml
```

---

# ⚙️ 3. Delete Namespace

```bash
kubectl delete namespace dev
```

⚠️ Important:

* Deletes **all resources inside it**

---

# ⚙️ 4. Get Resources in a Namespace

```bash
kubectl get pods -n dev
```

👉 Examples:

```bash
kubectl get all -n dev
kubectl get svc -n dev
kubectl get deployments -n dev
```

---

# ⚙️ 5. Describe Namespace

```bash
kubectl describe namespace dev
```

👉 Shows:

* Labels
* Resource quotas
* Events

---

# ⚙️ 6. Switch Default Namespace (Very Important)

```bash
kubectl config set-context --current --namespace=dev
```

✔️ Now you don’t need `-n dev` every time

---

# ⚙️ 7. Check Current Namespace

```bash
kubectl config view --minify | grep namespace
```

---

# ⚙️ 8. Run Pod in Specific Namespace

```bash
kubectl run nginx --image=nginx -n dev
```

---

# ⚙️ 9. Apply Resources in Namespace

```bash
kubectl apply -f app.yaml -n dev
```

---

## 🔹 Or define inside YAML

```yaml
metadata:
  namespace: dev
```

---

# ⚙️ 10. Edit Namespace

```bash
kubectl edit namespace dev
```

👉 Used to:

* Add labels
* Modify configs

---

# ⚙️ 11. Label Namespace

```bash
kubectl label namespace dev env=development
```

---

# ⚙️ 12. Annotate Namespace

```bash
kubectl annotate namespace dev owner=nikhil
```

---

# ⚙️ 13. Remove Label

```bash
kubectl label namespace dev env-
```

---

# ⚙️ 14. View Namespace YAML

```bash
kubectl get namespace dev -o yaml
```

---

# ⚙️ 15. Resource Quota in Namespace

```bash
kubectl create quota myquota \
  --hard=cpu=2,memory=4Gi \
  -n dev
```

---

# ⚙️ 16. Limit Range in Namespace

```bash
kubectl create limitrange mylimit \
  --default=cpu=500m,memory=512Mi \
  -n dev
```

---

# ⚙️ 17. Delete All Resources in Namespace

```bash
kubectl delete all --all -n dev
```

⚠️ Keeps namespace, deletes resources inside

---

# ⚙️ 18. Copy Resources Between Namespaces

```bash
kubectl get pod nginx -n dev -o yaml | sed 's/dev/prod/' | kubectl apply -n prod -f -
```

👉 Used for migration

---

# 🌍 Real-World Example

## 🎬 Scenario: Dev & Prod

```bash
kubectl create namespace dev
kubectl create namespace prod
```

Deploy app:

```bash
kubectl apply -f app.yaml -n dev
kubectl apply -f app.yaml -n prod
```

✔️ Same app, different environments

---

# 💥 Common Mistakes

---

## ❌ Forgetting Namespace

```bash
kubectl get pods
```

👉 Shows nothing (wrong namespace)

---

## ❌ Deleting Namespace

```bash
kubectl delete ns dev
```

👉 Deletes everything inside

---

# ⚡ Interview Key Points

* Use `-n` flag for namespace
* Use context to avoid repetition
* Namespace deletion removes all resources
* Namespaces isolate resources logically

---

# 🧠 One-Line Summary

👉 **Namespace commands help manage and isolate resources within a Kubernetes cluster**

---

# 🔥 Quick Cheat Sheet

```bash
kubectl get ns
kubectl create ns dev
kubectl delete ns dev
kubectl get pods -n dev
kubectl config set-context --current --namespace=dev
```

---

# 🔥 Follow-up Questions

1. Difference between namespace and context?
2. How to restrict access between namespaces?
3. Can we move pods between namespaces?
4. What happens when namespace is deleted?

---

If you want, I can next give:
👉 **“kubectl complete command cheat sheet (all categories)”**
👉 OR
👉 **“Real-time DevOps interview questions on Kubernetes commands”**
