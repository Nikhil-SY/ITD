Here are **solutions for Questions 21–30** in the same **interview-style format**.

---

# 21. Automate failed Kubernetes pod recovery using shell scripting and Kubernetes self-healing

## Objective

Automatically detect failed pods and recover them.

---

## Important concept: Kubernetes already does self-healing

If pod is managed by:

* Deployment
* ReplicaSet
* StatefulSet
* DaemonSet

Kubernetes automatically recreates failed pods.

Example:

```bash
kubectl delete pod mypod
```

Controller immediately creates new pod.

---

## When custom automation helps

Useful for:

* Detecting repeated failures (`CrashLoopBackOff`)
* Sending alerts
* Collecting logs before restart

---

## Script

```bash
#!/bin/bash

NAMESPACE=default

FAILED_PODS=$(kubectl get pods -n $NAMESPACE --no-headers | \
grep -E "CrashLoopBackOff|Error" | awk '{print $1}')

for POD in $FAILED_PODS
do
   echo "Recovering $POD"

   # Save logs before deleting
   kubectl logs $POD -n $NAMESPACE > /tmp/${POD}.log

   # Delete pod
   kubectl delete pod $POD -n $NAMESPACE
done
```

---

## Explanation

### Detect unhealthy pods

```bash
kubectl get pods
```

---

### Save logs

Important for RCA (Root Cause Analysis).

---

### Delete pod

Kubernetes recreates new healthy pod.

---

## Better production approach

Use:

* Liveness probes
* Readiness probes
* Prometheus alerts

---

## Benefits

* Faster recovery
* Automatic remediation
* Less downtime

---

# 22. Automate AWS EBS snapshot creation using Python and Boto3

## Objective

Create automatic EBS snapshots for backup.

---

## Python Script

```python
import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

VOLUME_ID = "vol-xxxxxxxx"

response = ec2.create_snapshot(
    VolumeId=VOLUME_ID,
    Description=f"Automated backup {datetime.now()}"
)

print("Snapshot created:", response['SnapshotId'])
```

---

## Explanation

### Connect to EC2

```python
boto3.client('ec2')
```

---

### Create snapshot

```python
create_snapshot()
```

AWS creates point-in-time backup.

---

## Automation options

Schedule using:

* Cron
* AWS Lambda + EventBridge (**preferred**)

---

## Retention cleanup

Delete old snapshots:

```python
ec2.delete_snapshot(SnapshotId='snap-id')
```

---

## Benefits

* Disaster recovery
* Automated backups
* No manual effort

---

# 23. Implement Kubernetes Horizontal Pod Autoscaling (HPA) based on CPU

## Objective

Automatically scale pods based on CPU usage.

---

## Requirements

Install metrics server:

```bash
kubectl get deployment metrics-server -n kube-system
```

---

## Deployment must define CPU requests

```yaml
resources:
  requests:
    cpu: "200m"
```

Without this HPA will not work.

---

## Create HPA

```bash
kubectl autoscale deployment myapp \
--cpu-percent=70 \
--min=2 \
--max=10
```

---

## YAML method

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Check HPA

```bash
kubectl get hpa
```

---

## Benefits

* Auto scaling
* Cost optimization
* Better availability

---

# 24. Automate SSL certificate renewal using Certbot in Linux

## Objective

Renew Let's Encrypt certificates automatically.

---

## Manual renewal command

```bash
certbot renew
```

---

## Automated Cron

```bash
0 3 * * * certbot renew --quiet
```

Runs daily at 3 AM.

---

## Verify renewal

```bash
certbot certificates
```

---

## Reload web server after renewal

```bash
certbot renew --deploy-hook "systemctl reload nginx"
```

---

## Benefits

* Prevents certificate expiry
* Zero downtime renewal

---

# 25. Automate Jenkins pipeline failure notifications using email alerts

## Objective

Notify team when Jenkins build fails.

---

## Jenkinsfile example

```groovy
post {
    failure {
        mail to: 'team@example.com',
        subject: "Build Failed: ${env.JOB_NAME}",
        body: "Check Jenkins build ${env.BUILD_URL}"
    }
}
```

---

## Explanation

### `post`

Runs after pipeline completion.

---

### `failure`

Only triggers when build fails.

---

### `mail`

Sends email alert.

---

## Configure SMTP in Jenkins

Go to:

```text
Manage Jenkins → Configure System → E-mail Notification
```

---

## Benefits

* Immediate awareness
* Faster issue resolution

---

# 26. Automate Kubernetes cluster configuration backups regularly

## Objective

Backup Kubernetes YAML configurations.

---

## Backup command

```bash
kubectl get all --all-namespaces -o yaml > cluster_backup.yaml
```

---

## Full backup script

```bash
#!/bin/bash

BACKUP_DIR=/backup/k8s
DATE=$(date +%F)

mkdir -p $BACKUP_DIR

kubectl get all --all-namespaces -o yaml \
> $BACKUP_DIR/cluster_$DATE.yaml
```

---

## For etcd backup (control plane)

```bash
etcdctl snapshot save etcd-backup.db
```

Critical for full cluster recovery.

---

## Benefits

* Disaster recovery
* Restore cluster state

---

# 27. Automate Docker container health monitoring

## Objective

Detect unhealthy containers automatically.

---

## Healthcheck in Dockerfile

```dockerfile
HEALTHCHECK CMD curl -f http://localhost:8080 || exit 1
```

---

## Monitor script

```bash
#!/bin/bash

docker ps --format "{{.Names}}" | while read CONTAINER
do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER)

  if [ "$STATUS" = "unhealthy" ]; then
      docker restart $CONTAINER
  fi
done
```

---

## Benefits

* Automatic recovery
* Better uptime

---

# 28. Automate deletion of old backup files based on retention

## Objective

Delete backup files older than defined period.

---

## Script

```bash
#!/bin/bash

BACKUP_DIR="/backup"
RETENTION=30

find $BACKUP_DIR -type f -mtime +$RETENTION -delete
```

---

## Explanation

### `mtime +30`

Older than 30 days.

---

## Benefits

* Saves storage
* Enforces retention policy

---

# 29. Implement blue-green deployment in Kubernetes

## Objective

Deploy new version without downtime.

---

## Blue deployment

```yaml
app: myapp
version: blue
```

---

## Green deployment

```yaml
app: myapp
version: green
```

---

## Service initially points to blue

```yaml
selector:
  app: myapp
  version: blue
```

---

## Switch traffic to green

Change service selector:

```yaml
selector:
  app: myapp
  version: green
```

Apply:

```bash
kubectl apply -f service.yaml
```

---

## Benefits

* Zero downtime
* Easy rollback
* Safe releases

---

# 30. Automate cleanup of unused AWS snapshots to reduce costs

## Objective

Delete old EBS snapshots.

---

## Python Script

```python
import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

for snap in snapshots:
    age = datetime.now(timezone.utc) - snap['StartTime']

    if age.days > 30:
        ec2.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        print("Deleted", snap['SnapshotId'])
```

---

## Explanation

### Get snapshots

```python
describe_snapshots()
```

---

### Check age

Older than 30 days.

---

### Delete snapshot

```python
delete_snapshot()
```

---

## Benefits

* Reduces AWS bill
* Automated cost optimization

---

# Interview Tip (21–30)

Strong answer pattern:

```text
Problem
→ Automation tool
→ Script/YAML
→ Scheduling
→ Monitoring
→ Benefits
```

This sounds professional in DevOps interviews.
