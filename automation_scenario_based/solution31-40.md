Here are **solutions for Questions 31–40** in the same **detailed interview-style format**.

---

# 31. Automate Nginx configuration validation before restarting the service

## Objective

Validate Nginx config before restart to avoid downtime due to bad configuration.

---

## Problem

If you directly restart:

```bash
systemctl restart nginx
```

…and config has syntax error → **Nginx will fail to start** → website goes down.

---

## Solution Script

```bash
#!/bin/bash

echo "Validating Nginx config..."

nginx -t

if [ $? -eq 0 ]; then
    echo "Config valid. Restarting Nginx..."
    systemctl restart nginx
else
    echo "Config invalid. Restart aborted."
fi
```

---

## Explanation

### Test config

```bash
nginx -t
```

Checks:

* Syntax errors
* Missing files
* Invalid directives

---

### Check exit status

```bash
$?
```

* `0` = success
* non-zero = failure

---

## Better option: reload instead of restart

```bash
systemctl reload nginx
```

Reload applies config without downtime.

---

## Benefits

* Prevents accidental outage
* Safe deployment practice

---

# 32. Automate Kubernetes pod CPU and memory usage monitoring

## Objective

Monitor pod resource usage continuously.

---

## Basic command

```bash
kubectl top pods
```

Example:

```text
myapp-abc   120m   200Mi
```

---

## Script

```bash
#!/bin/bash

OUTPUT=$(kubectl top pods)

echo "$OUTPUT" > /tmp/pod_usage.log
echo "$OUTPUT"
```

---

## Filter high CPU pods

```bash
kubectl top pods | sort -k2 -nr
```

---

## Requirements

Metrics server must be installed:

```bash
kubectl get deployment metrics-server -n kube-system
```

---

## Production tools

Better monitoring:

* Prometheus
* Grafana
* Alertmanager

---

## Benefits

* Capacity planning
* Detect resource bottlenecks

---

# 33. Automate Linux server patching and security updates

## Objective

Keep Linux servers updated automatically.

---

## Ubuntu/Debian

```bash
apt update
apt upgrade -y
```

---

## Automation Script

```bash
#!/bin/bash

apt update
apt upgrade -y
apt autoremove -y
```

---

## Schedule

```bash
0 2 * * 0 /home/nikhil/patch.sh
```

Weekly Sunday at 2 AM.

---

## RHEL/CentOS

```bash
yum update -y
```

or

```bash
dnf update -y
```

---

## Safer production practice

Use:

```bash
apt list --upgradable
```

Review before patching.

---

## Benefits

* Security compliance
* Vulnerability reduction

---

# 34. Automate file synchronization between Linux servers using `rsync`

## Objective

Keep files synchronized between servers.

---

## Basic command

```bash
rsync -avz /data/ user@server2:/data/
```

---

## Script

```bash
#!/bin/bash

SOURCE="/data/"
DEST="user@server2:/data/"

rsync -avz --delete $SOURCE $DEST
```

---

## Explanation

### `-a`

Archive mode.

---

### `-v`

Verbose.

---

### `-z`

Compression.

---

### `--delete`

Removes files on destination if deleted in source.

---

## Passwordless automation

Use SSH keys:

```bash
ssh-keygen
ssh-copy-id user@server2
```

---

## Benefits

* Fast sync
* Incremental transfer
* Disaster recovery

---

# 35. Automate memory utilization monitoring and threshold alerting

## Objective

Alert when RAM usage exceeds threshold.

---

## Script

```bash
#!/bin/bash

THRESHOLD=80

USED=$(free | awk '/Mem:/ {printf("%.0f"), $3/$2 * 100}')

if [ $USED -gt $THRESHOLD ]; then
   echo "Memory usage high: $USED%"
fi
```

---

## Explanation

### Check memory

```bash
free
```

---

### Calculate usage %

```bash
$3/$2 * 100
```

Used / total memory.

---

## Cron

```bash
*/5 * * * * /home/nikhil/memory_monitor.sh
```

Every 5 minutes.

---

## Benefits

* Prevent OOM issues
* Early warning

---

# 36. Automate Docker image builds using GitLab CI/CD

## Objective

Build Docker images automatically after code push.

---

## `.gitlab-ci.yml`

```yaml
stages:
  - build

build_image:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push myapp:$CI_COMMIT_SHA
```

---

## Explanation

### Trigger

Runs automatically on Git push.

---

### Build image

```bash
docker build
```

---

### Push image

```bash
docker push
```

---

## Requirements

GitLab Runner must support Docker.

---

## Benefits

* Automated image creation
* Faster delivery

---

# 37. Automate Kubernetes ConfigMap updates dynamically

## Objective

Update app configuration without manual pod deletion.

---

## Update ConfigMap

```bash
kubectl apply -f configmap.yaml
```

---

## Restart deployment

```bash
kubectl rollout restart deployment myapp
```

---

## Script

```bash
#!/bin/bash

kubectl apply -f configmap.yaml
kubectl rollout restart deployment myapp
```

---

## Advanced dynamic reload

Use:

* Reloader operator
* Sidecar config reloaders

Example:

**Stakater Reloader**

Automatically restarts pods when ConfigMap changes.

---

## Benefits

* Easy config management
* Faster updates

---

# 38. Automate monitoring of failed SSH login attempts

## Objective

Detect brute-force attacks.

---

## Check logs

Ubuntu:

```bash
grep "Failed password" /var/log/auth.log
```

RHEL:

```bash
grep "Failed password" /var/log/secure
```

---

## Script

```bash
#!/bin/bash

COUNT=$(grep "Failed password" /var/log/auth.log | wc -l)

if [ $COUNT -gt 10 ]; then
   echo "Possible SSH attack detected"
fi
```

---

## Better protection

Use:

```bash
fail2ban
```

Automatically blocks attacker IPs.

---

## Benefits

* Security monitoring
* Attack detection

---

# 39. Automate cleanup of evicted Kubernetes pods

## Objective

Delete old **Evicted** pods.

---

## Problem

Evicted pods stay in cluster and clutter output:

```bash
kubectl get pods
```

---

## Cleanup command

```bash
kubectl get pods --all-namespaces | \
grep Evicted | \
awk '{print $2 " -n " $1}' | \
xargs -L1 kubectl delete pod
```

---

## Safer script

```bash
#!/bin/bash

kubectl get pods --all-namespaces \
--field-selector=status.phase=Failed
```

Then filter for evicted pods.

---

## Benefits

* Cleaner cluster
* Easier troubleshooting

---

# 40. Automate service availability and network reachability monitoring using shell scripting

## Objective

Check if services and network endpoints are reachable.

---

## Ping check

```bash
ping -c 3 google.com
```

---

## Port check

```bash
nc -zv myserver 443
```

---

## HTTP check

```bash
curl -I https://myapp.com
```

---

## Combined monitoring script

```bash
#!/bin/bash

HOST="myapp.com"

if ping -c 2 $HOST > /dev/null; then
    echo "Host reachable"
else
    echo "Host unreachable"
fi

STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$HOST)

if [ "$STATUS" != "200" ]; then
    echo "Application issue detected"
fi
```

---

## Explanation

### `ping`

Tests network connectivity.

---

### `curl`

Tests application availability.

---

### `nc`

Tests specific ports.

---

## Benefits

* Detect outages quickly
* Basic service monitoring

---

# Final Interview Tip (31–40)

For every automation question, answer in this flow:

```text
1. Objective
2. Problem
3. Script/YAML
4. Command explanation
5. Scheduling/automation method
6. Benefits
7. Better production alternative
```

This structure sounds strong and professional for **DevOps Engineer interviews**.
