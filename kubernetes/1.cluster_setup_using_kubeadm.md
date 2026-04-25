Here’s a **clear, interview-style + practical guide** to set up a **Kubernetes cluster using kubeadm (1 Master + 2 Workers)** with **deep explanation of commands + config files + locations**.

---

# 🧠 1. What is kubeadm?

**kubeadm** is a tool to:

* Bootstrap a Kubernetes cluster
* Configure control plane (master)
* Join worker nodes

👉 It does **NOT** manage workloads — only cluster setup.

---

# 🏗️ 2. Architecture Overview

```
Master Node:
- kube-apiserver
- etcd
- kube-scheduler
- kube-controller-manager

Worker Nodes:
- kubelet
- kube-proxy
- container runtime (Docker/containerd)
```

---

# ⚙️ 3. Prerequisites (ALL NODES)

## 🔹 System Requirements

* Ubuntu 20.04/22.04
* Minimum:

  * Master: 2 CPU, 2GB RAM
  * Worker: 1 CPU, 2GB RAM

---

## 🔹 Disable Swap (IMPORTANT)

```bash
swapoff -a
sed -i '/swap/d' /etc/fstab
```

### 💡 Why?

* Kubernetes scheduler assumes no swap
* Ensures predictable resource allocation

---

## 🔹 Enable Kernel Modules

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
```

```bash
modprobe overlay
modprobe br_netfilter
```

---

## 🔹 Network Settings

```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```

```bash
sysctl --system
```

---

# 🐳 4. Install Container Runtime (containerd)

```bash
apt update
apt install -y containerd
```

### Configure containerd

```bash
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
```

👉 Edit:

```bash
vi /etc/containerd/config.toml
```

Change:

```
SystemdCgroup = true
```

Restart:

```bash
systemctl restart containerd
systemctl enable containerd
```

---

# 📦 5. Install Kubernetes Components

```bash
apt update
apt install -y apt-transport-https curl
```

```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | \
gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```

```bash
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" | \
tee /etc/apt/sources.list.d/kubernetes.list
```

```bash
apt update
apt install -y kubelet kubeadm kubectl
```

```bash
apt-mark hold kubelet kubeadm kubectl
```

---

# 🚀 6. Initialize Master Node

Run ONLY on master:

```bash
kubeadm init --pod-network-cidr=192.168.0.0/16
```

---

## 🔍 What this command does

* Starts control plane components
* Generates certificates
* Creates kubeconfig files
* Starts etcd
* Generates join token

---

## 📁 Files Created (VERY IMPORTANT)

### 🔹 1. kubeconfig files

```
/etc/kubernetes/admin.conf
/etc/kubernetes/kubelet.conf
/etc/kubernetes/controller-manager.conf
/etc/kubernetes/scheduler.conf
```

👉 Used for authentication to API server

---

### 🔹 2. Static Pod Manifests

```
/etc/kubernetes/manifests/
```

Contains:

* kube-apiserver.yaml
* etcd.yaml
* kube-scheduler.yaml
* kube-controller-manager.yaml

👉 These are automatically picked by kubelet

---

### 🔹 3. Certificates

```
/etc/kubernetes/pki/
```

Contains:

* CA certs
* API server certs
* etcd certs

---

### 🔹 4. kubelet config

```
/var/lib/kubelet/config.yaml
```

---

### 🔹 5. etcd data

```
/var/lib/etcd/
```

---

# 🧑‍💻 7. Configure kubectl (Master)

```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```

👉 Now you can run:

```bash
kubectl get nodes
```

---

# 🌐 8. Install Network Plugin (CNI)

Example: Calico

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

👉 Without CNI:

* Pods won’t communicate
* Nodes stay NotReady

---

# 🔗 9. Join Worker Nodes

On master, you get command like:

```bash
kubeadm join <MASTER-IP>:6443 \
--token <TOKEN> \
--discovery-token-ca-cert-hash sha256:<HASH>
```

Run this on BOTH workers.

---

## 🔍 What happens internally?

* Worker registers with API server
* kubelet starts
* Node becomes part of cluster

---

# 📂 10. Important Files on Worker Nodes

### 🔹 kubelet config

```
/var/lib/kubelet/config.yaml
```

### 🔹 certificates

```
/var/lib/kubelet/pki/
```

### 🔹 kube-proxy config

```
/var/lib/kube-proxy/
```

---

# 🔁 11. Verify Cluster

```bash
kubectl get nodes
```

Expected:

```
master     Ready
worker1    Ready
worker2    Ready
```

---

# 🔧 12. Important Commands Explained

## 🔹 kubeadm init

* Initializes control plane
* Generates certs + configs

---

## 🔹 kubeadm join

* Adds worker node
* Uses token-based authentication

---

## 🔹 kubelet

* Runs on every node
* Talks to API server
* Manages pods

---

## 🔹 kubectl

* CLI to interact with cluster

---

## 🔹 kube-proxy

* Handles networking
* Maintains iptables rules

---

# ⚠️ 13. Common Issues

| Issue              | Cause                   | Fix              |
| ------------------ | ----------------------- | ---------------- |
| Node NotReady      | No CNI                  | Install Calico   |
| Swap error         | Swap enabled            | Disable swap     |
| kubeadm init fails | container runtime issue | Check containerd |
| SSL error          | time mismatch           | sync time        |

---

# 🎯 14. Quick Flow Summary

1. Prepare all nodes
2. Install containerd
3. Install kubeadm/kubelet/kubectl
4. Run `kubeadm init` (master)
5. Configure kubectl
6. Install CNI
7. Run `kubeadm join` (workers)

---

# 💡 Interview Tip

👉 **Key line to remember:**

> "kubeadm creates static pod manifests under `/etc/kubernetes/manifests`, which kubelet uses to run control plane components."

---

# 🔄 Follow-up Questions

1. Do you want a **diagram + real-time traffic flow explanation**?
2. Want me to show **how to reset cluster and redo setup**?
3. Want **HA (multi-master) setup instead of single master**?

I can also give you a **real-world DevOps troubleshooting scenario** based on this setup.
