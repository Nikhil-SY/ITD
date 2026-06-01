# ArgoCD — Complete Guide: Installation, Setup & Dashboard

> **Audience:** This guide is written for everyone — whether you're brand new to Kubernetes or an experienced engineer. Every concept is explained with *What it is*, *Why it matters*, and *How to use it*, supported by real examples.

---

## Table of Contents

1. [What is ArgoCD? (The Big Picture)](#1-what-is-argocd-the-big-picture)
2. [Core Concepts Before You Begin](#2-core-concepts-before-you-begin)
3. [Prerequisites](#3-prerequisites)
4. [Installation Method 1 — Plain Manifests (kubectl)](#4-installation-method-1--plain-manifests-kubectl)
5. [Installation Method 2 — Kustomize](#5-installation-method-2--kustomize)
6. [Installation Method 3 — Helm](#6-installation-method-3--helm)
7. [Accessing the ArgoCD Dashboard](#7-accessing-the-argocd-dashboard)
8. [Dashboard Deep Dive — Every Section Explained](#8-dashboard-deep-dive--every-section-explained)
9. [Creating Your First Application](#9-creating-your-first-application)
10. [Sync Policies — Manual vs Automatic](#10-sync-policies--manual-vs-automatic)
11. [Health Status & Sync Status Explained](#11-health-status--sync-status-explained)
12. [ArgoCD CLI — Power User Commands](#12-argocd-cli--power-user-commands)
13. [Real-World Project Structure](#13-real-world-project-structure)
14. [Troubleshooting Common Issues](#14-troubleshooting-common-issues)
15. [Security Best Practices](#15-security-best-practices)

---

## 1. What is ArgoCD? (The Big Picture)

### What

**ArgoCD** (Argo Continuous Delivery) is a **GitOps-based continuous delivery tool for Kubernetes**. It watches a Git repository and automatically ensures your Kubernetes cluster matches exactly what is defined in that repository.

Think of it like this:

> Imagine you have a blueprint (your Git repo) for how a building should look. ArgoCD is the construction supervisor who constantly checks: *"Does the actual building match the blueprint?"* If someone paints a wall the wrong colour, ArgoCD notices the drift and can automatically repaint it back — or alert you to do so.

### Why

Without ArgoCD, deploying applications to Kubernetes typically looks like this:

```
Developer writes YAML → runs kubectl apply manually → hopes nothing drifts
```

Problems with this approach:
- **Manual and error-prone** — someone forgets a flag, applies to the wrong cluster
- **No audit trail** — who deployed what, when, and why?
- **No rollback** — reverting a bad deploy is painful
- **Configuration drift** — someone manually patches a running pod; now cluster ≠ Git

ArgoCD solves all of this via the **GitOps** philosophy:

> **"Git is the single source of truth. If it's in Git, it's deployed. If it's not in Git, it doesn't exist."**

### How ArgoCD Works (Conceptually)

```
┌─────────────────────────────────────────────────────────┐
│                        Git Repository                    │
│   (Your Kubernetes YAML / Helm charts / Kustomize)       │
└───────────────────────┬─────────────────────────────────┘
                        │  ArgoCD polls every 3 minutes
                        │  (or webhook triggers immediately)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    ArgoCD Controller                     │
│  Compares: Desired State (Git) vs Live State (Cluster)   │
│                                                          │
│  If MATCH  → Status: Synced ✅                           │
│  If MISMATCH → Status: OutOfSync ⚠️ → Auto/Manual Sync  │
└───────────────────────┬─────────────────────────────────┘
                        │  kubectl apply (internally)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                      │
│   Deployments, Services, ConfigMaps, Secrets, etc.       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Core Concepts Before You Begin

Understanding these terms will make everything else click.

### GitOps
A practice where Git is the authoritative source for infrastructure and application configuration. Changes are made via pull requests, not direct `kubectl` commands.

### Application (ArgoCD's main unit)
An ArgoCD **Application** is a custom Kubernetes resource that says:
- **"Watch THIS Git repo path"**
- **"Deploy to THIS cluster/namespace"**
- **"Use THIS tool (Helm/Kustomize/plain YAML) to render manifests"**

### Sync
The act of making the cluster match Git. ArgoCD *syncs* the desired state (Git) into the live state (cluster).

### App of Apps Pattern
A single ArgoCD Application that manages other ArgoCD Applications. Used for bootstrapping entire clusters.

### Source of Truth
Git. Always Git. Changes to production must go through Git — never direct `kubectl edit` on production.

---

## 3. Prerequisites

Before installing ArgoCD, ensure you have:

| Requirement | Minimum Version | Check Command |
|---|---|---|
| Kubernetes cluster | 1.23+ | `kubectl version` |
| kubectl configured | Any | `kubectl cluster-info` |
| Helm (for Helm install) | 3.8+ | `helm version` |
| Kustomize (for Kustomize install) | 5.0+ | `kustomize version` |
| ArgoCD CLI (optional) | Latest | `argocd version` |

### Verify your cluster is accessible

```bash
kubectl cluster-info
# Expected output:
# Kubernetes control plane is running at https://...
# CoreDNS is running at https://...
```

---

## 4. Installation Method 1 — Plain Manifests (kubectl)

This is the simplest method — good for quickly understanding what gets installed. It installs ArgoCD using the official upstream manifests directly.

### Step 1: Create the ArgoCD namespace

```bash
# A namespace is like a dedicated room in your cluster for ArgoCD's components
kubectl create namespace argocd
```

### Step 2: Apply the official install manifest

```bash
# This installs the full ArgoCD stack (non-HA)
kubectl apply -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### What gets installed?

```
argocd namespace
├── argocd-server              # The API server + UI (what you interact with)
├── argocd-repo-server         # Clones Git repos and generates manifests
├── argocd-application-controller  # The brain: watches cluster, compares with Git
├── argocd-dex-server          # SSO/authentication (integrates with GitHub, LDAP, etc.)
├── argocd-redis               # Caching layer for performance
└── argocd-applicationset-controller  # Manages ApplicationSets (advanced multi-app)
```

### Step 3: Wait for all pods to be Ready

```bash
kubectl get pods -n argocd -w
# -w = watch (live updates)
# Wait until all pods show STATUS: Running
```

Expected output:
```
NAME                                                READY   STATUS    RESTARTS
argocd-application-controller-0                     1/1     Running   0
argocd-applicationset-controller-xxx                1/1     Running   0
argocd-dex-server-xxx                               1/1     Running   0
argocd-notifications-controller-xxx                 1/1     Running   0
argocd-redis-xxx                                    1/1     Running   0
argocd-repo-server-xxx                              1/1     Running   0
argocd-server-xxx                                   1/1     Running   0
```

---

## 5. Installation Method 2 — Kustomize

### What is Kustomize?

Kustomize is a tool that lets you **customize Kubernetes YAML without editing the original files**. You define patches and overlays on top of a base configuration.

Think of it like this: The original ArgoCD install.yaml is a **template house**. Kustomize lets you add your own wallpaper, furniture, and custom rooms — without modifying the original blueprint.

### Why use Kustomize for ArgoCD?

- **Reproducible** — your customizations are stored in Git alongside your apps
- **Auditable** — every change is a Git commit
- **Overlayable** — easily have dev/staging/prod variants
- **No templating language** — pure YAML patches

### Project Structure

```
argocd/
├── base/
│   └── kustomization.yaml        # Points to upstream ArgoCD manifests
└── overlays/
    ├── dev/
    │   └── kustomization.yaml    # Dev-specific patches (smaller resources)
    └── production/
        ├── kustomization.yaml    # Prod-specific patches (HA, resource limits)
        ├── argocd-server-patch.yaml
        └── argocd-cm-patch.yaml
```

### Step 1: Create the base kustomization

```yaml
# argocd/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: argocd

# This is the upstream ArgoCD install manifest — Kustomize fetches it directly
resources:
  - https://raw.githubusercontent.com/argoproj/argo-cd/v2.11.0/manifests/install.yaml
```

> **What this does:** Tells Kustomize to use the official ArgoCD v2.11.0 manifests as the *base* — like referencing the original blueprint.

### Step 2: Create the production overlay

```yaml
# argocd/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# Reference the base (inherits everything from it)
resources:
  - ../../base

namespace: argocd

# Patches: modify specific parts of base resources without touching them
patches:
  # Patch 1: Customise the ArgoCD server deployment
  - path: argocd-server-patch.yaml
    target:
      kind: Deployment
      name: argocd-server

  # Patch 2: Customise the ArgoCD ConfigMap
  - path: argocd-cm-patch.yaml
    target:
      kind: ConfigMap
      name: argocd-cm

# Add/override ConfigMap data using configMapGenerator
configMapGenerator:
  - name: argocd-cm
    behavior: merge    # merge = add to existing, not replace
    literals:
      # Allow connections from these domains (for SSO/webhook)
      - url=https://argocd.mycompany.com

# Replace image tags (e.g., to pin to a specific version)
images:
  - name: quay.io/argoproj/argocd
    newTag: v2.11.0
```

### Step 3: ArgoCD Server Patch

```yaml
# argocd/overlays/production/argocd-server-patch.yaml
# This is a strategic merge patch — it merges with the existing Deployment spec
apiVersion: apps/v1
kind: Deployment
metadata:
  name: argocd-server
spec:
  # Scale to 2 replicas for high availability in production
  replicas: 2
  template:
    spec:
      containers:
        - name: argocd-server
          # Set resource requests and limits
          resources:
            requests:
              cpu: "100m"       # 0.1 CPU cores
              memory: "128Mi"   # 128 megabytes RAM
            limits:
              cpu: "500m"       # 0.5 CPU cores
              memory: "256Mi"   # 256 megabytes RAM
          # Add the --insecure flag if you're terminating TLS at an ingress/load balancer
          # (ArgoCD won't try to serve its own TLS)
          args:
            - /usr/local/bin/argocd-server
            - --insecure
```

### Step 4: ArgoCD ConfigMap Patch

```yaml
# argocd/overlays/production/argocd-cm-patch.yaml
# The argocd-cm ConfigMap controls ArgoCD's behaviour
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
data:
  # Which Kubernetes resources ArgoCD should manage
  # (Usually left at defaults)

  # Enable status badge for repositories
  statusbadge.enabled: "true"

  # Git polling interval (default: 3m0s)
  timeout.reconciliation: "180s"

  # Ignore differences in specific fields (e.g., autoscaler-managed replicas)
  resource.customizations.ignoreDifferences.apps_Deployment: |
    jsonPointers:
      - /spec/replicas
```

### Step 5: Create a dev overlay (lighter resources)

```yaml
# argocd/overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namespace: argocd

patches:
  - patch: |-
      - op: replace
        path: /spec/replicas
        value: 1
    target:
      kind: Deployment
      name: argocd-server
```

### Step 6: Deploy using Kustomize

```bash
# First, preview what will be applied (dry run — safe to run anytime)
kubectl apply -k argocd/overlays/production --dry-run=client

# Create the namespace first
kubectl create namespace argocd

# Apply the production overlay
kubectl apply -k argocd/overlays/production

# Or apply dev overlay
kubectl apply -k argocd/overlays/dev
```

### Step 7: Verify

```bash
kubectl get all -n argocd
```

---

## 6. Installation Method 3 — Helm

### What is Helm?

Helm is the **package manager for Kubernetes**. Instead of writing raw YAML, you install pre-packaged "charts" and configure them with a `values.yaml` file.

Think of Helm like **apt/brew for Kubernetes** — `helm install argocd argo/argo-cd` is like `brew install argocd`.

### Why use Helm for ArgoCD?

- **Simpler customisation** — change values, not YAML patches
- **Easy upgrades** — `helm upgrade` handles version bumps
- **Community maintained** — the Argo Helm chart is well-tested and widely used
- **Templated** — Go templating for complex conditional logic

### Step 1: Add the Argo Helm repository

```bash
# "repos" are like app stores for Helm charts
helm repo add argo https://argoproj.github.io/argo-helm

# Update the local cache (like apt-get update)
helm repo update

# Verify the repo was added
helm repo list
# NAME   URL
# argo   https://argoproj.github.io/argo-helm
```

### Step 2: Inspect available versions and default values

```bash
# See available chart versions
helm search repo argo/argo-cd --versions | head -10

# Download the default values to understand all options
helm show values argo/argo-cd > argocd-default-values.yaml

# Open argocd-default-values.yaml to explore — it's very well documented
```

### Step 3: Create your custom values file

```yaml
# argocd-values.yaml
# Only override what you need — everything else uses smart defaults

## ─────────────────────────────────────────────
## Global settings
## ─────────────────────────────────────────────
global:
  # Domain where ArgoCD will be accessed
  # Used for generating URLs in notifications
  domain: argocd.mycompany.com

## ─────────────────────────────────────────────
## ArgoCD Server (the UI + API component)
## ─────────────────────────────────────────────
server:
  # Number of replicas (use 2+ for production HA)
  replicas: 2

  # Run in insecure mode (let your ingress/load balancer handle TLS)
  # Remove --insecure if you want ArgoCD to serve its own TLS certificate
  extraArgs:
    - --insecure

  # Resource requests/limits for the server pod
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi

  # Ingress: exposes ArgoCD via a hostname
  ingress:
    enabled: true
    ingressClassName: nginx    # Use your ingress class (nginx / traefik / alb)
    hostname: argocd.mycompany.com
    annotations:
      nginx.ingress.kubernetes.io/ssl-redirect: "true"
      # If using cert-manager for automatic TLS certificates:
      cert-manager.io/cluster-issuer: "letsencrypt-prod"
    tls: true

## ─────────────────────────────────────────────
## Application Controller
## (The brain that watches your cluster)
## ─────────────────────────────────────────────
controller:
  replicas: 1    # Statefulset; 1 is fine unless very large cluster

  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

## ─────────────────────────────────────────────
## Repo Server
## (Clones Git repos, runs Helm/Kustomize)
## ─────────────────────────────────────────────
repoServer:
  replicas: 2    # Scale this for faster sync on many apps

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi

## ─────────────────────────────────────────────
## Redis (caching)
## ─────────────────────────────────────────────
redis:
  resources:
    requests:
      cpu: 100m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 128Mi

## ─────────────────────────────────────────────
## ApplicationSet Controller
## (Manages ApplicationSets for multi-app patterns)
## ─────────────────────────────────────────────
applicationSet:
  replicas: 1

## ─────────────────────────────────────────────
## ArgoCD Configuration (argocd-cm ConfigMap)
## ─────────────────────────────────────────────
configs:
  cm:
    # How often to poll Git for changes (default: 3 minutes)
    timeout.reconciliation: 180s

    # Enable status badges on repos
    statusbadge.enabled: "true"

    # Admin account enabled (set to false once you configure SSO)
    admin.enabled: "true"

    # Example: GitHub SSO using Dex (uncomment and configure)
    # dex.config: |
    #   connectors:
    #     - type: github
    #       id: github
    #       name: GitHub
    #       config:
    #         clientID: YOUR_GITHUB_CLIENT_ID
    #         clientSecret: $dex.github.clientSecret
    #         orgs:
    #           - name: your-github-org

  # RBAC: Role-Based Access Control
  rbac:
    # Default policy for logged-in users
    # role:readonly = can see everything, change nothing
    # role:admin    = full access
    policy.default: role:readonly

    # Give your team admin access (replace with real usernames/groups)
    policy.csv: |
      p, role:org-admin, applications, *, */*, allow
      p, role:org-admin, clusters, get, *, allow
      p, role:org-admin, repositories, get, *, allow
      g, your-github-org:devops-team, role:org-admin

  # Manage the initial admin password via secret
  secret:
    # Set an initial argocd admin password (bcrypt hash)
    # Generate with: htpasswd -nbBC 10 "" YOUR_PASSWORD | tr -d ':\n' | sed 's/$2y/$2a/'
    # Leave empty to get a random auto-generated password
    argocdServerAdminPassword: ""

## ─────────────────────────────────────────────
## Notifications Controller
## (Send Slack/email alerts on sync events)
## ─────────────────────────────────────────────
notifications:
  enabled: true
```

### Step 4: Install ArgoCD via Helm

```bash
# Create the namespace
kubectl create namespace argocd

# Install (first time)
helm install argocd argo/argo-cd \
  --namespace argocd \
  --values argocd-values.yaml \
  --version 7.3.4    # Pin to a specific chart version for reproducibility

# Expected output:
# NAME: argocd
# LAST DEPLOYED: Mon Jun  1 12:00:00 2026
# NAMESPACE: argocd
# STATUS: deployed
# REVISION: 1
```

### Step 5: Upgrade ArgoCD (when you change values or bump version)

```bash
# After editing argocd-values.yaml, upgrade:
helm upgrade argocd argo/argo-cd \
  --namespace argocd \
  --values argocd-values.yaml \
  --version 7.4.0    # New version

# Check the history
helm history argocd -n argocd

# Rollback if something goes wrong
helm rollback argocd 1 -n argocd    # Roll back to revision 1
```

### Step 6: Verify the Helm installation

```bash
# See what Helm installed
helm list -n argocd

# Check all pods are running
kubectl get pods -n argocd

# See the values currently active
helm get values argocd -n argocd
```

### Kustomize vs Helm — When to Use Which?

| Factor | Kustomize | Helm |
|---|---|---|
| Learning curve | Lower (plain YAML) | Slightly higher (templates) |
| Customisation | Patch-based | Values-based |
| Upgrades | Manual diff/patch | `helm upgrade` |
| Community charts | Must write yourself | Large ecosystem |
| Best for | Teams already using Kustomize | New setups, complex configs |

---

## 7. Accessing the ArgoCD Dashboard

### Method 1: Port Forwarding (Local/Dev — simplest)

Port forwarding creates a tunnel from your laptop to the ArgoCD server pod. No ingress needed.

```bash
# Forward local port 8080 to ArgoCD server port 443
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Keep this terminal open — the tunnel stays active while it runs
```

Open your browser: **https://localhost:8080**

> **Why HTTPS?** ArgoCD uses TLS by default. Your browser will show a certificate warning (self-signed cert). Click "Advanced → Proceed" — this is safe for local access.

### Method 2: NodePort (Cluster accessible)

```bash
# Patch the argocd-server service to NodePort type
kubectl patch svc argocd-server -n argocd \
  -p '{"spec": {"type": "NodePort"}}'

# Get the assigned NodePort
kubectl get svc argocd-server -n argocd
# NAME            TYPE       CLUSTER-IP      PORT(S)
# argocd-server   NodePort   10.96.200.100   80:32080/TCP,443:32443/TCP

# Access at: https://<any-node-ip>:32443
```

### Method 3: LoadBalancer (Cloud clusters — GKE, EKS, AKS)

```bash
# Change service type to LoadBalancer
kubectl patch svc argocd-server -n argocd \
  -p '{"spec": {"type": "LoadBalancer"}}'

# Wait for an external IP to be assigned
kubectl get svc argocd-server -n argocd -w
# NAME            TYPE           CLUSTER-IP      EXTERNAL-IP
# argocd-server   LoadBalancer   10.96.200.100   34.120.10.50   <-- use this IP

# Access at: https://34.120.10.50
```

### Method 4: Ingress (Production recommended)

If you installed with Helm and `ingress.enabled: true`, ArgoCD is already accessible at your hostname.

```bash
# Verify the ingress was created
kubectl get ingress -n argocd

# DNS: Point argocd.mycompany.com → your ingress controller's IP
# Then access: https://argocd.mycompany.com
```

### Getting the Initial Admin Password

ArgoCD auto-generates a password and stores it in a Kubernetes Secret.

```bash
# Get the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo

# Output: something like "Xf3kLm9pQr2v" — copy this
```

Log in with:
- **Username:** `admin`
- **Password:** (the value from above)

> **Important:** After first login, change the admin password via **Settings → Account → Update Password**, then delete the auto-generated secret:
> ```bash
> kubectl delete secret argocd-initial-admin-secret -n argocd
> ```

### ArgoCD CLI Login

```bash
# Install ArgoCD CLI (macOS)
brew install argocd

# Install ArgoCD CLI (Linux)
curl -sSL -o argocd \
  https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x argocd && sudo mv argocd /usr/local/bin/

# Login
argocd login localhost:8080 \
  --username admin \
  --password <your-password> \
  --insecure   # Skip TLS verification for localhost

# Change password immediately
argocd account update-password
```

---

## 8. Dashboard Deep Dive — Every Section Explained

### 8.1 Home / Applications Page

This is your **mission control** — the first page you see after login.

```
┌──────────────────────────────────────────────────────────────────┐
│  🔷 ArgoCD          Applications    Settings    ?  admin  🔔     │
├──────────────────────────────────────────────────────────────────┤
│  + NEW APP    SYNC ALL    REFRESH ALL                            │
│                                                                  │
│  Filters: [All Clusters ▼] [All Namespaces ▼] [Status ▼]        │
│                                                                  │
│  ┌────────────────────┐  ┌────────────────────┐                  │
│  │ 📦 my-webapp       │  │ 📦 my-database      │                  │
│  │ Synced ✅  Healthy ✅│  │ OutOfSync ⚠️ Healthy│                  │
│  │ default            │  │ default             │                  │
│  │ https://github.com │  │ https://github.com  │                  │
│  └────────────────────┘  └────────────────────┘                  │
└──────────────────────────────────────────────────────────────────┘
```

**What each card shows:**
- **App name** — the ArgoCD Application resource name
- **Sync status** — does the cluster match Git? (Synced / OutOfSync / Unknown)
- **Health status** — are the workloads actually running? (Healthy / Degraded / Progressing / Missing)
- **Namespace** — target namespace in the cluster
- **Repo URL** — the Git repository being watched

**Top bar controls:**
- **+ NEW APP** — create a new ArgoCD Application (walk-through UI wizard)
- **SYNC ALL** — trigger sync for all applications at once
- **REFRESH ALL** — force ArgoCD to re-poll Git immediately (don't wait 3 minutes)

### 8.2 Application Detail View

Click any application card to open the **Application Detail View** — the most information-rich screen in ArgoCD.

```
┌──────────────────────────────────────────────────────────────────┐
│  my-webapp                                    SYNC  REFRESH  ⚙️  │
├──────────────┬───────────────────────────────────────────────────┤
│ SYNC STATUS  │  HEALTH STATUS  │  REPOSITORY              │      │
│ Synced ✅    │  Healthy ✅      │  github.com/org/repo      │      │
│              │                │  Path: k8s/overlays/prod  │      │
├──────────────┴───────────────────────────────────────────────────┤
│                     RESOURCE TREE                                │
│                                                                  │
│  📦 my-webapp (Application)                                      │
│  └─ 🔷 Deployment/my-webapp                         Healthy ✅   │
│     ├─ 📋 ReplicaSet/my-webapp-7d9f8b6c4            Healthy ✅   │
│     │  ├─ 🟢 Pod/my-webapp-7d9f8b6c4-xkj2p          Running      │
│     │  └─ 🟢 Pod/my-webapp-7d9f8b6c4-m9v3q          Running      │
│     └─ 🔧 Service/my-webapp                         Healthy ✅   │
│  └─ 📄 ConfigMap/my-webapp-config                   Synced ✅    │
│  └─ 🔒 ServiceAccount/my-webapp                     Synced ✅    │
└──────────────────────────────────────────────────────────────────┘
```

**Resource Tree:** A live visual graph of every Kubernetes resource this app manages, with their current health. You can:
- **Click any resource** → see its YAML, logs, events
- **See parent-child relationships** — e.g., Deployment → ReplicaSet → Pods
- **Identify the problematic resource** in a degraded app instantly

#### Tabs inside Application Detail

**SUMMARY tab**
Shows: Source (Git repo, branch, path), Destination (cluster, namespace), Sync Policy, Last sync time, and commit hash.

**PARAMETERS tab (Helm/Kustomize apps)**
Shows all the Helm values or Kustomize parameters active for this app. For Helm apps, you can override values here directly (though it's better practice to update your `values.yaml` in Git).

**MANIFEST tab**
Shows the **diff** between what's in Git (desired) vs what's running in the cluster (live):

```diff
  spec:
    replicas: 2       # Live state (cluster)
-   replicas: 2
+   replicas: 3       # Desired state (Git) — OutOfSync!
```

This is incredibly useful for debugging — you can see *exactly* what has drifted.

**EVENTS tab**
Shows Kubernetes events related to this application's resources — pod scheduling failures, image pull errors, etc.

**LOGS tab**
Stream pod logs directly in the ArgoCD UI — no need to switch to `kubectl logs`.

**DIFF tab**
A coloured diff view showing what will change when you sync.

### 8.3 Settings Page

The Settings page has multiple sub-sections. Navigate via the left sidebar.

#### Repositories (Settings → Repositories)

**What:** Where you connect ArgoCD to your Git repositories.

**Why:** ArgoCD needs credentials to clone private repos.

**How to add a repository:**
1. Click **+ Connect Repo**
2. Choose connection method:
   - **HTTPS** — provide username + password or personal access token
   - **SSH** — provide SSH private key
   - **GitHub App** — use a GitHub App installation (recommended for organisations)

```bash
# Via CLI alternative:
argocd repo add https://github.com/myorg/myapp \
  --username myuser \
  --password mytoken
```

Once connected, the repo appears with a **CONNECTION STATUS: Successful** indicator.

#### Clusters (Settings → Clusters)

**What:** The Kubernetes clusters ArgoCD can deploy to.

**Why:** ArgoCD can manage multiple clusters from one control plane — one ArgoCD instance in a management cluster can deploy to dev, staging, and prod clusters.

**Default entry:** `in-cluster` — this is the cluster ArgoCD itself is running in (always available).

**Add an external cluster:**
```bash
# Add another cluster (kubeconfig must be configured for that cluster)
argocd cluster add my-production-cluster \
  --name production
```

#### Projects (Settings → Projects)

**What:** ArgoCD Projects are boundaries that group applications and restrict what they can do.

**Why:** In a team environment, you don't want the dev team accidentally deploying to production. Projects enforce:
- Which Git repos applications in this project can use
- Which clusters/namespaces applications can deploy to
- Which Kubernetes resource types are allowed/blocked

**Default project:** Every app belongs to the `default` project if not specified.

**Example: Create a restricted project**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-frontend
  namespace: argocd
spec:
  description: Frontend team applications

  # Only allow deploying from this GitHub org
  sourceRepos:
    - 'https://github.com/mycompany/frontend-*'

  # Only allow deploying to the frontend namespace in the prod cluster
  destinations:
    - namespace: frontend
      server: https://prod-cluster.mycompany.com

  # Block deploying ClusterRoles (security sensitive)
  clusterResourceBlacklist:
    - group: 'rbac.authorization.k8s.io'
      kind: ClusterRole
```

#### Accounts (Settings → Accounts)

**What:** Manage local ArgoCD users (in addition to the `admin` account).

**Why:** Create service accounts for CI/CD pipelines, or team members who don't use SSO.

```bash
# Create a new account via CLI
argocd account update-password --account ci-bot
```

#### RBAC (Settings → RBAC)

**What:** Defines who can do what in ArgoCD.

**Why:** Prevent developers from syncing production apps, or give read-only access to auditors.

ArgoCD uses a Casbin-style policy format:

```
# Format: p, <role/user>, <resource>, <action>, <object>, <allow/deny>
#
# Give the 'developer' role read access to all apps
p, role:developer, applications, get, */*, allow

# But only allow them to sync apps in the 'dev' project
p, role:developer, applications, sync, dev/*, allow

# Assign the developer role to a GitHub group
g, myorg:developers, role:developer
```

#### Certificates (Settings → Certificates)

**What:** TLS certificates for connecting to Git repositories or external clusters.

**Why:** When using self-signed certificates on internal GitLab/Gitea servers.

### 8.4 Notifications Bell (🔔)

Shows a history of sync events, errors, and warnings across all applications. Useful for quickly spotting:
- Apps that failed to sync
- Apps that recently went from Healthy → Degraded
- Apps that were manually synced (potential policy violations)

---

## 9. Creating Your First Application

Let's deploy a real application step by step — both via UI and YAML.

### 9.1 Via the Dashboard UI

1. Click **+ NEW APP** on the Applications page
2. Fill in the **General** section:
   - **Application Name:** `my-webapp`
   - **Project Name:** `default`
   - **Sync Policy:** `Manual` (for now)

3. Fill in the **Source** section:
   - **Repository URL:** `https://github.com/argoproj/argocd-example-apps`
   - **Revision:** `HEAD` (latest commit on default branch)
   - **Path:** `guestbook` (folder inside the repo)

4. Fill in the **Destination** section:
   - **Cluster URL:** `https://kubernetes.default.svc` (in-cluster)
   - **Namespace:** `default`

5. Click **CREATE**

ArgoCD will immediately show the app as **OutOfSync** (because nothing is deployed yet). Click **SYNC → SYNCHRONIZE** to deploy it.

### 9.2 Via YAML (GitOps way — recommended)

```yaml
# my-webapp-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-webapp
  namespace: argocd          # Application resources always go in argocd namespace
  # Finalizer: when you delete this Application, ArgoCD also deletes the deployed resources
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/argoproj/argocd-example-apps
    targetRevision: HEAD       # Branch, tag, or commit SHA
    path: guestbook            # Path within the repo

    # For Helm apps, add:
    # chart: my-chart
    # helm:
    #   valueFiles:
    #     - values-production.yaml
    #   parameters:
    #     - name: replicaCount
    #       value: "3"

    # For Kustomize apps, add:
    # kustomize:
    #   version: v5.0.0
    #   namePrefix: prod-

  destination:
    server: https://kubernetes.default.svc   # Target cluster
    namespace: default                        # Target namespace

  syncPolicy:
    automated:                    # Auto-sync when Git changes
      prune: true                 # Delete resources removed from Git
      selfHeal: true              # Re-sync if someone manually changes the cluster
    syncOptions:
      - CreateNamespace=true      # Create namespace if it doesn't exist
      - PrunePropagationPolicy=foreground  # Delete child resources first
    retry:
      limit: 5                    # Retry sync up to 5 times on failure
      backoff:
        duration: 5s              # Wait 5 seconds before retrying
        factor: 2                 # Double the wait each retry (5s, 10s, 20s...)
        maxDuration: 3m           # Never wait more than 3 minutes
```

Apply it:
```bash
kubectl apply -f my-webapp-application.yaml
```

---

## 10. Sync Policies — Manual vs Automatic

### Manual Sync

**What:** You must explicitly click "SYNC" or run `argocd app sync` to apply Git changes to the cluster.

**Why use it:**
- Production environments where you want human approval before deploying
- Apps where you're not yet confident in the automation
- Compliance requirements (change approval workflows)

```yaml
syncPolicy: {}  # Empty = manual sync
```

### Automatic Sync

**What:** ArgoCD syncs the cluster to Git whenever it detects a difference.

**Why use it:**
- Dev/staging environments where rapid iteration is needed
- When Git is truly the single source of truth and you trust CI/CD
- Microservices where many small deploys happen frequently

```yaml
syncPolicy:
  automated:
    prune: true      # IMPORTANT: Delete resources removed from Git
    selfHeal: true   # Re-sync if someone manually edits cluster resources
```

#### prune: true vs prune: false

**With `prune: false` (default):**
You delete a Deployment from Git → ArgoCD syncs but the old Deployment keeps running. App shows as OutOfSync forever.

**With `prune: true`:**
You delete a Deployment from Git → ArgoCD syncs and deletes the Deployment from the cluster.

> **Warning:** Enable prune carefully. If you accidentally delete something from Git, ArgoCD will delete it from production too.

#### selfHeal: true vs selfHeal: false

**With `selfHeal: false`:**
A developer runs `kubectl scale deployment my-app --replicas=10` in production.
ArgoCD notices the drift but doesn't fix it — the cluster stays at 10 replicas.

**With `selfHeal: true`:**
A developer runs `kubectl scale deployment my-app --replicas=10` in production.
ArgoCD notices the drift within minutes and scales it back to whatever is in Git.
This enforces immutable infrastructure.

---

## 11. Health Status & Sync Status Explained

### Sync Status

| Status | Icon | Meaning |
|---|---|---|
| **Synced** | ✅ | Cluster matches Git exactly |
| **OutOfSync** | ⚠️ | Cluster differs from Git (needs sync) |
| **Unknown** | ❓ | ArgoCD can't determine sync status (often Git connectivity issue) |

### Health Status

| Status | Icon | Meaning |
|---|---|---|
| **Healthy** | 💚 | All resources are running and ready |
| **Progressing** | 🔵 | Resources are being created/updated (e.g., rolling deployment in progress) |
| **Degraded** | 🔴 | Something is wrong — pods crashlooping, deployment stuck |
| **Suspended** | 🟡 | Resource is intentionally paused (e.g., CronJob suspended) |
| **Missing** | ⬜ | Resource defined in Git but doesn't exist in cluster |
| **Unknown** | ❓ | ArgoCD can't determine health (usually custom resources without health checks) |

### Combined States

The most common combinations you'll see and what they mean:

| Sync + Health | Meaning | Action |
|---|---|---|
| Synced + Healthy | 🎉 Perfect state | None |
| Synced + Progressing | Deployment rolling out | Wait |
| Synced + Degraded | App deployed but broken | Check pod logs |
| OutOfSync + Healthy | Git changed, cluster not updated | Sync when ready |
| OutOfSync + Degraded | Multiple problems | Fix Git, then sync |
| OutOfSync + Missing | Resource was deleted from cluster | Sync to restore |

---

## 12. ArgoCD CLI — Power User Commands

### App Management

```bash
# List all applications
argocd app list

# Get detailed status of an app
argocd app get my-webapp

# Sync an app (deploy latest from Git)
argocd app sync my-webapp

# Sync but don't prune (safe sync)
argocd app sync my-webapp --prune=false

# Sync a specific resource only (not the whole app)
argocd app sync my-webapp --resource apps:Deployment:my-webapp

# Hard refresh: bypass cache, re-clone Git repo
argocd app get my-webapp --hard-refresh

# Show the diff between Git and cluster
argocd app diff my-webapp

# Rollback to a previous revision
argocd app history my-webapp    # See revision history
argocd app rollback my-webapp 5  # Roll back to revision 5
```

### App Creation via CLI

```bash
# Create a plain YAML app
argocd app create guestbook \
  --repo https://github.com/argoproj/argocd-example-apps \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# Create a Helm app
argocd app create my-helm-app \
  --repo https://charts.bitnami.com/bitnami \
  --helm-chart nginx \
  --revision 15.0.0 \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace nginx \
  --helm-set replicaCount=2

# Create a Kustomize app
argocd app create my-kustomize-app \
  --repo https://github.com/myorg/myapp \
  --path overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production
```

### Cluster & Repo Management

```bash
# List connected clusters
argocd cluster list

# Add a cluster
argocd cluster add my-cluster-context-name

# List connected repos
argocd repo list

# Add a private GitHub repo with token
argocd repo add https://github.com/myorg/private-repo \
  --username not-used \
  --password ghp_yourPersonalAccessToken
```

---

## 13. Real-World Project Structure

Here is a production-grade GitOps repository structure:

```
infrastructure-gitops/
├── README.md
│
├── argocd/
│   ├── install/
│   │   ├── base/
│   │   │   └── kustomization.yaml        # Upstream ArgoCD manifests
│   │   └── overlays/
│   │       ├── dev/
│   │       │   └── kustomization.yaml
│   │       └── production/
│   │           ├── kustomization.yaml
│   │           └── patches/
│   │               ├── argocd-server.yaml
│   │               └── argocd-cm.yaml
│   │
│   └── apps/
│       ├── root-app.yaml                 # The "App of Apps" — manages all other apps
│       ├── team-frontend/
│       │   ├── frontend-app.yaml
│       │   └── frontend-project.yaml
│       └── team-backend/
│           ├── backend-app.yaml
│           └── backend-project.yaml
│
├── apps/
│   ├── frontend/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       │   ├── kustomization.yaml
│   │       │   └── replica-patch.yaml   # 1 replica in dev
│   │       └── production/
│   │           ├── kustomization.yaml
│   │           └── replica-patch.yaml   # 3 replicas in production
│   │
│   └── backend/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── values-production.yaml
│
└── clusters/
    ├── dev-cluster/
    │   └── apps.yaml                     # All apps targeting dev cluster
    └── production-cluster/
        └── apps.yaml                     # All apps targeting prod cluster
```

### The App of Apps Pattern

```yaml
# argocd/apps/root-app.yaml
# This single Application manages ALL other Applications
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/infrastructure-gitops
    targetRevision: HEAD
    path: argocd/apps           # Folder containing all Application YAMLs
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

With this pattern:
- You deploy only `root-app` manually once
- root-app discovers and deploys all other apps automatically
- Adding a new app = add its `Application` YAML to `argocd/apps/` and commit to Git
- ArgoCD picks it up within 3 minutes (or immediately on webhook)

---

## 14. Troubleshooting Common Issues

### Issue 1: App stuck in "Progressing"

**Symptom:** App shows Synced but Health = Progressing for more than 5 minutes.

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -n <app-namespace>

# Check pod events
kubectl describe pod <pod-name> -n <app-namespace>

# Check deployment rollout
kubectl rollout status deployment/<name> -n <app-namespace>
```

**Common causes:**
- Image pull error (`ImagePullBackOff`) — wrong image name/tag or no pull secret
- Resource quota exceeded — namespace is out of CPU/memory
- Liveness/readiness probe failing — app starts but health check fails

### Issue 2: "ComparisonError" or "OperationError"

**Symptom:** App shows an error badge, won't sync.

```bash
argocd app get my-webapp
# Look for "Message:" field — it usually has the exact error
```

**Common causes:**
- YAML syntax error in Git
- Kubernetes API version deprecated (e.g., using `extensions/v1beta1` Ingress on K8s 1.22+)
- Missing CRD (deploying a resource type that isn't installed)

### Issue 3: App keeps going OutOfSync even after sync

**Symptom:** You sync, it shows Synced, then goes OutOfSync within minutes.

**Common causes:**
1. **Annotation mutations** — some controllers (cert-manager, Helm) add annotations after deploy. Fix with `ignoreDifferences`:

```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/template/metadata/annotations/kubectl.kubernetes.io~1last-applied-configuration
```

2. **Replica count changed by HPA** — Horizontal Pod Autoscaler changes replicas dynamically:

```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

3. **Default values added by Kubernetes** — K8s adds default fields not in your YAML.

### Issue 4: Repository connection failed

```bash
argocd repo list
# Status: Failed

# Test connectivity
argocd repo get https://github.com/myorg/myapp

# Re-add with correct credentials
argocd repo rm https://github.com/myorg/myapp
argocd repo add https://github.com/myorg/myapp --username user --password token
```

### Issue 5: Can't access the UI

```bash
# Check argocd-server pod is running
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server

# Check logs for errors
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server

# Re-do port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

---

## 15. Security Best Practices

### 1. Change the admin password immediately

```bash
argocd account update-password
```

### 2. Disable admin account after setting up SSO

```yaml
# In argocd-cm ConfigMap:
data:
  admin.enabled: "false"
```

### 3. Enable SSO (GitHub, Google, LDAP)

```yaml
# argocd-cm ConfigMap
data:
  dex.config: |
    connectors:
      - type: github
        id: github
        name: GitHub
        config:
          clientID: $GITHUB_CLIENT_ID
          clientSecret: $GITHUB_CLIENT_SECRET
          orgs:
            - name: your-org
```

### 4. Use Projects to isolate teams

Never let all teams deploy to the `default` project with unrestricted access.

### 5. Limit ArgoCD's own RBAC

ArgoCD's service account needs cluster-admin to deploy arbitrary resources. Scope it down in security-sensitive environments using AppProject cluster resource allow/block lists.

### 6. Enable audit logging

```yaml
# argocd-cmd-params-cm ConfigMap
data:
  server.log.level: "info"
  server.log.format: "json"
```

Stream logs to your SIEM for audit trails.

### 7. Use Sealed Secrets or External Secrets for secrets in Git

Never commit plain Kubernetes Secrets to Git. Use:
- **Sealed Secrets** — encrypt secrets, store ciphertext in Git
- **External Secrets Operator** — pull secrets from AWS Secrets Manager, Vault, etc.

```bash
# Install sealed-secrets controller
helm install sealed-secrets \
  sealed-secrets/sealed-secrets \
  -n kube-system

# Seal a secret
kubeseal --format yaml < my-secret.yaml > my-sealed-secret.yaml
# my-sealed-secret.yaml is safe to commit to Git
```

---

## Quick Reference Cheatsheet

```bash
# ─── Installation ───────────────────────────────────────────────
kubectl apply -k argocd/overlays/production          # Kustomize install
helm install argocd argo/argo-cd -n argocd -f vals.yaml  # Helm install

# ─── Access ─────────────────────────────────────────────────────
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# ─── App Lifecycle ──────────────────────────────────────────────
argocd app list
argocd app get <app>
argocd app sync <app>
argocd app sync <app> --prune=false   # Safe sync
argocd app diff <app>
argocd app history <app>
argocd app rollback <app> <revision>
argocd app delete <app>

# ─── Troubleshooting ────────────────────────────────────────────
argocd app get <app>                    # See detailed status + error message
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server
```

---

*Guide covers ArgoCD v2.11+ | Kubernetes 1.25+ | Helm Chart 7.x | Kustomize 5.x*