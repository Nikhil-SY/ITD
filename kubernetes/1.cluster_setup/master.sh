# #!/bin/bash

# set -e

# echo "=== Initialize Kubernetes Master ==="

# kubeadm init --pod-network-cidr=192.168.0.0/16 | tee /root/kubeinit.log

# echo "=== Setup kubeconfig ==="

# mkdir -p $HOME/.kube
# cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
# chown $(id -u):$(id -g) $HOME/.kube/config

# echo "=== Install Calico Network ==="

# kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# echo "=== Extract Join Command ==="

# grep "kubeadm join" /root/kubeinit.log > /root/join.sh

# chmod +x /root/join.sh

# echo "=== MASTER SETUP COMPLETE ==="
# echo "Run /root/join.sh on worker nodes"



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
echo "👉 Copy /root/join.sh to worker nodes and run it"