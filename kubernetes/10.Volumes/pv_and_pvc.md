# Persistent Volume (PV) and Persistent Volume Claim (PVC)

This is one of the most important Kubernetes storage concepts.

To fully understand PV and PVC, first understand the problem they solve.

---

# The Problem Without Persistent Storage

Suppose you run MySQL inside a pod.

```text id="pbtxv7"
MySQL Pod
   ↓
Stores DB files inside container
```

Now pod crashes or gets deleted.

Kubernetes creates new pod.

But:

```text id="5lctb5"
All database files are lost
```

because container filesystem is temporary.

---

# Why This Happens

Containers are:

```text id="ewjlwm"
Ephemeral
```

Meaning:

* temporary
* replaceable
* recreated anytime

So Kubernetes needs storage that:

* survives pod restart
* survives pod deletion
* survives node problems sometimes

That is:

```text id="5h3ydt"
Persistent Storage
```

---

# Real World Analogy

Think:

```text id="09o10d"
Pod = Laptop
Storage = External Hard Disk
```

If laptop crashes:

* external hard disk data still exists

Similarly:

* pod may die
* storage should remain

---

# Kubernetes Storage Architecture

```text id="ifw6hb"
Application Pod
      ↓
PVC (request)
      ↓
PV (actual storage)
      ↓
Physical Storage
(AWS EBS / Azure Disk / NFS / Ceph)
```

---

# What is Persistent Volume (PV)?

## Definition

A PV is:

```text id="4g5m90"
Actual storage resource in Kubernetes cluster
```

It represents:

* cloud disk
* NFS share
* SSD
* external storage

---

# Important Point

PV is:

```text id="18hz9k"
Cluster-level resource
```

NOT pod-level.

---

# PV Lifecycle

PV exists independently of pods.

Meaning:

* pod deleted → PV remains
* pod recreated → can reuse same PV

---

# What a PV Contains

A PV defines:

* storage size
* access mode
* storage type
* reclaim policy
* actual backend storage

---

# Example PV

```yaml id="lc81wr"
apiVersion: v1
kind: PersistentVolume

metadata:
  name: my-pv

spec:
  capacity:
    storage: 5Gi

  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  hostPath:
    path: /mnt/data
```

---

# Understanding Every Section

---

# 1. capacity

```yaml id="yq9t5o"
capacity:
  storage: 5Gi
```

Means:

```text id="evsl0n"
PV provides 5GB storage
```

---

# 2. accessModes

Controls:

```text id="h4o8pd"
How pods can access volume
```

---

# Access Modes in Detail

---

## ReadWriteOnce (RWO)

```text id="48s3v5"
One node can mount volume as read-write
```

Most common.

Example:

* AWS EBS
* Azure Disk

---

# Important

Multiple pods CAN use same PVC:
BUT
they must run on same node.

Because volume attached to one node.

---

# Visual

```text id="77l3wy"
Node-1
 ├── Pod-A
 ├── Pod-B
 └── Same RWO volume
```

Allowed.

---

But:

```text id="bx5wfr"
Node-1 → Pod-A
Node-2 → Pod-B
```

Not allowed for RWO.

---

## ReadOnlyMany (ROX)

```text id="7qj79d"
Multiple nodes can mount as read-only
```

Example:

* shared configs
* shared static files

---

## ReadWriteMany (RWX)

```text id="a7q09l"
Multiple nodes can read/write
```

Example:

* NFS
* CephFS

Useful for:

* multiple replicas sharing files

---

# Visual

```text id="rjlwmk"
Node-1 Pod-A
Node-2 Pod-B
Node-3 Pod-C
       ↓
Same shared RWX storage
```

---

## ReadWriteOncePod (RWOP)

Newer mode.

```text id="0on4vx"
Only ONE pod in entire cluster can use PVC
```

Very strict locking.

---

# 3. persistentVolumeReclaimPolicy

MOST IMPORTANT INTERVIEW TOPIC.

Controls:

```text id="wdbx6z"
What happens to actual storage after PVC deletion
```

---

# Reclaim Policies

| Policy  | Meaning                      |
| ------- | ---------------------------- |
| Retain  | Keep storage/data            |
| Delete  | Delete storage automatically |
| Recycle | Deprecated                   |

---

# 1. Retain Policy

## Meaning

When PVC deleted:

```text id="yrzjhc"
PV and actual data remain
```

Only binding removed.

---

# Flow

```text id="j6m19u"
PVC deleted
    ↓
PV becomes Released
    ↓
Actual disk/data still exists
```

---

# Use Cases

Critical data:

* databases
* production data
* backups

---

# Example

```yaml id="0ml7m5"
persistentVolumeReclaimPolicy: Retain
```

---

# Important

Admin must manually:

* clean data
* reuse PV
* delete PV

---

# State Flow

```text id="zyt8x6"
Available → Bound → Released
```

---

# Real Example

```text id="6mqmmb"
MySQL PVC deleted accidentally
```

With Retain:

```text id="w4kr0w"
Data still safe
```

---

# 2. Delete Policy

## Meaning

When PVC deleted:

* PV deleted
* actual storage deleted

---

# Flow

```text id="8h7u4u"
PVC deleted
    ↓
PV deleted
    ↓
Cloud disk deleted
```

---

# Common in Cloud

Used with:

* dynamic provisioning
* AWS EBS
* Azure Disk

---

# Example

```yaml id="ax1nyv"
persistentVolumeReclaimPolicy: Delete
```

---

# Risk

Accidental PVC deletion:

```text id="ydb5tb"
Entire data gone
```

---

# 3. Recycle Policy (Deprecated)

Old behavior:

```text id="b7gww4"
Delete files and make PV reusable
```

No longer recommended.

---

# 4. hostPath

```yaml id="r8fjlwm"
hostPath:
  path: /mnt/data
```

Actual storage location.

---

# Important

hostPath is:

```text id="6qvhfr"
Node-specific storage
```

Not production-grade.

If pod moves:

* data may not exist on new node.

---

# What is PVC?

PVC means:

```text id="69xlwi"
PersistentVolumeClaim
```

It is:

```text id="ppvfr7"
Request for storage
```

by application/user.

---

# Why PVC Exists

Without PVC:

* app must know storage details

Bad design.

---

# PVC Provides Abstraction

Pod only says:

```text id="77xvhn"
I need 5GB storage
```

Kubernetes handles:

* finding storage
* binding storage
* provisioning storage

---

# PVC Example

```yaml id="t5isgx"
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: my-pvc

spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 2Gi
```

---

# What Happens Internally

Kubernetes searches PV matching:

* enough size
* matching access mode
* matching storage class

Then:

```text id="ltnhyz"
binds PVC to PV
```

---

# Binding Process

```text id="r67w1o"
PV available
     ↓
PVC created
     ↓
Kubernetes matches both
     ↓
STATUS = Bound
```

---

# Check Status

```bash id="2iqlf4"
kubectl get pv
kubectl get pvc
```

---

# Possible PVC States

| State   | Meaning               |
| ------- | --------------------- |
| Pending | No matching PV        |
| Bound   | Successfully attached |
| Lost    | PV lost/problem       |

---

# Pod Never Uses PV Directly

VERY IMPORTANT.

Pod uses:

```text id="o2ndyu"
PVC
```

PVC uses:

```text id="6hsk7k"
PV
```

---

# Full Flow

```text id="y3rrcc"
Pod
 ↓
PVC
 ↓
PV
 ↓
Actual Storage
```

---

# Pod Using PVC

```yaml id="r3g1xu"
apiVersion: v1
kind: Pod

metadata:
  name: app-pod

spec:
  containers:
  - name: app
    image: nginx

    volumeMounts:
    - name: app-storage
      mountPath: /data

  volumes:
  - name: app-storage
    persistentVolumeClaim:
      claimName: my-pvc
```

---

# Data Flow

```text id="grw0hl"
Container writes /data/file.txt
        ↓
PVC
        ↓
PV
        ↓
Actual Disk
```

---

# Static Provisioning

Admin manually creates:

```text id="d0vjwo"
PV
```

Users create:

```text id="q94rjlwm"
PVC
```

Kubernetes binds them.

---

# Problem with Static Provisioning

Imagine:

* 500 developers
* each needs storage

Admin manually creating PVs becomes difficult.

---

# Dynamic Provisioning

Kubernetes automatically creates PVs.

Using:

```text id="juzcmg"
StorageClass
```

---

# Dynamic Provisioning Flow

```text id="mjlwm0"
PVC created
     ↓
StorageClass provisions storage
     ↓
Cloud disk created
     ↓
PV automatically created
     ↓
PVC bound
```

---

# StorageClass

Defines:

* storage type
* provisioner
* performance class

---

# Example

```yaml id="4zslm3"
apiVersion: storage.k8s.io/v1
kind: StorageClass

metadata:
  name: fast-storage

provisioner: kubernetes.io/aws-ebs

parameters:
  type: gp3
```

---

# PVC Using StorageClass

```yaml id="jlwmr1"
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: dynamic-pvc

spec:
  storageClassName: fast-storage

  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 10Gi
```

---

# Automatic Process

```text id="r7uk5z"
PVC created
    ↓
AWS EBS disk created automatically
    ↓
PV created automatically
    ↓
PVC bound
```

---

# Volume Expansion

PVC can sometimes be resized.

Example:

```yaml id="xvhj2r"
resources:
  requests:
    storage: 20Gi
```

Requires:

```text id="sq0q1v"
allowVolumeExpansion: true
```

in StorageClass.

---

# Important PV States

| State     | Meaning          |
| --------- | ---------------- |
| Available | Free PV          |
| Bound     | Used by PVC      |
| Released  | PVC deleted      |
| Failed    | Problem occurred |

---

# Important Commands

---

# Get PV

```bash id="jlwmc5"
kubectl get pv
```

---

# Get PVC

```bash id="jlwm9k"
kubectl get pvc
```

---

# Describe PV

```bash id="jlwm1g"
kubectl describe pv my-pv
```

---

# Describe PVC

```bash id="jlwmc0"
kubectl describe pvc my-pvc
```

---

# Delete PVC

```bash id="0t26zu"
kubectl delete pvc my-pvc
```

---

# Real Production Examples

---

# Database Storage

```text id="8bn4rr"
MySQL Pod
   ↓
PVC
   ↓
AWS EBS Volume
```

---

# Shared Filesystem

```text id="1vl0ey"
Multiple application replicas
        ↓
RWX PVC
        ↓
NFS Share
```

---

# Important Interview Questions

---

# Why PVC instead of direct PV?

Answer:

```text id="jlwmr4"
PVC abstracts storage implementation from application.
```

---

# What happens if pod deleted?

```text id="jlwm0o"
PVC and PV remain.
```

Data survives.

---

# What happens if PVC deleted?

Depends on reclaim policy.

---

# Can multiple pods use same PVC?

Depends on:

```text id="6jlwm"
Access Mode
```

---

# Difference Between Volume and PV

| Volume             | PV                |
| ------------------ | ----------------- |
| Pod-level          | Cluster-level     |
| Temporary usually  | Persistent        |
| Defined inside pod | Separate resource |

---

# Difference Between PV and PVC

| PV                  | PVC              |
| ------------------- | ---------------- |
| Actual storage      | Storage request  |
| Supply              | Consume          |
| Admin/cloud creates | User/app creates |

---

# Full End-to-End Flow

```text id="jlwm9f"
Developer creates PVC
        ↓
Kubernetes finds/provisions PV
        ↓
PVC bound to PV
        ↓
Pod mounts PVC
        ↓
Application stores data
        ↓
Data persists even if pod dies
```
