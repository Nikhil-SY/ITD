# Amazon EKS — Complete Guide: Scratch to Production-Grade

> **What → Why → How** for every concept. Beginner-friendly analogies + production-grade depth.

---

## Table of Contents

1. [What is EKS?](#1-what-is-eks)
2. [EKS Architecture — Every Component Explained](#2-eks-architecture)
3. [EKS vs Self-Managed Kubernetes](#3-eks-vs-self-managed-kubernetes)
4. [Core EKS Concepts](#4-core-eks-concepts)
   - Node Groups (Managed vs Self-Managed vs Fargate)
   - Control Plane
   - Data Plane
5. [Networking in EKS (VPC CNI)](#5-networking-in-eks)
6. [IAM & Security in EKS](#6-iam--security-in-eks)
   - IRSA (IAM Roles for Service Accounts)
   - aws-auth ConfigMap
   - Pod Identity
7. [Storage in EKS (EBS, EFS, FSx)](#7-storage-in-eks)
8. [Creating an EKS Cluster — 3 Ways](#8-creating-an-eks-cluster)
   - AWS Console
   - AWS CLI + eksctl
   - Terraform
9. [Managed Node Groups — Deep Dive](#9-managed-node-groups)
10. [Cluster Autoscaler — Deep Dive](#10-cluster-autoscaler)
11. [Karpenter — Next-Gen Autoscaling](#11-karpenter)
12. [Load Balancing in EKS (ALB Ingress Controller)](#12-load-balancing-in-eks)
13. [Observability (Logging, Metrics, Tracing)](#13-observability)
14. [EKS Add-ons](#14-eks-add-ons)
15. [EKS Fargate](#15-eks-fargate)
16. [EKS Anywhere & EKS Distro](#16-eks-anywhere--eks-distro)
17. [Upgrading EKS Clusters](#17-upgrading-eks-clusters)
18. [Production Best Practices](#18-production-best-practices)
19. [Cost Optimization](#19-cost-optimization)
20. [Troubleshooting Common Issues](#20-troubleshooting-common-issues)

---

## 1. What is EKS?

### What

**Amazon Elastic Kubernetes Service (EKS)** is a fully managed Kubernetes service provided by AWS. It runs Kubernetes for you — meaning AWS takes care of installing, operating, patching, and scaling the Kubernetes **control plane** (the "brain" of the cluster).

### Why

Running Kubernetes yourself is hard. You need to:
- Install and configure `etcd` (the database), `kube-apiserver`, `kube-scheduler`, `kube-controller-manager`
- Handle HA (high availability) across 3+ masters
- Patch them for CVEs regularly
- Back up `etcd`
- Handle control plane failures

EKS eliminates all of this. AWS manages the control plane. You only manage your worker nodes (where your containers actually run).

### Analogy

Think of Kubernetes like a **restaurant kitchen**:
- The **control plane** = the head chef and restaurant manager (decides what to cook, assigns tasks, keeps inventory)
- The **worker nodes** = the line cooks (actually prepare the food)

With **self-managed Kubernetes**, you hire and manage your own head chef.  
With **EKS**, AWS provides and guarantees the head chef — you only manage the line cooks.

### Key Facts

| Property | Value |
|----------|-------|
| Kubernetes versions supported | N-2 (e.g., 1.28, 1.29, 1.30) |
| Control plane SLA | 99.95% uptime |
| Control plane cost | $0.10/hour per cluster (~$73/month) |
| First released | June 2018 |
| Regions | All major AWS regions |

---

## 2. EKS Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR AWS ACCOUNT                             │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              AWS MANAGED CONTROL PLANE (Hidden VPC)          │   │
│  │                                                              │   │
│  │   ┌─────────────────┐   ┌──────────────────────────────┐   │   │
│  │   │  kube-apiserver  │   │      etcd (HA across 3 AZs)  │   │   │
│  │   │  (HA, 3 replicas)│   │      (encrypted at rest)     │   │   │
│  │   └────────┬─────────┘   └──────────────────────────────┘   │   │
│  │            │              ┌──────────────────────────────┐   │   │
│  │            │              │  kube-scheduler              │   │   │
│  │            │              │  kube-controller-manager     │   │   │
│  │            │              │  cloud-controller-manager    │   │   │
│  │            │              └──────────────────────────────┘   │   │
│  └────────────┼─────────────────────────────────────────────────┘   │
│               │  (EKS Endpoint - Public or Private)                 │
│               │                                                     │
│  ┌────────────┼────────────────────────────────────────────────┐   │
│  │  YOUR VPC  │                                                 │   │
│  │            ▼                                                 │   │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │   │
│  │   │  Worker Node │  │  Worker Node │  │  Worker Node │     │   │
│  │   │  (EC2)       │  │  (EC2)       │  │  (EC2)       │     │   │
│  │   │              │  │              │  │              │     │   │
│  │   │  kubelet     │  │  kubelet     │  │  kubelet     │     │   │
│  │   │  kube-proxy  │  │  kube-proxy  │  │  kube-proxy  │     │   │
│  │   │  containerd  │  │  containerd  │  │  containerd  │     │   │
│  │   │              │  │              │  │              │     │   │
│  │   │  [Pod] [Pod] │  │  [Pod] [Pod] │  │  [Pod] [Pod] │     │   │
│  │   └──────────────┘  └──────────────┘  └──────────────┘     │   │
│  │        AZ-1               AZ-2               AZ-3           │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Control Plane Components (AWS-managed)

| Component | Role |
|-----------|------|
| `kube-apiserver` | The front door — all kubectl commands go here |
| `etcd` | The database — stores ALL cluster state (HA, encrypted) |
| `kube-scheduler` | Decides which node each pod runs on |
| `kube-controller-manager` | Watches cluster state, reconciles desired vs actual |
| `cloud-controller-manager` | AWS-specific — provisions ELBs, EBS volumes, etc. |

### Data Plane Components (Your EC2 nodes)

| Component | Role |
|-----------|------|
| `kubelet` | Agent on each node — takes pod specs from API server and runs them |
| `kube-proxy` | Manages network rules (iptables/IPVS) for Service routing |
| `containerd` | Container runtime — actually pulls images and runs containers |
| `aws-node` (VPC CNI) | AWS networking plugin — assigns VPC IPs to pods |

---

## 3. EKS vs Self-Managed Kubernetes

| Responsibility | Self-Managed | EKS |
|----------------|-------------|-----|
| Control plane install | You | AWS |
| Control plane HA | You | AWS |
| Control plane patching | You | AWS |
| etcd backups | You | AWS |
| Worker node provisioning | You | You (or AWS for Fargate) |
| Worker node patching | You | You (or AWS for Managed Node Groups) |
| Kubernetes upgrades | You | Triggered by you, managed by AWS |
| Cluster autoscaling | You | You (Cluster Autoscaler or Karpenter) |

**Bottom line**: EKS is NOT fully managed (unlike ECS Fargate). You still own worker nodes. AWS owns the control plane.

---

## 4. Core EKS Concepts

### Node Groups

A **Node Group** is a collection of EC2 instances (worker nodes) that share the same configuration (instance type, AMI, IAM role, labels, taints).

#### Types of Node Groups

```
EKS Worker Nodes
├── Managed Node Groups     ← AWS-managed EC2 lifecycle
├── Self-Managed Node Groups ← You manage EC2 lifecycle yourself
└── Fargate Profiles        ← Serverless (no EC2 at all)
```

#### Managed Node Groups (MNG)
- AWS provisions, registers, and drains EC2s automatically
- Backed by Auto Scaling Groups (ASG)
- Supports rolling updates for node version upgrades
- Uses EKS-optimized AMIs (maintained by AWS)

#### Self-Managed Node Groups
- You create and manage the ASG yourself
- You manage AMI updates
- More flexibility (spot instances via mixed instance policies, custom AMIs)
- More operational burden

#### Fargate
- No EC2 instances at all
- Each pod gets its own micro-VM
- Only pay per pod (vCPU + memory per second)
- No access to node-level features (DaemonSets don't work on Fargate)

---

## 5. Networking in EKS

### Amazon VPC CNI Plugin

**What**: EKS uses `aws-node` (Amazon VPC CNI) as the network plugin. Every pod gets a **real VPC IP address** — not an overlay network IP.

**Why this is different**: Most Kubernetes clusters use overlay networks (Flannel, Calico) where pods get virtual IPs. AWS VPC CNI assigns actual ENI (Elastic Network Interface) secondary IPs to pods.

**How it works**:

```
EC2 Instance (m5.large = 3 ENIs × 10 IPs = 30 pods max)
├── Primary ENI
│   ├── Primary IP: 10.0.1.10 (node IP)
│   ├── Secondary IP: 10.0.1.11 → Pod A
│   └── Secondary IP: 10.0.1.12 → Pod B
├── Secondary ENI
│   ├── Secondary IP: 10.0.1.13 → Pod C
│   └── Secondary IP: 10.0.1.14 → Pod D
└── Tertiary ENI
    └── ...
```

### Pod Density Limits

Each EC2 instance type has a max pod count based on ENI limits:

```bash
# Formula:
# Max Pods = (Number of ENIs × (IPs per ENI - 1)) + 2

# m5.large: 3 ENIs × 10 IPs = 29 pods
# m5.xlarge: 4 ENIs × 15 IPs = 58 pods
# m5.4xlarge: 8 ENIs × 30 IPs = 234 pods
```

### VPC CNI with Prefix Delegation (More Pods)

AWS supports **prefix delegation** which assigns /28 CIDR blocks (16 IPs) per ENI slot instead of individual IPs:

```bash
# Enable prefix delegation
kubectl set env daemonset aws-node \
  ENABLE_PREFIX_DELEGATION=true \
  -n kube-system

# m5.large with prefix delegation: 3 ENIs × 10 prefixes × 16 IPs = 480 pods!
```

### EKS Cluster Endpoint Modes

```
Public Endpoint (default):
  kubectl → Internet → AWS-managed EKS endpoint → Control Plane
  Worker nodes → Internet (or NAT GW) → Control Plane

Private Endpoint:
  kubectl → VPN/Direct Connect → EKS Private Endpoint in your VPC
  Worker nodes → Private endpoint (no NAT GW needed)

Public + Private (recommended for production):
  kubectl from office → Public endpoint
  Worker nodes → Private endpoint (stays within VPC)
```

---

## 6. IAM & Security in EKS

### How Auth Works in EKS

EKS uses **AWS IAM for authentication** and **Kubernetes RBAC for authorization**.

```
User runs: kubectl get pods
    ↓
kubectl sends request to EKS API server
    ↓
API server calls aws-iam-authenticator to verify IAM identity
    ↓
IAM identity mapped to Kubernetes user/group via aws-auth ConfigMap
    ↓
Kubernetes RBAC checks if that user/group has permission
    ↓
Response returned
```

### aws-auth ConfigMap

The `aws-auth` ConfigMap maps IAM roles/users to Kubernetes users/groups:

```yaml
# kubectl edit configmap aws-auth -n kube-system
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    # Worker nodes role — REQUIRED for nodes to join the cluster
    - rolearn: arn:aws:iam::123456789012:role/eks-node-role
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes

    # Developer role — read-only access
    - rolearn: arn:aws:iam::123456789012:role/developer-role
      username: developer
      groups:
        - dev-readonly

    # Admin role — cluster admin
    - rolearn: arn:aws:iam::123456789012:role/eks-admin-role
      username: eks-admin
      groups:
        - system:masters

  mapUsers: |
    # Direct IAM user mapping
    - userarn: arn:aws:iam::123456789012:user/alice
      username: alice
      groups:
        - system:masters
```

### IRSA — IAM Roles for Service Accounts

**What**: IRSA lets Kubernetes pods assume AWS IAM roles **without any credentials in the pod**. No access keys, no secrets.

**Why**: Before IRSA, pods used the EC2 instance's IAM role — meaning ALL pods on a node had the same AWS permissions. IRSA gives per-pod AWS permissions.

**How it works**:

```
Pod with IRSA:
1. Pod has a ServiceAccount annotated with an IAM role ARN
2. EKS injects AWS_WEB_IDENTITY_TOKEN_FILE env var into the pod
3. AWS SDK reads that token and calls STS AssumeRoleWithWebIdentity
4. STS verifies token against EKS OIDC provider
5. STS returns temporary credentials
6. Pod uses those credentials to call AWS APIs

No hard-coded credentials anywhere!
```

**Setup**:

```bash
# Step 1: Get OIDC provider URL for your cluster
aws eks describe-cluster --name my-cluster \
  --query "cluster.identity.oidc.issuer" --output text

# Step 2: Create OIDC identity provider in IAM
eksctl utils associate-iam-oidc-provider \
  --cluster my-cluster --approve

# Step 3: Create IAM policy
cat > s3-read-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
  }]
}
EOF
aws iam create-policy \
  --policy-name S3ReadPolicy \
  --policy-document file://s3-read-policy.json

# Step 4: Create IAM Role with trust policy for the ServiceAccount
eksctl create iamserviceaccount \
  --cluster my-cluster \
  --namespace default \
  --name s3-reader-sa \
  --attach-policy-arn arn:aws:iam::123456789012:policy/S3ReadPolicy \
  --approve
```

```yaml
# The ServiceAccount created by eksctl looks like this:
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-reader-sa
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/s3-reader-role

---
# Use it in a Pod
apiVersion: v1
kind: Pod
metadata:
  name: s3-reader-pod
spec:
  serviceAccountName: s3-reader-sa   # ← IRSA kicks in here
  containers:
  - name: app
    image: amazon/aws-cli
    command: ["aws", "s3", "ls", "s3://my-bucket"]
```

### Node IAM Role (Required Policies)

Every worker node needs these IAM policies:

```
AmazonEKSWorkerNodePolicy        — Join the cluster, describe nodes
AmazonEC2ContainerRegistryReadOnly — Pull images from ECR
AmazonEKS_CNI_Policy            — Manage VPC networking (ENIs, IPs)
```

---

## 7. Storage in EKS

### EBS CSI Driver

The EBS CSI Driver allows pods to use EBS volumes as persistent storage.

```bash
# Install EBS CSI Driver as EKS add-on
aws eks create-addon \
  --cluster-name my-cluster \
  --addon-name aws-ebs-csi-driver \
  --service-account-role-arn arn:aws:iam::123456789012:role/ebs-csi-role
```

```yaml
# StorageClass for GP3 volumes
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer   # ← Crucial for multi-AZ!
reclaimPolicy: Retain

---
# PVC using this StorageClass
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: gp3
  resources:
    requests:
      storage: 20Gi
```

**Important**: EBS volumes are AZ-scoped. `WaitForFirstConsumer` ensures the volume is created in the same AZ as the pod that claims it.

### EFS CSI Driver (Shared Storage)

EFS provides ReadWriteMany — multiple pods across nodes can mount the same volume simultaneously.

```yaml
# StorageClass for EFS
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: efs-sc
provisioner: efs.csi.aws.com
parameters:
  provisioningMode: efs-ap
  fileSystemId: fs-0123456789abcdef
  directoryPerms: "700"
```

---

## 8. Creating an EKS Cluster

### Method 1: AWS Console

```
Step 1: Open EKS Console → "Create cluster"

Step 2: Cluster Configuration
  ├── Name: production-cluster
  ├── Kubernetes version: 1.30
  └── Cluster service role: eks-cluster-role
      (needs AmazonEKSClusterPolicy attached)

Step 3: Networking
  ├── VPC: your-production-vpc
  ├── Subnets: private-subnet-1a, private-subnet-1b, private-subnet-1c
  ├── Security groups: (optional additional SGs)
  └── Cluster endpoint access: Public and private

Step 4: Logging (optional but recommended for production)
  ├── API server logs    ✓
  ├── Audit logs         ✓
  ├── Authenticator logs ✓
  ├── Controller logs    ✓
  └── Scheduler logs     ✓

Step 5: Add-ons
  ├── kube-proxy (required)
  ├── CoreDNS (required)
  ├── Amazon VPC CNI (required)
  └── EBS CSI Driver (recommended)

Step 6: Review and Create
  → Control plane takes ~10-15 minutes to provision

Step 7: Add Node Group
  ├── Node group name: production-nodes
  ├── Node IAM role: eks-node-role
  ├── AMI type: Amazon Linux 2 (AL2_x86_64)
  ├── Instance type: m5.large
  ├── Disk size: 50 GiB
  ├── Scaling config: Min=2, Desired=3, Max=10
  └── Subnets: private subnets only

Step 8: Update kubeconfig
  aws eks update-kubeconfig --name production-cluster --region us-east-1
```

---

### Method 2: eksctl (Recommended for Quick Setup)

`eksctl` is the official CLI tool for EKS — think of it as `kubectl` but for cluster management.

```bash
# Install eksctl
curl --silent --location \
  "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | \
  tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Verify
eksctl version
```

#### Simple cluster creation

```bash
eksctl create cluster \
  --name production-cluster \
  --region us-east-1 \
  --version 1.30 \
  --nodegroup-name production-nodes \
  --node-type m5.large \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5 \
  --managed
```

#### Production-grade cluster via config file

```yaml
# cluster-config.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: production-cluster
  region: us-east-1
  version: "1.30"
  tags:
    Environment: production
    Team: platform

# Use existing VPC (recommended for production)
vpc:
  id: vpc-0abc123
  subnets:
    private:
      us-east-1a: { id: subnet-0aaa111 }
      us-east-1b: { id: subnet-0bbb222 }
      us-east-1c: { id: subnet-0ccc333 }
    public:
      us-east-1a: { id: subnet-0pub111 }
      us-east-1b: { id: subnet-0pub222 }
      us-east-1c: { id: subnet-0pub333 }
  clusterEndpoints:
    publicAccess:  true
    privateAccess: true

# IAM OIDC provider (required for IRSA)
iam:
  withOIDC: true
  serviceAccounts:
    - metadata:
        name: aws-load-balancer-controller
        namespace: kube-system
      wellKnownPolicies:
        awsLoadBalancerController: true
    - metadata:
        name: cluster-autoscaler
        namespace: kube-system
      wellKnownPolicies:
        autoScaler: true
    - metadata:
        name: ebs-csi-controller-sa
        namespace: kube-system
      wellKnownPolicies:
        ebsCSIController: true

# Managed Node Groups
managedNodeGroups:
  # On-demand nodes for critical workloads
  - name: on-demand-nodes
    instanceType: m5.xlarge
    minSize: 2
    desiredCapacity: 3
    maxSize: 10
    privateNetworking: true          # Place in private subnets
    availabilityZones:
      - us-east-1a
      - us-east-1b
      - us-east-1c
    labels:
      role: general
      lifecycle: on-demand
    taints:
      - key: dedicated
        value: "false"
        effect: NoSchedule
    tags:
      k8s.io/cluster-autoscaler/enabled: "true"
      k8s.io/cluster-autoscaler/production-cluster: "owned"
    iam:
      attachPolicyARNs:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
    updateConfig:
      maxUnavailable: 1
    amiFamily: AmazonLinux2
    volumeSize: 50
    volumeType: gp3
    volumeEncrypted: true
    ssh:
      enableSsm: true              # SSM access instead of SSH keys

  # Spot instances for batch/non-critical workloads
  - name: spot-nodes
    instanceTypes:
      - m5.xlarge
      - m5a.xlarge
      - m4.xlarge
      - m5d.xlarge
    minSize: 0
    desiredCapacity: 2
    maxSize: 20
    privateNetworking: true
    spot: true
    labels:
      role: spot
      lifecycle: spot
    taints:
      - key: spot
        value: "true"
        effect: NoSchedule
    tags:
      k8s.io/cluster-autoscaler/enabled: "true"
      k8s.io/cluster-autoscaler/production-cluster: "owned"

# Control plane logging
cloudWatch:
  clusterLogging:
    enableTypes:
      - api
      - audit
      - authenticator
      - controllerManager
      - scheduler

# EKS Add-ons
addons:
  - name: vpc-cni
    version: latest
    resolveConflicts: overwrite
    configurationValues: '{"env":{"ENABLE_PREFIX_DELEGATION":"true"}}'
  - name: coredns
    version: latest
  - name: kube-proxy
    version: latest
  - name: aws-ebs-csi-driver
    version: latest
    wellKnownPolicies:
      ebsCSIController: true
```

```bash
# Apply the config
eksctl create cluster -f cluster-config.yaml

# Check nodes
kubectl get nodes -o wide

# Expected output:
# NAME                          STATUS   ROLES    AGE   VERSION   INTERNAL-IP
# ip-10-0-1-10.ec2.internal    Ready    <none>   5m    v1.30.0   10.0.1.10
# ip-10-0-2-20.ec2.internal    Ready    <none>   5m    v1.30.0   10.0.2.20
# ip-10-0-3-30.ec2.internal    Ready    <none>   5m    v1.30.0   10.0.3.30
```

---

### Method 3: Terraform (Production-Grade IaC)

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "eks/production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region
}

# Configure Kubernetes provider using EKS cluster output
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}
```

```hcl
# variables.tf
variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "production-cluster"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.30"
}

variable "vpc_id" {
  description = "VPC ID for EKS cluster"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for worker nodes"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for load balancers"
  type        = list(string)
}
```

```hcl
# iam.tf

# ─── EKS Cluster IAM Role ───
resource "aws_iam_role" "cluster" {
  name = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}

# ─── Node Group IAM Role ───
resource "aws_iam_role" "node_group" {
  name = "${var.cluster_name}-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "node_worker" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_ecr" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_cni" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_group.name
}

# ─── OIDC Provider for IRSA ───
data "tls_certificate" "eks" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer
}
```

```hcl
# eks.tf

# ─── Security Group for Control Plane ───
resource "aws_security_group" "cluster" {
  name        = "${var.cluster_name}-cluster-sg"
  description = "EKS cluster control plane security group"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.cluster_name}-cluster-sg"
  }
}

# ─── EKS Cluster ───
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  version  = var.cluster_version
  role_arn = aws_iam_role.cluster.arn

  vpc_config {
    subnet_ids              = concat(var.private_subnet_ids, var.public_subnet_ids)
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["YOUR_OFFICE_IP/32"]  # Restrict public access!
    security_group_ids      = [aws_security_group.cluster.id]
  }

  # Enable all control plane logs
  enabled_cluster_log_types = [
    "api", "audit", "authenticator", "controllerManager", "scheduler"
  ]

  encryption_config {
    resources = ["secrets"]
    provider {
      key_arn = aws_kms_key.eks.arn
    }
  }

  tags = {
    Name        = var.cluster_name
    Environment = "production"
  }

  depends_on = [aws_iam_role_policy_attachment.cluster_policy]
}

# KMS key for secret encryption
resource "aws_kms_key" "eks" {
  description             = "EKS Secret Encryption Key"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}

# ─── Managed Node Group: On-Demand ───
resource "aws_eks_node_group" "on_demand" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "on-demand"
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.private_subnet_ids

  ami_type       = "AL2_x86_64"
  capacity_type  = "ON_DEMAND"
  instance_types = ["m5.xlarge"]
  disk_size      = 50

  scaling_config {
    desired_size = 3
    min_size     = 2
    max_size     = 10
  }

  update_config {
    max_unavailable = 1
  }

  labels = {
    role      = "general"
    lifecycle = "on-demand"
  }

  # Enable SSM access
  remote_access {
    ec2_ssh_key               = null  # No SSH key - use SSM
    source_security_group_ids = []
  }

  tags = {
    "k8s.io/cluster-autoscaler/enabled"                     = "true"
    "k8s.io/cluster-autoscaler/${var.cluster_name}"         = "owned"
    "kubernetes.io/cluster/${var.cluster_name}"             = "owned"
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_worker,
    aws_iam_role_policy_attachment.node_ecr,
    aws_iam_role_policy_attachment.node_cni,
  ]
}

# ─── Managed Node Group: Spot ───
resource "aws_eks_node_group" "spot" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "spot"
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.private_subnet_ids

  ami_type      = "AL2_x86_64"
  capacity_type = "SPOT"

  # Multiple instance types for spot diversity
  instance_types = [
    "m5.xlarge", "m5a.xlarge", "m4.xlarge",
    "m5d.xlarge", "m5n.xlarge"
  ]

  disk_size = 50

  scaling_config {
    desired_size = 2
    min_size     = 0
    max_size     = 20
  }

  update_config {
    max_unavailable = 2
  }

  labels = {
    role      = "spot"
    lifecycle = "spot"
  }

  taint {
    key    = "spot"
    value  = "true"
    effect = "NO_SCHEDULE"
  }

  tags = {
    "k8s.io/cluster-autoscaler/enabled"             = "true"
    "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned"
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_worker,
    aws_iam_role_policy_attachment.node_ecr,
    aws_iam_role_policy_attachment.node_cni,
  ]
}

# ─── EKS Add-ons ───
resource "aws_eks_addon" "vpc_cni" {
  cluster_name             = aws_eks_cluster.main.name
  addon_name               = "vpc-cni"
  addon_version            = data.aws_eks_addon_version.vpc_cni.version
  resolve_conflicts_on_update = "OVERWRITE"
  configuration_values = jsonencode({
    env = {
      ENABLE_PREFIX_DELEGATION = "true"
    }
  })
}

resource "aws_eks_addon" "coredns" {
  cluster_name             = aws_eks_cluster.main.name
  addon_name               = "coredns"
  addon_version            = data.aws_eks_addon_version.coredns.version
  resolve_conflicts_on_update = "OVERWRITE"
  depends_on               = [aws_eks_node_group.on_demand]
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name             = aws_eks_cluster.main.name
  addon_name               = "kube-proxy"
  addon_version            = data.aws_eks_addon_version.kube_proxy.version
  resolve_conflicts_on_update = "OVERWRITE"
}

resource "aws_eks_addon" "ebs_csi" {
  cluster_name             = aws_eks_cluster.main.name
  addon_name               = "aws-ebs-csi-driver"
  addon_version            = data.aws_eks_addon_version.ebs_csi.version
  service_account_role_arn = aws_iam_role.ebs_csi.arn
  resolve_conflicts_on_update = "OVERWRITE"
}

data "aws_eks_addon_version" "vpc_cni" {
  addon_name         = "vpc-cni"
  kubernetes_version = aws_eks_cluster.main.version
  most_recent        = true
}

data "aws_eks_addon_version" "coredns" {
  addon_name         = "coredns"
  kubernetes_version = aws_eks_cluster.main.version
  most_recent        = true
}

data "aws_eks_addon_version" "kube_proxy" {
  addon_name         = "kube-proxy"
  kubernetes_version = aws_eks_cluster.main.version
  most_recent        = true
}

data "aws_eks_addon_version" "ebs_csi" {
  addon_name         = "aws-ebs-csi-driver"
  kubernetes_version = aws_eks_cluster.main.version
  most_recent        = true
}
```

```hcl
# outputs.tf
output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "cluster_name" {
  value = aws_eks_cluster.main.name
}

output "cluster_certificate_authority_data" {
  value = aws_eks_cluster.main.certificate_authority[0].data
}

output "oidc_provider_arn" {
  value = aws_iam_openid_connect_provider.eks.arn
}
```

```bash
# Deploy
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Update kubeconfig
aws eks update-kubeconfig \
  --name production-cluster \
  --region us-east-1

# Verify
kubectl get nodes
kubectl get pods -A
```

---

## 9. Managed Node Groups — Deep Dive

### What

A Managed Node Group (MNG) is an AWS-managed group of EC2 instances that form the worker nodes of your EKS cluster. AWS handles the lifecycle of these nodes.

### What AWS Does for You in MNG

```
You request: "Upgrade node group from k8s 1.29 to 1.30"

AWS does:
  1. Provisions a new EC2 with new AMI (1.30)
  2. Registers it with the cluster
  3. Cordons the old node (marks it unschedulable)
  4. Drains it (evicts all pods gracefully)
  5. Waits for pods to reschedule on other nodes
  6. Terminates the old node
  7. Repeats for each node (respecting maxUnavailable)
```

### MNG Lifecycle Flow

```
Desired state change (scale up / upgrade) detected
          ↓
AWS creates new EC2 instance
          ↓
EC2 user-data script runs:
  - Installs kubelet, containerd
  - Configures kubelet with cluster endpoint/CA
  - kubelet registers with API server
          ↓
Node appears as "NotReady" (CNI not yet configured)
          ↓
aws-node (VPC CNI) daemonset starts on node
  - Attaches ENIs
  - Pre-allocates IP addresses
          ↓
Node transitions to "Ready"
          ↓
Scheduler places pending pods on node
```

### Node Group Update Strategies

```yaml
# Rolling update (default) — safer
updateConfig:
  maxUnavailable: 1         # Only 1 node down at a time

# Faster update — more risk
updateConfig:
  maxUnavailablePercentage: 33  # Up to 33% nodes down at once
```

### MNG vs Self-Managed: When to Use What

| Use Case | MNG | Self-Managed |
|----------|-----|-------------|
| Standard workloads | ✅ Recommended | Overkill |
| Custom AMI needed | ❌ Limited | ✅ Full control |
| Mixed instance types with complex ASG | ⚠️ Limited | ✅ Full control |
| Auto-patching desired | ✅ AWS handles | ❌ Manual |
| Bottlerocket OS | ✅ Supported | ✅ Supported |

### EKS-Optimized AMIs

AWS provides pre-built AMIs for EKS that include:
- Specific kernel version optimized for containers
- containerd as the container runtime
- kubelet configured correctly
- `bootstrap.sh` to join the cluster

```bash
# Get latest EKS-optimized AMI ID for 1.30 in us-east-1
aws ssm get-parameter \
  --name /aws/service/eks/optimized-ami/1.30/amazon-linux-2/recommended/image_id \
  --query "Parameter.Value" --output text

# For ARM (Graviton):
aws ssm get-parameter \
  --name /aws/service/eks/optimized-ami/1.30/amazon-linux-2-arm64/recommended/image_id \
  --query "Parameter.Value" --output text
```

---

## 10. Cluster Autoscaler — Deep Dive

### What

The **Cluster Autoscaler (CA)** is a Kubernetes component that **automatically adjusts the number of nodes** in your cluster based on pod scheduling needs.

### Why

Imagine you have 3 nodes and 10 pods running. Suddenly you need 20 pods (traffic spike). Without CA:
- 10 new pods stay in `Pending` state (no node has room)
- You manually add more nodes
- Latency/errors while pods are pending

With CA:
- CA detects `Pending` pods
- CA tells AWS ASG to add more nodes
- Pods get scheduled automatically

Similarly, CA removes nodes when they're underutilized to save cost.

### How Cluster Autoscaler Works (Detailed)

```
Scale-UP Flow:
─────────────
Pod becomes Pending (no node has enough resources)
          ↓
CA loop runs every 10 seconds
          ↓
CA calls Kubernetes Scheduler Simulator:
  "If I added a node from NodeGroup X, would this pod schedule?"
          ↓
If yes: CA calls AWS ASG API to increase DesiredCapacity by N
          ↓
ASG launches new EC2
          ↓
EC2 boots, joins cluster (~2-3 minutes)
          ↓
Pod schedules on new node

Scale-DOWN Flow:
────────────────
CA checks all nodes every 10 seconds
          ↓
If a node's requested resources < 50% (default threshold)
  AND all pods on it can be moved elsewhere
  AND node has been underutilized for 10+ minutes
          ↓
CA cordons the node
          ↓
CA evicts pods (respecting PodDisruptionBudgets)
          ↓
Pods reschedule on other nodes
          ↓
CA calls ASG to decrease DesiredCapacity
          ↓
EC2 terminates (after 10 min scale-down delay by default)
```

### Critical: Node Group Tagging (Required for CA)

CA discovers node groups via ASG tags:

```
k8s.io/cluster-autoscaler/enabled = true
k8s.io/cluster-autoscaler/<cluster-name> = owned
```

Without these tags, CA won't manage the node group.

### Installing Cluster Autoscaler

```bash
# Step 1: Create IAM Policy for Cluster Autoscaler
cat > cluster-autoscaler-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeScalingActivities",
        "autoscaling:DescribeTags",
        "ec2:DescribeImages",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:GetInstanceTypesFromInstanceRequirements",
        "eks:DescribeNodegroup"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Resource": ["*"]
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name ClusterAutoscalerPolicy \
  --policy-document file://cluster-autoscaler-policy.json

# Step 2: Create IRSA for Cluster Autoscaler
eksctl create iamserviceaccount \
  --cluster production-cluster \
  --namespace kube-system \
  --name cluster-autoscaler \
  --attach-policy-arn arn:aws:iam::123456789012:policy/ClusterAutoscalerPolicy \
  --override-existing-serviceaccounts \
  --approve
```

```yaml
# cluster-autoscaler.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    app: cluster-autoscaler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8085"
    spec:
      serviceAccountName: cluster-autoscaler   # IRSA ServiceAccount
      priorityClassName: system-cluster-critical

      # Run on on-demand nodes only (not spot)
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: lifecycle
                operator: In
                values: [on-demand]

      containers:
      - name: cluster-autoscaler
        image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.30.0
        resources:
          requests:
            cpu: 100m
            memory: 600Mi
          limits:
            cpu: 100m
            memory: 600Mi
        command:
          - ./cluster-autoscaler
          - --v=4
          - --stderrthreshold=info
          - --cloud-provider=aws
          - --skip-nodes-with-local-storage=false
          - --expander=least-waste    # ← Scale up smallest node that fits
          - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled=true,k8s.io/cluster-autoscaler/production-cluster=owned
          - --balance-similar-node-groups
          - --skip-nodes-with-system-pods=false

          # Scale-down tuning
          - --scale-down-enabled=true
          - --scale-down-delay-after-add=10m      # Wait 10m after scale-up before scale-down
          - --scale-down-unneeded-time=10m        # Node must be unneeded for 10m before removal
          - --scale-down-utilization-threshold=0.5  # Remove if < 50% utilized

        env:
        - name: AWS_REGION
          value: us-east-1
        volumeMounts:
        - name: ssl-certs
          mountPath: /etc/ssl/certs/ca-certificates.crt
          readOnly: true

      volumes:
      - name: ssl-certs
        hostPath:
          path: "/etc/ssl/certs/ca-bundle.crt"
```

```bash
kubectl apply -f cluster-autoscaler.yaml

# Verify CA is running
kubectl get pods -n kube-system | grep cluster-autoscaler

# Watch CA logs
kubectl logs -n kube-system -l app=cluster-autoscaler -f
```

### CA Expanders — How CA Chooses Which Node Group to Scale

When multiple node groups could accommodate a pending pod, the **expander** decides:

| Expander | Behavior | Use Case |
|----------|----------|----------|
| `least-waste` | Pick node group with least leftover resources | Resource efficiency |
| `most-pods` | Pick group that schedules the most pending pods | Reduce # of scale-ups |
| `random` | Random selection | Testing |
| `price` | Pick cheapest option (requires pricing config) | Cost optimization |
| `priority` | User-defined priority list | Full control |

### CA Annotations — Fine-Tuning Per Node/Pod

```yaml
# Prevent a specific pod from triggering scale-up
metadata:
  annotations:
    cluster-autoscaler.kubernetes.io/safe-to-evict: "true"

# Prevent a node from being scaled down (e.g., stateful node)
# Label the node:
kubectl annotate node <node-name> \
  cluster-autoscaler.kubernetes.io/scale-down-disabled=true
```

### PodDisruptionBudget — Protecting Apps During Scale-Down

```yaml
# Ensure at least 2 replicas are always available during CA scale-down
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2     # OR: maxUnavailable: 1
  selector:
    matchLabels:
      app: my-app
```

CA **respects PDBs** — it won't evict pods if doing so would violate the PDB.

### CA Limitations and Edge Cases

```
❌ CA does NOT scale down nodes with:
  - Pods with local storage (emptyDir)
  - Pods with restrictive PDBs
  - DaemonSet pods (they don't count)
  - Pods with "safe-to-evict: false" annotation
  - Pods not managed by a controller (bare pods)

❌ CA scale-up has ~2-3 min latency (EC2 boot time)

❌ CA doesn't handle CPU/memory pressure on existing nodes
   (that's HPA's job — CA only handles node count)
```

---

## 11. Karpenter — Next-Gen Autoscaling

### What

**Karpenter** is a newer, more powerful node provisioner that **replaces Cluster Autoscaler** for most use cases. It was open-sourced by AWS.

### Karpenter vs Cluster Autoscaler

| Feature | Cluster Autoscaler | Karpenter |
|---------|-------------------|-----------|
| Works with | Pre-defined ASG node groups | Any EC2 instance type |
| Provisioning speed | 2-3 min (ASG) | ~60 seconds |
| Instance selection | Fixed instance type per group | Optimal instance per workload |
| Spot handling | Manual configuration | Automatic disruption handling |
| Bin packing | Basic | Advanced |
| Node consolidation | Basic scale-down | Aggressive consolidation |

### Karpenter Core Concepts

```
NodePool: Defines what types of nodes Karpenter can provision
  ├── Instance families (m5, c5, r5...)
  ├── Capacity types (on-demand, spot)
  ├── Resource limits (max total CPU/memory in cluster)
  └── Disruption settings (when to consolidate)

EC2NodeClass: AWS-specific config for nodes
  ├── AMI selection
  ├── Subnet selection
  ├── Security groups
  └── IAM instance profile
```

```yaml
# NodePool — what Karpenter can provision
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    metadata:
      labels:
        managed-by: karpenter
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default

      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["m5", "m5a", "m4", "c5", "r5"]
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["large", "xlarge", "2xlarge"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]

      # Node expiry — forces node replacement (for AMI updates)
      expireAfter: 720h  # 30 days

  limits:
    cpu: "1000"
    memory: 1000Gi

  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s

---
# EC2NodeClass — AWS-specific settings
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiSelectorTerms:
    - alias: al2023@latest   # Auto-select latest EKS-optimized AL2023 AMI

  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: production-cluster

  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: production-cluster

  instanceProfile: "KarpenterNodeInstanceProfile-production-cluster"

  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 50Gi
        volumeType: gp3
        encrypted: true
```

---

## 12. Load Balancing in EKS

### AWS Load Balancer Controller

The **AWS Load Balancer Controller** provisions ALBs (Application Load Balancers) and NLBs (Network Load Balancers) directly from Kubernetes Ingress and Service objects.

```bash
# Install AWS Load Balancer Controller via Helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=production-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

```yaml
# Ingress — provisions an ALB
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip    # Route directly to pods (bypass NodePort)
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:123456789012:certificate/xxx
    alb.ingress.kubernetes.io/ssl-redirect: "443"
    alb.ingress.kubernetes.io/healthcheck-path: /healthz
    alb.ingress.kubernetes.io/group.name: production  # Share ALB across multiple Ingresses
spec:
  rules:
  - host: api.myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-api-service
            port:
              number: 80
  - host: admin.myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: admin-service
            port:
              number: 80
```

---

## 13. Observability

### Control Plane Logs → CloudWatch

```bash
# Enable all log types
aws eks update-cluster-config \
  --name production-cluster \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# View logs in CloudWatch
# Log Group: /aws/eks/production-cluster/cluster
```

### Container Insights (Node + Pod Metrics)

```bash
# Install CloudWatch agent as DaemonSet
ClusterName=production-cluster
RegionName=us-east-1

curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | \
  sed "s/{{cluster_name}}/${ClusterName}/;s/{{region_name}}/${RegionName}/" | \
  kubectl apply -f -
```

### Prometheus + Grafana Stack

```bash
# Install kube-prometheus-stack via Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install kube-prometheus-stack \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=admin \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName=gp3 \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi
```

### FluentBit — Log Aggregation

```yaml
# values.yaml for aws-for-fluent-bit
image:
  repository: public.ecr.aws/aws-observability/aws-for-fluent-bit
  tag: stable

firehose:
  enabled: false

cloudWatch:
  enabled: true
  region: us-east-1
  logGroupName: /aws/eks/production-cluster/pods
  logStreamPrefix: "fluent-bit-"
  autoCreateGroup: true
```

---

## 14. EKS Add-ons

**EKS Add-ons** are operational software components managed by AWS — they're automatically updated, monitored for conflicts, and health-checked.

| Add-on | Purpose |
|--------|---------|
| `vpc-cni` | AWS VPC networking for pods |
| `coredns` | DNS resolution inside the cluster |
| `kube-proxy` | Network rules for Service routing |
| `aws-ebs-csi-driver` | EBS persistent volume provisioning |
| `aws-efs-csi-driver` | EFS shared volume provisioning |
| `amazon-guardduty-agent` | Runtime security monitoring |
| `aws-mountpoint-s3-csi-driver` | Mount S3 buckets as volumes |
| `adot` | AWS Distro for OpenTelemetry |
| `aws-load-balancer-controller` | ALB/NLB provisioning |

```bash
# List available add-on versions
aws eks describe-addon-versions \
  --kubernetes-version 1.30 \
  --query "addons[*].{Name:addonName,Versions:addonVersions[0].addonVersion}"

# Update an add-on
aws eks update-addon \
  --cluster-name production-cluster \
  --addon-name vpc-cni \
  --addon-version v1.18.0-eksbuild.1 \
  --resolve-conflicts OVERWRITE
```

---

## 15. EKS Fargate

### What

EKS Fargate lets you run pods **without managing EC2 instances**. Each pod runs in its own isolated micro-VM.

### How Fargate Works

```
You create a Fargate Profile:
  "Run pods in namespace 'serverless' on Fargate"

You deploy a pod to namespace 'serverless'
    ↓
EKS matches pod against Fargate profiles
    ↓
AWS provisions a micro-VM (seconds, not minutes)
    ↓
Pod runs in isolated VM (no shared node)
    ↓
You pay per pod vCPU+memory per second
    ↓
Pod completes → VM terminated → billing stops
```

### Fargate Profile

```yaml
# eksctl config for Fargate
fargateProfiles:
  - name: serverless-profile
    selectors:
      - namespace: serverless
        labels:
          fargate: "true"
      - namespace: kube-system   # Run CoreDNS on Fargate
```

### Fargate Limitations

```
❌ No DaemonSets (each pod is its own node)
❌ No privileged containers
❌ No GPU support
❌ Max pod size: 16 vCPU, 120 GB RAM
❌ No EBS volumes (EFS only)
❌ Slower startup than EC2 nodes
✅ Great for: batch jobs, dev/test, variable workloads
```

---

## 16. EKS Anywhere & EKS Distro

### EKS Distro (EKS-D)

The same Kubernetes distribution AWS uses in EKS, but you can run it **anywhere** — on-prem, other clouds.

```bash
# EKS-D provides:
# - Same Kubernetes version as EKS
# - Same patches and CVE fixes
# - Available as open source
# - No AWS-managed control plane
```

### EKS Anywhere

A deployment option that lets you run EKS on-premises using your own hardware or VMware vSphere.

```
EKS Anywhere:
  ├── On bare metal servers (your data center)
  ├── On VMware vSphere
  ├── On Nutanix
  └── On Snow (AWS Snowball Edge - air-gapped environments)

Management:
  ├── Single pane of glass via AWS console
  ├── Same tooling as cloud EKS
  └── Optional: Connected mode (requires internet) or Disconnected mode
```

---

## 17. Upgrading EKS Clusters

### Upgrade Order (CRITICAL)

```
Always upgrade in this order:
1. Control Plane (EKS managed)
2. Add-ons (vpc-cni, coredns, kube-proxy)
3. Node Groups (worker nodes)

NEVER skip Kubernetes minor versions:
  1.28 → 1.29 → 1.30 ✅
  1.28 → 1.30        ❌ (not supported)
```

### Upgrade Steps

```bash
# Step 1: Check current version
kubectl version

# Step 2: Read the Kubernetes changelog for breaking changes
# https://kubernetes.io/releases/

# Step 3: Upgrade control plane
aws eks update-cluster-version \
  --name production-cluster \
  --kubernetes-version 1.30

# Monitor upgrade (takes ~15 minutes)
aws eks describe-cluster \
  --name production-cluster \
  --query "cluster.status"

# Step 4: Update add-ons
aws eks update-addon \
  --cluster-name production-cluster \
  --addon-name vpc-cni \
  --addon-version v1.18.0-eksbuild.1

aws eks update-addon \
  --cluster-name production-cluster \
  --addon-name coredns \
  --addon-version v1.11.1-eksbuild.4

aws eks update-addon \
  --cluster-name production-cluster \
  --addon-name kube-proxy \
  --addon-version v1.30.0-eksbuild.1

# Step 5: Upgrade node groups (triggers rolling replacement)
aws eks update-nodegroup-version \
  --cluster-name production-cluster \
  --nodegroup-name on-demand

# Watch node group update
aws eks describe-nodegroup \
  --cluster-name production-cluster \
  --nodegroup-name on-demand \
  --query "nodegroup.status"
```

---

## 18. Production Best Practices

### Multi-AZ Architecture

```yaml
# Always spread nodes across 3 AZs
topology.kubernetes.io/zone: us-east-1a  # node label added automatically

# Spread pods across AZs using topologySpreadConstraints
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: my-app
```

### Resource Requests & Limits (Always Set These)

```yaml
resources:
  requests:
    cpu: "100m"       # 0.1 CPU cores — used for scheduling
    memory: "128Mi"   # 128 MB — used for scheduling
  limits:
    cpu: "500m"       # 0.5 CPU cores — hard cap
    memory: "512Mi"   # 512 MB — OOMKilled if exceeded
```

### Security Hardening

```yaml
# Pod Security — run as non-root
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  seccompProfile:
    type: RuntimeDefault

containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities:
      drop: [ALL]
```

### Namespace Strategy

```
cluster
├── kube-system         — Kubernetes system components
├── monitoring          — Prometheus, Grafana
├── ingress-nginx       — Ingress controller
├── production          — Production workloads
├── staging             — Staging workloads
└── development         — Dev workloads
```

### Node Selectors & Taints for Workload Isolation

```yaml
# Database pods — on high-memory, on-demand nodes only
spec:
  nodeSelector:
    role: database
  tolerations:
  - key: dedicated
    value: database
    effect: NoSchedule

# Batch jobs — on spot nodes
spec:
  nodeSelector:
    lifecycle: spot
  tolerations:
  - key: spot
    value: "true"
    effect: NoSchedule
```

---

## 19. Cost Optimization

### Use Spot Instances for Non-Critical Workloads

```
On-Demand: Full price
Spot:      Up to 90% cheaper — but can be interrupted with 2-min notice

Strategy:
  On-Demand: Control plane components, databases, stateful apps
  Spot: Batch jobs, stateless microservices, dev/test
```

### Right-Size Nodes with Goldilocks

```bash
# Install Goldilocks — analyzes pod resource usage and recommends right-sizing
helm install goldilocks fairwinds/goldilocks \
  --namespace goldilocks \
  --create-namespace

# Label a namespace to enable recommendations
kubectl label namespace production goldilocks.fairwinds.com/enabled=true

# Access dashboard
kubectl -n goldilocks port-forward svc/goldilocks-dashboard 8080:80
```

### EKS Cost Breakdown

```
Control plane:         $0.10/hour × 730 hours = $73/month
On-demand worker node (m5.xlarge): $0.192/hour × 730 = $140/node/month
Spot worker node:      ~$0.04/hour × 730 = $29/node/month
NAT Gateway:           $0.045/hour + $0.045/GB data
ALB:                   $0.008/hour + $0.008/LCU-hour
EBS (gp3 50GB/node):   $4/month/node
CloudWatch Logs:       $0.50/GB ingested
```

---

## 20. Troubleshooting Common Issues

### Nodes Not Joining the Cluster

```bash
# Check aws-auth ConfigMap has the node role
kubectl describe configmap aws-auth -n kube-system

# Check node bootstrap logs
# SSH to node or use SSM:
aws ssm start-session --target <instance-id>
# On node:
sudo cat /var/log/cloud-init-output.log
sudo journalctl -u kubelet -f
```

### Pods Stuck in Pending

```bash
# Describe the pod to see events
kubectl describe pod <pod-name>

# Common reasons:
# 1. Insufficient CPU/memory → add nodes or reduce requests
# 2. Node selector mismatch → check nodeSelector vs node labels
# 3. Taint/toleration mismatch → add tolerations
# 4. PVC not bound → check StorageClass and PVC status
# 5. Image pull failure → check ECR permissions/image name

kubectl get events --sort-by=.metadata.creationTimestamp
```

### EKS API Server Unreachable

```bash
# Check endpoint access
aws eks describe-cluster --name production-cluster \
  --query "cluster.resourcesVpcConfig"

# If privateAccess only, ensure you're on VPN/bastion
# Check security group allows 443 from your IP

# Test connectivity
curl -k https://<eks-endpoint>/healthz
```

### OOMKilled Pods

```bash
# Find OOMKilled pods
kubectl get pods -A | grep OOMKilled

# Check memory usage trends
kubectl top pod <pod-name> --containers

# Solution: Increase memory limit
# kubectl edit deployment <name> and increase limits.memory
```

### Cluster Autoscaler Not Scaling

```bash
# Check CA logs
kubectl logs -n kube-system -l app=cluster-autoscaler --tail=100

# Common issues:
# 1. ASG tags missing → add k8s.io/cluster-autoscaler/enabled=true tag
# 2. IAM permissions → check IRSA role has autoscaling:SetDesiredCapacity
# 3. Node group at max → increase maxSize in ASG
# 4. PDB blocking eviction → check PodDisruptionBudgets
# 5. Pods with local storage → annotate with safe-to-evict: true
```

---

## Quick Reference

### Essential Commands

```bash
# Cluster operations
aws eks update-kubeconfig --name <cluster> --region <region>
eksctl get cluster
eksctl delete cluster -f cluster-config.yaml

# Node group operations
eksctl get nodegroup --cluster production-cluster
eksctl scale nodegroup --cluster production-cluster --name on-demand --nodes 5

# Add-ons
aws eks list-addons --cluster-name production-cluster
aws eks describe-addon --cluster-name production-cluster --addon-name vpc-cni

# Debugging
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl top nodes
kubectl top pods -A --sort-by=memory
kubectl get events -A --sort-by=.metadata.creationTimestamp | tail -30

# IRSA verification
kubectl exec -it <pod> -- aws sts get-caller-identity
```

### EKS Cluster Architecture Summary

```
Your AWS Account
├── EKS Control Plane (AWS managed, your VPC ENI)
│   ├── API Server (HA, 3 replicas)
│   ├── etcd (encrypted, backed up)
│   ├── Scheduler + Controller Manager
│   └── OIDC Provider (for IRSA)
│
├── Worker Nodes (your responsibility)
│   ├── Managed Node Group: On-Demand (m5.xlarge, 2-10 nodes)
│   ├── Managed Node Group: Spot (m5/m4/c5, 0-20 nodes)
│   └── Fargate Profile (serverless namespace)
│
├── Networking
│   ├── VPC CNI (pods get real VPC IPs)
│   ├── AWS Load Balancer Controller (ALB/NLB)
│   └── CoreDNS (internal DNS)
│
├── Storage
│   ├── EBS CSI Driver (block storage, per pod)
│   └── EFS CSI Driver (shared storage, ReadWriteMany)
│
├── Autoscaling
│   ├── HPA (horizontal pod autoscaler — scales pods)
│   ├── VPA (vertical pod autoscaler — right-sizes pods)
│   └── Cluster Autoscaler or Karpenter (scales nodes)
│
├── Security
│   ├── aws-auth ConfigMap (IAM → K8s RBAC mapping)
│   ├── IRSA (pod-level AWS permissions)
│   ├── KMS (secret encryption at rest)
│   └── Pod Security Standards
│
└── Observability
    ├── CloudWatch Container Insights (metrics)
    ├── CloudWatch Logs (control plane + pod logs)
    ├── Prometheus + Grafana (custom metrics)
    └── FluentBit (log aggregation)
```

---

*Last updated: June 2026 | Kubernetes 1.30 | EKS Best Practices*