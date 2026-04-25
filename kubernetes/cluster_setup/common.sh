# #!/bin/bash

# set -e

# echo "=== Disable Swap ==="
# swapoff -a
# sed -i '/swap/d' /etc/fstab

# echo "=== Enable Kernel Modules ==="
# cat <<EOF | tee /etc/modules-load.d/k8s.conf
# overlay
# br_netfilter
# EOF

# modprobe overlay
# modprobe br_netfilter

# echo "=== Set Sysctl Params ==="
# cat <<EOF | tee /etc/sysctl.d/k8s.conf
# net.bridge.bridge-nf-call-iptables  = 1
# net.ipv4.ip_forward                 = 1
# net.bridge.bridge-nf-call-ip6tables = 1
# EOF

# sysctl --system

# echo "=== Install containerd ==="
# apt update -y
# apt install -y containerd

# mkdir -p /etc/containerd
# containerd config default > /etc/containerd/config.toml

# sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# systemctl restart containerd
# systemctl enable containerd

# echo "=== Install Kubernetes Tools ==="
# apt install -y apt-transport-https ca-certificates curl

# mkdir -p /etc/apt/keyrings

# curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | \
# gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
# https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" | \
# tee /etc/apt/sources.list.d/kubernetes.list

# apt update -y
# apt install -y kubelet kubeadm kubectl

# apt-mark hold kubelet kubeadm kubectl

# systemctl enable kubelet

# echo "=== Common Setup Completed ==="/


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