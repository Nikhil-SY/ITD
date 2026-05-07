# Volumes in Kubernetes

## Why Volumes Are Needed

By default, containers are **ephemeral**.

Meaning:

* If container restarts → data inside container is lost
* If pod gets deleted → all files inside pod are deleted

Example:

```bash
kubectl exec -it my-pod -- /bin/bash
echo "hello" > /tmp/test.txt
```

If pod restarts:

```bash
/tmp/test.txt
```

is gone.

To solve this → Kubernetes uses **Volumes**.

---

# What is a Volume?

A **Volume** is a storage mounted inside a pod/container.

It allows:

* Data persistence
* Sharing data between containers
* Accessing external storage

---

# Important Point

Volume lifecycle depends on volume type.

Some volumes:

* Exist only till pod lives

Some:

* Persist even after pod deletion

---

# How Volume Works

```text
Storage
   ↓
Volume
   ↓
Mounted into container path
   ↓
Application reads/writes files
```

---

# Basic Volume Flow

```text
Container Path
     ↓
Volume Mount
     ↓
Volume
     ↓
Actual Storage
```

---

# Main Volume Types in Kubernetes

| Volume Type      | Persistent? | Use Case                |
| ---------------- | ----------- | ----------------------- |
| emptyDir         | No          | Temporary storage       |
| hostPath         | Sometimes   | Access node filesystem  |
| configMap        | No          | Config files            |
| secret           | No          | Sensitive data          |
| PersistentVolume | Yes         | Real persistent storage |

---

# 1. emptyDir Volume

## What is it?

Temporary storage created when pod starts.

Deleted when pod is deleted.

---

# Use Cases

* Cache
* Temporary files
* Sharing data between containers

---

# How It Works

```text
Pod starts
   ↓
emptyDir created
   ↓
Containers use it
   ↓
Pod deleted
   ↓
Data deleted
```

---

# Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-pod

spec:
  containers:
  - name: app-container
    image: nginx

    volumeMounts:
    - name: shared-volume
      mountPath: /usr/share/nginx/html

  volumes:
  - name: shared-volume
    emptyDir: {}
```

---

# Explanation

## volumeMounts

```yaml
volumeMounts:
- name: shared-volume
  mountPath: /usr/share/nginx/html
```

Mounts volume inside container.

---

## volumes

```yaml
volumes:
- name: shared-volume
  emptyDir: {}
```

Creates temporary storage.

---

# 2. hostPath Volume

## What is it?

Mounts actual node filesystem into pod.

---

# Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-pod

spec:
  containers:
  - name: app
    image: nginx

    volumeMounts:
    - name: host-volume
      mountPath: /data

  volumes:
  - name: host-volume
    hostPath:
      path: /tmp
      type: Directory
```

---

# Flow

```text
Node /tmp directory
        ↓
hostPath volume
        ↓
Mounted inside pod at /data
```

---

# Important

If pod moves to another node:

* data may not exist there

So hostPath is not ideal for production.

---

# Use Cases

* Node logs access
* Monitoring agents
* Debugging

---

# 3. ConfigMap Volume

Used to mount configuration files.

---

# Example ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config

data:
  app.properties: |
    app.name=myapp
    app.port=8080
```

---

# Pod Using ConfigMap

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod

spec:
  containers:
  - name: app
    image: nginx

    volumeMounts:
    - name: config-volume
      mountPath: /etc/config

  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

---

# Inside Container

```text
/etc/config/app.properties
```

file will exist.

---

# 4. Secret Volume

Same as ConfigMap but for sensitive data.

---

# Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret

type: Opaque

data:
  password: YWRtaW4=
```

(Base64 encoded)

---

# Pod Using Secret

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod

spec:
  containers:
  - name: app
    image: nginx

    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secret

  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
```

---

# Persistent Storage Problem

Suppose:

* Database pod stores data
* Pod crashes
* New pod created

Without persistent storage:

```text
All DB data lost
```

Need storage independent of pod lifecycle.

This is where:

* PV
* PVC
  come.

---

# Persistent Volume (PV)

## What is PV?

A **PersistentVolume** is actual storage in cluster.

Can be:

* AWS EBS
* Azure Disk
* NFS
* Ceph
* Local storage

It exists independently of pods.

---

# Real World Analogy

```text
PV = Actual Hard Disk
PVC = Request for storage
Pod = Uses storage
```

---

# Persistent Volume Flow

```text
Cloud Disk / NFS / Storage
          ↓
PersistentVolume
          ↓
PersistentVolumeClaim
          ↓
Pod
```

---

# What is PVC?

PVC = PersistentVolumeClaim

It is a request for storage by user/application.

---

# Why PVC Needed?

Without PVC:

* Pod must know storage details

With PVC:

* Pod only requests storage
* Kubernetes handles matching

This gives abstraction.

---

# Example Analogy

```text
Employee asks:
"I need 10GB storage"

Admin provides disk.

Employee does not care:
- which server
- which disk
- which hardware
```

PVC works similarly.

---

# Static Provisioning

Admin manually creates PV.

User creates PVC.

Kubernetes binds both.

---

# Step-by-Step Example

# Step 1 — Create PV

```yaml
apiVersion: v1
kind: PersistentVolume

metadata:
  name: my-pv

spec:
  capacity:
    storage: 1Gi

  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  hostPath:
    path: /mnt/data
```

---

# Explanation

## capacity

```yaml
capacity:
  storage: 1Gi
```

Storage size.

---

## accessModes

```yaml
ReadWriteOnce
```

Only one node can mount as read-write.

---

# Access Modes

| Mode                | Meaning                   |
| ------------------- | ------------------------- |
| ReadWriteOnce (RWO) | One node read/write       |
| ReadOnlyMany (ROX)  | Multiple nodes read-only  |
| ReadWriteMany (RWX) | Multiple nodes read/write |

---

## reclaimPolicy

```yaml
Retain
```

When PVC deleted:

* actual data remains

Other options:

* Delete
* Recycle (deprecated)

---

# Step 2 — Create PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: my-pvc

spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 500Mi
```

---

# What Happens?

Kubernetes checks:

* access mode
* storage size

Then binds PVC to matching PV.

---

# Check Binding

```bash
kubectl get pv
kubectl get pvc
```

STATUS:

```text
Bound
```

---

# Step 3 — Use PVC in Pod

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: app-pod

spec:
  containers:
  - name: app
    image: nginx

    volumeMounts:
    - mountPath: /data
      name: storage

  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: my-pvc
```

---

# Flow

```text
Container /data
      ↓
PVC
      ↓
PV
      ↓
Actual Disk
```

---

# Important Interview Point

Pod never directly uses PV.

Pod uses:

```text
PVC
```

PVC uses:

```text
PV
```

---

# Dynamic Provisioning

Manual PV creation is difficult.

So Kubernetes supports:

* automatic PV creation

using:

```text
StorageClass
```

---

# Dynamic Provisioning Flow

```text
PVC created
     ↓
StorageClass provisions disk automatically
     ↓
PV created automatically
     ↓
PVC bound
```

---

# StorageClass Example

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass

metadata:
  name: fast-storage

provisioner: kubernetes.io/aws-ebs

parameters:
  type: gp2
```

---

# PVC Using StorageClass

```yaml
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
      storage: 5Gi
```

---

# Real Production Flow

```text
Application
    ↓
PVC
    ↓
StorageClass
    ↓
Cloud creates disk
    ↓
PV automatically created
```

---

# Important Commands

## Get PV

```bash
kubectl get pv
```

---

## Get PVC

```bash
kubectl get pvc
```

---

## Describe PVC

```bash
kubectl describe pvc my-pvc
```

---

## Describe PV

```bash
kubectl describe pv my-pv
```

---

# Volume Mount Path

Example:

```yaml
mountPath: /data
```

Inside container:

```text
/data
```

becomes persistent storage.

---

# subPath in Volume

Used to mount only specific folder/file.

Example:

```yaml
volumeMounts:
- name: storage
  mountPath: /app/config
  subPath: config
```

---

# Multi-Container Shared Volume

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: shared-volume-pod

spec:
  containers:
  - name: writer
    image: busybox
    command: ["/bin/sh", "-c"]

    args:
      - while true; do
          echo hello >> /shared-data/index.html;
          sleep 5;
        done

    volumeMounts:
    - name: shared-volume
      mountPath: /shared-data

  - name: reader
    image: nginx

    volumeMounts:
    - name: shared-volume
      mountPath: /usr/share/nginx/html

  volumes:
  - name: shared-volume
    emptyDir: {}
```

---

# Flow Here

```text
Writer container
      ↓ writes
emptyDir volume
      ↓ reads
Reader container
```

---

# Difference Between Volume and PV

| Volume                          | PV                    |
| ------------------------------- | --------------------- |
| Pod-level storage               | Cluster-level storage |
| Usually temporary               | Persistent            |
| Defined in pod                  | Separate resource     |
| Lifecycle tied to pod sometimes | Independent of pod    |

---

# Difference Between PV and PVC

| PV                             | PVC                 |
| ------------------------------ | ------------------- |
| Actual storage                 | Request for storage |
| Created by admin/storage class | Created by user/app |
| Supplies storage               | Consumes storage    |

---

# Real Production Example

## Database Pod

```text
MySQL Pod
   ↓
PVC
   ↓
AWS EBS Volume
```

Pod deleted?

* data still safe.

New pod attaches same volume.

---

# Important Interview Questions

## Why PVC instead of direct PV?

Answer:

```text
PVC abstracts actual storage implementation from application.
```

---

## What happens if PVC deleted?

Depends on reclaim policy:

* Retain → keep data
* Delete → delete storage

---

## Can multiple pods use same PVC?

Depends on:

```text
AccessMode
```

RWX supports multiple pods.

---

# Summary

```text
Container storage → temporary

Volume → storage for pod

emptyDir → temporary pod storage

hostPath → node filesystem

PV → actual persistent storage

PVC → request for storage

StorageClass → automatic provisioning
```
