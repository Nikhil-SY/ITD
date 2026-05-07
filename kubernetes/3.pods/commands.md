Here’s a **complete, interview-style guide** on **Pod-related commands in Kubernetes** 👇

---

# 🔹 Pod Commands in Kubernetes

## 🧠 Basic Idea

👉 Pod commands are used to:

* Create
* View
* Debug
* Manage lifecycle

---

# ⚙️ 1. List Pods

```bash id="8vv7n6"
kubectl get pods
```

👉 With more details:

```bash id="j3l5y1"
kubectl get pods -o wide
```

👉 Specific namespace:

```bash id="z0cs21"
kubectl get pods -n dev
```

---

# ⚙️ 2. Create Pod

```bash id="n7o0wx"
kubectl run nginx --image=nginx
```

👉 In namespace:

```bash id="d9o3cw"
kubectl run nginx --image=nginx -n dev
```

---

## 🔹 Create using YAML

```bash id="s8rm93"
kubectl apply -f pod.yaml
```

---

# ⚙️ 3. Describe Pod

```bash id="4q9e1p"
kubectl describe pod nginx
```

👉 Shows:

* Events
* Errors
* Node assigned

---

# ⚙️ 4. Delete Pod

```bash id="t4d3lp"
kubectl delete pod nginx
```

👉 Force delete:

```bash id="i4k3n9"
kubectl delete pod nginx --force --grace-period=0
```

---

# ⚙️ 5. View Pod Logs

```bash id="k1l9mn"
kubectl logs nginx
```

👉 For multi-container pod:

```bash id="1kq4cz"
kubectl logs nginx -c container-name
```

👉 Follow logs:

```bash id="q3u7c2"
kubectl logs -f nginx
```

---

# ⚙️ 6. Execute Command Inside Pod

```bash id="c8l6zp"
kubectl exec -it nginx -- /bin/bash
```

👉 Example:

```bash id="v3z7s9"
kubectl exec -it nginx -- ls /
```

---

# ⚙️ 7. Port Forwarding

```bash id="r8z3k1"
kubectl port-forward pod/nginx 8080:80
```

👉 Access app locally:

```
http://localhost:8080
```

---

# ⚙️ 8. Get Pod YAML

```bash id="0gn8n7"
kubectl get pod nginx -o yaml
```

---

# ⚙️ 9. Edit Pod

```bash id="x3l1pw"
kubectl edit pod nginx
```

⚠️ Limited changes allowed

---

# ⚙️ 10. Check Pod Events

```bash id="tx9q6b"
kubectl get events
```

👉 Helps in debugging

---

# ⚙️ 11. Watch Pod Status (Real-time)

```bash id="s4j9kp"
kubectl get pods -w
```

---

# ⚙️ 12. Copy Files To/From Pod

```bash id="d7l8zp"
kubectl cp file.txt nginx:/tmp/
```

👉 From pod:

```bash id="p8l6t3"
kubectl cp nginx:/tmp/file.txt .
```

---

# ⚙️ 13. Restart Pod

👉 Pods don’t restart directly

Use:

```bash id="5h8z1y"
kubectl delete pod nginx
```

✔️ If managed by Deployment → auto recreated

---

# ⚙️ 14. Check Pod Resource Usage

```bash id="9p2k4r"
kubectl top pod
```

👉 Specific namespace:

```bash id="n8k2pl"
kubectl top pod -n dev
```

---

# ⚙️ 15. Debug Pod (Advanced)

```bash id="g3k9l2"
kubectl debug -it nginx --image=busybox
```

👉 Used for troubleshooting

---

# ⚙️ 16. Get Pod by Label

```bash id="q6p2n9"
kubectl get pods -l app=nginx
```

---

# ⚙️ 17. Delete Multiple Pods

```bash id="q4k7p1"
kubectl delete pods -l app=nginx
```

---

# 🌍 Real-World Example

## 🎬 Scenario: App Debugging

1. Check pods:

```bash id="8y2k6m"
kubectl get pods
```

---

2. See error:

```bash id="x6p1z8"
kubectl describe pod app-pod
```

---

3. Check logs:

```bash id="p2m7k4"
kubectl logs app-pod
```

---

4. Enter pod:

```bash id="c3k9z7"
kubectl exec -it app-pod -- /bin/bash
```

---

✔️ Debug completed

---

# 💥 Common Mistakes

---

## ❌ Wrong Namespace

```bash id="r4t8k2"
kubectl get pods
```

👉 No output

✔️ Fix:

```bash id="b3k7n9"
kubectl get pods -n dev
```

---

## ❌ Pod Deleted

👉 If standalone pod:

* Gone permanently

👉 If Deployment:

* Recreated automatically

---

# ⚡ Interview Key Points

* `kubectl get pods` → view pods
* `describe` → debug
* `logs` → application logs
* `exec` → access container
* `port-forward` → local testing
* Pods are **ephemeral**

---

# 🧠 One-Line Summary

👉 **Pod commands help you create, manage, and debug running containers in Kubernetes**

---

# 🔥 Quick Cheat Sheet

```bash id="6j3k9p"
kubectl get pods
kubectl describe pod <name>
kubectl logs <name>
kubectl exec -it <name> -- /bin/bash  #you should open 10250 port which is kubelet port to login in to pod
kubectl delete pod <name>
```

---

# 🔥 Follow-up Questions

1. Difference between logs and exec?
2. Can we restart a pod directly?
3. What happens when pod is deleted?
4. How to debug failing pods?

---
