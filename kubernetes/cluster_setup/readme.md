Perfect — here’s your **complete, final working setup (ALL scripts + flow)** with **SSL bypass (lab only)** and proper validation.

---

# 🧠 OVERVIEW

You will use 3 scripts:

| Script      | Run Where    | Purpose              |
| ----------- | ------------ | -------------------- |
| `common.sh` | All nodes    | Install dependencies |
| `master.sh` | Master only  | Initialize cluster   |
| `worker.sh` | Worker nodes | Join cluster         |

---

# 📜 1. COMMON SCRIPT (FINAL)

👉 File: `common.sh`

```bash
#!/bin/bash

set -e

echo "=== STEP 1: Disable Swap ==="
swapoff -a
sed -i '/swap/d' /etc/fstab

echo "=== STEP 2: Enable Kernel Modules ==="
cat <<EOF | tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter

echo "=== STEP 3: Set Sysctl Params ==="
cat <<EOF | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sysctl --system

echo "=== STEP 4: Install containerd ==="
apt update -y
apt install -y containerd ca-certificates curl gnupg

mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml

sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

systemctl restart containerd
systemctl enable containerd

echo "=== STEP 5: Configure APT to ignore SSL (LAB ONLY) ==="
echo 'Acquire::https::Verify-Peer "false";' | tee /etc/apt/apt.conf.d/99insecure
echo 'Acquire::https::Verify-Host "false";' | tee -a /etc/apt/apt.conf.d/99insecure

echo "=== STEP 6: Add Kubernetes Repo (SSL BYPASS) ==="

rm -f /etc/apt/keyrings/kubernetes-apt-keyring.gpg
mkdir -p /etc/apt/keyrings

curl -k -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | \
gpg --dearmor --yes -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" | \
tee /etc/apt/sources.list.d/kubernetes.list

echo "=== STEP 7: Install Kubernetes Components ==="

apt update -y
apt install -y kubelet kubeadm kubectl

apt-mark hold kubelet kubeadm kubectl
systemctl enable kubelet

echo "=== STEP 8: VALIDATION ==="

kubeadm version
kubectl version --client
kubelet --version

echo "=== COMMON SETUP COMPLETED SUCCESSFULLY ==="
```

---

# 👑 2. MASTER SCRIPT

👉 File: `master.sh`

```bash
#!/bin/bash

set -e

echo "=== STEP 1: Initialize Kubernetes Master ==="

kubeadm init --pod-network-cidr=192.168.0.0/16 | tee /root/kubeinit.log

echo "=== STEP 2: Configure kubectl ==="

mkdir -p $HOME/.kube
cp /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

echo "=== STEP 3: Install Calico Network Plugin ==="

kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

echo "=== STEP 4: Extract Join Command ==="

grep "kubeadm join" /root/kubeinit.log > /root/join.sh
chmod +x /root/join.sh

echo "=== MASTER SETUP COMPLETE ==="
echo "👉 Copy /root/join.sh to worker nodes"
```

---

# 👷 3. WORKER SCRIPT

👉 File: `worker.sh`

```bash
#!/bin/bash

set -e

echo "=== STEP: Join Kubernetes Cluster ==="

if [ ! -f /root/join.sh ]; then
  echo "❌ join.sh not found. Copy it from master first."
  exit 1
fi

bash /root/join.sh

echo "=== WORKER NODE JOINED SUCCESSFULLY ==="
```

---

# 🧭 EXECUTION FLOW (STEP-BY-STEP)

---

## 🥇 Step 1: Copy scripts to all nodes

```bash
scp common.sh master.sh worker.sh user@node-ip:/home/user/
```

---

## 🥈 Step 2: Run on ALL nodes

```bash
sudo bash common.sh
```

👉 Verify:

```bash
kubeadm version
```

---

## 🥉 Step 3: Run on MASTER

```bash
sudo bash master.sh
```

---

## 📤 Step 4: Copy join script

```bash
scp /root/join.sh user@worker1:/root/
scp /root/join.sh user@worker2:/root/
```

---

## 👷 Step 5: Run on WORKERS

```bash
sudo bash worker.sh
```

---

## ✅ Step 6: Verify cluster

```bash
kubectl get nodes
```

---

# 📁 IMPORTANT FILES CREATED

## 🔹 Master Node

| Path                         | Purpose            |
| ---------------------------- | ------------------ |
| `/etc/kubernetes/admin.conf` | kubectl access     |
| `/etc/kubernetes/manifests/` | control plane pods |
| `/etc/kubernetes/pki/`       | certificates       |
| `/var/lib/etcd/`             | cluster data       |

---

## 🔹 Worker Node

| Path                           | Purpose        |
| ------------------------------ | -------------- |
| `/var/lib/kubelet/config.yaml` | kubelet config |
| `/var/lib/kubelet/pki/`        | certificates   |

---

# ⚠️ COMMON ERRORS

## ❌ kubeadm not found

👉 common.sh failed

---

## ❌ Node NotReady

👉 CNI not installed

---

## ❌ Join failed

```bash
kubeadm token create --print-join-command
```

---

# 🎯 INTERVIEW SUMMARY

👉 Flow:

1. Prepare nodes
2. Install container runtime
3. Install kubeadm tools
4. Initialize master
5. Install CNI
6. Join workers

---

# ⚠️ FINAL WARNING

This setup:

* ❌ Disables SSL verification
* ❌ Not secure
* ✅ Only for learning/lab

---

# 🔄 NEXT STEP (Recommended)

If you want to level up:

* Convert this to **Ansible playbook** (very important)
* Setup **HA multi-master cluster**
* Debug real-world issues (like the SSL one you faced)

Just tell 👍


####################################################################################################
# To re-generate join command, run this on master node

kubeadm token create --print-join-command

Good — this error is actually **very important security behavior from kubeadm** 👇

---

# ❌ Problem

```bash
discovery.bootstrapToken.caCertHashes: Invalid value: ""
```

👉 Your `join.sh` is **missing CA cert hash**

So kubeadm is blocking the join for security reasons.

---

# 🧠 Why This Happened

Your `master.sh` used:

```bash
grep "kubeadm join" /root/kubeinit.log > /root/join.sh
```

👉 Problem:

* The join command is **multi-line**
* `grep` only captured **partial line**
* So `--discovery-token-ca-cert-hash` is missing ❌

---

# ✅ FIX (Best Way)

## 🔧 Regenerate Join Command Properly

Run this on **MASTER**:

```bash
kubeadm token create --print-join-command
```

👉 You’ll get something like:

```bash
kubeadm join <MASTER-IP>:6443 \
--token abcdef.1234567890abcdef \
--discovery-token-ca-cert-hash sha256:xxxxxx
```

---

## 📝 Save it properly

```bash
kubeadm token create --print-join-command > /root/join.sh
chmod +x /root/join.sh
```

---

## 📤 Copy again to workers

```bash
scp /root/join.sh user@worker1:/root/
scp /root/join.sh user@worker2:/root/
```

---

## ▶️ Run on worker

```bash
sudo bash /root/join.sh
```

---

# ⚠️ Quick Hack (Not Recommended but Works)

If you don’t care about security (lab only):

Edit `/root/join.sh`:

```bash
kubeadm join <MASTER-IP>:6443 \
--token <TOKEN> \
--discovery-token-unsafe-skip-ca-verification
```

---

# 🔥 BEST PRACTICE (Fix your master.sh)

Replace this:

```bash
grep "kubeadm join" /root/kubeinit.log > /root/join.sh
```

👉 With this:

```bash
kubeadm token create --print-join-command > /root/join.sh
chmod +x /root/join.sh
```

---

# 🎯 Interview Explanation

👉 If asked:

**Why is CA cert hash required in kubeadm join?**

Answer:

* Ensures worker connects to **trusted API server**
* Prevents **man-in-the-middle attacks**
* Without it, cluster join is unsafe

---

# 🧠 Key Learning

👉 Never parse logs for critical commands
👉 Always use:

```bash
kubeadm token create --print-join-command
```

---

# 🔄 Next Step

After fixing:

```bash
kubectl get nodes
```

---

If nodes still not `Ready`, I can help debug networking (next common issue) 👍



# Azssign role manually in master 
kubectl label node worker1 node-role.kubernetes.io/worker=worker
