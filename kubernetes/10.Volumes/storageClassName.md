## Case 1: `storageClassName: manual` (Static provisioning)

**Meaning:**
You **manually create the PV first**, then PVC binds to it.

---

### Step 1: Create PV manually

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: manual-pv
spec:
  capacity:
    storage: 5Gi                    # PV size
  accessModes:
    - ReadWriteOnce                 # One node can mount as read-write
  storageClassName: manual          # Custom label for matching
  persistentVolumeReclaimPolicy: Retain   # Keep data even after PVC deletion
  hostPath:
    path: /mnt/data                 # Node local directory
```

---

### Step 2: Create PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: manual-pvc
spec:
  accessModes:
    - ReadWriteOnce                 # Must match PV
  resources:
    requests:
      storage: 2Gi                  # Request 2Gi (PV has 5Gi, so okay)
  storageClassName: manual          # Must match PV
```

---

### How binding happens

```text
PV created manually
storageClassName = manual
       ↓
PVC created
storageClassName = manual
       ↓
Kubernetes checks:
  same storage class? yes
  enough storage? yes
  access mode match? yes
       ↓
PVC bound to PV
```

Check:

```bash
kubectl get pv,pvc
```

Output:

```text
manual-pv    Bound
manual-pvc   Bound
```

---

# Case 2: `storageClassName: local` (Local storage example)

Usually used with **local disk storage** + **node affinity**.

---

### Step 1: Create PV

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: local
  persistentVolumeReclaimPolicy: Delete

  local:
    path: /mnt/local-storage      # Actual disk path on node

  nodeAffinity:                   # IMPORTANT for local PV
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - worker-node-1
```

---

### Why `nodeAffinity` needed?

Because local storage exists only on **one node**.

```text
worker-node-1
   └── /mnt/local-storage
```

Kubernetes must schedule pod on same node.

---

### Step 2: PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local
```

---

### Step 3: Pod using PVC

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
    - name: my-storage
      mountPath: /usr/share/nginx/html

  volumes:
  - name: my-storage
    persistentVolumeClaim:
      claimName: local-pvc
```

---

# How this works

```text
Node worker-node-1
    ↓
Disk path /mnt/local-storage
    ↓
PV (storageClassName: local)
    ↓
PVC (storageClassName: local)
    ↓
Pod uses PVC
    ↓
Scheduler places pod on worker-node-1
```

---

# Difference between both

| Feature              | `manual`           | `local`                     |
| -------------------- | ------------------ | --------------------------- |
| Meaning              | Just a custom name | Usually used for local disk |
| PV type              | Often `hostPath`   | Usually `local`             |
| Node affinity needed | No                 | Yes                         |
| Production use       | Learning/testing   | Better than hostPath        |
| Static provisioning  | Yes                | Yes                         |

---

# Important note

Both:

```yaml
storageClassName: manual
storageClassName: local
```

are just **labels**.

This would also work:

```yaml
storageClassName: nikhil-storage
```

As long as PV and PVC match.

---

## Interview one-liner

**With `manual`, you statically create and bind a PV and PVC using a matching storage class name; with `local`, you usually create a local-disk PV with node affinity so pods use storage from a specific node.**
