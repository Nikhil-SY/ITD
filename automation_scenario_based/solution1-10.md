You want **solutions for questions 1–10**, with **detailed explanation**, and you prefer **interview-style structured answers**. I’ll follow that format.

---

# 1. Automate Linux log cleanup (delete logs older than 7 days)

## Objective

Automatically delete old log files to prevent disk space issues in production servers.

---

## Approach

* Identify log directory (`/var/log/myapp`)
* Find files older than 7 days
* Delete them safely
* Log cleanup activity
* Schedule using **cron**

---

## Script (Bash)

```bash
#!/bin/bash

LOG_DIR="/var/log/myapp"
RETENTION_DAYS=7
CLEANUP_LOG="/var/log/log_cleanup.log"

echo "Cleanup started at $(date)" >> $CLEANUP_LOG

find $LOG_DIR -type f -name "*.log" -mtime +$RETENTION_DAYS -print -delete >> $CLEANUP_LOG 2>&1

echo "Cleanup completed at $(date)" >> $CLEANUP_LOG
```

---

## Explanation

### `find`

Searches files.

### `-type f`

Only files.

### `-name "*.log"`

Only log files.

### `-mtime +7`

Files older than 7 days.

### `-print`

Shows deleted file names.

### `-delete`

Deletes files.

---

## Schedule using Cron

```bash
crontab -e
```

Add:

```bash
0 2 * * * /home/nikhil/log_cleanup.sh
```

### Meaning

Runs every day at **2 AM**.

---

## Benefits

* Prevents disk full issues
* Fully automated
* Saves manual effort
* Keeps server healthy

---

# 2. Automate Jenkins backup for disaster recovery

## Objective

Take regular backups of Jenkins configuration and jobs.

---

## Important Jenkins data to backup

Usually:

```bash
/var/lib/jenkins/
```

Contains:

* Jobs
* Plugins
* Credentials
* Pipeline configs
* User settings

---

## Backup Script

```bash
#!/bin/bash

BACKUP_DIR="/backup/jenkins"
DATE=$(date +%F_%H-%M)

mkdir -p $BACKUP_DIR

tar -czf $BACKUP_DIR/jenkins_backup_$DATE.tar.gz /var/lib/jenkins

find $BACKUP_DIR -type f -mtime +7 -delete
```

---

## Explanation

### `tar -czf`

Creates compressed archive.

### `mkdir -p`

Creates backup folder if not present.

### `mtime +7`

Deletes backups older than 7 days.

---

## Schedule

```bash
0 1 * * * /home/nikhil/jenkins_backup.sh
```

Daily at 1 AM.

---

## Disaster Recovery

To restore:

```bash
systemctl stop jenkins
tar -xzf backup.tar.gz -C /
systemctl start jenkins
```

---

## Benefits

* Fast recovery
* Protects pipelines
* Prevents configuration loss

---

# 3. Automate unhealthy Kubernetes pod detection and recovery

## Objective

Detect CrashLoopBackOff pods and recover automatically.

---

## Script

```bash
#!/bin/bash

NAMESPACE=default

pods=$(kubectl get pods -n $NAMESPACE --no-headers | grep CrashLoopBackOff | awk '{print $1}')

for pod in $pods
do
  echo "Restarting $pod"
  kubectl delete pod $pod -n $NAMESPACE
done
```

---

## How it works

### Check pod status

```bash
kubectl get pods
```

Looks for:

```text
CrashLoopBackOff
```

---

### Delete pod

```bash
kubectl delete pod
```

Deployment recreates new healthy pod automatically.

---

## Better production solution

Use:

* Liveness probes
* Readiness probes
* Prometheus alerts
* Kubernetes self-healing

---

## Benefits

* Faster recovery
* Reduced downtime
* Less manual monitoring

---

# 4. Automate disk space monitoring and alerting

## Objective

Send alert when disk usage exceeds threshold.

---

## Script

```bash
#!/bin/bash

THRESHOLD=80
EMAIL="admin@example.com"

USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ $USAGE -gt $THRESHOLD ]; then
   echo "Disk usage is $USAGE%" | mail -s "Disk Alert" $EMAIL
fi
```

---

## Explanation

### `df /`

Shows filesystem usage.

### `awk`

Extracts usage percentage.

### `if`

Checks threshold.

### `mail`

Sends email alert.

---

## Cron

```bash
*/10 * * * * /home/nikhil/disk_monitor.sh
```

Checks every 10 minutes.

---

## Benefits

* Prevents outages
* Early warning
* Easy monitoring

---

# 5. Automate Docker cleanup safely

## Objective

Remove unused Docker resources.

---

## Script

```bash
#!/bin/bash

docker container prune -f
docker image prune -a -f
docker volume prune -f
docker network prune -f
```

---

## Explanation

### Remove stopped containers

```bash
docker container prune
```

---

### Remove unused images

```bash
docker image prune -a
```

---

### Remove unused volumes

```bash
docker volume prune
```

---

### Remove unused networks

```bash
docker network prune
```

---

## Safer alternative

Check first:

```bash
docker system df
```

---

## Benefits

* Saves disk space
* Prevents server issues

---

# 6. Automate AWS EC2 start/stop using Python + Boto3

## Objective

Save cost by stopping unused EC2 instances.

---

## Python Script

```python
import boto3

ec2 = boto3.client('ec2', region_name='ap-south-1')

response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:AutoStop',
            'Values': ['true']
        }
    ]
)

instance_ids = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_ids.append(instance['InstanceId'])

if instance_ids:
    ec2.stop_instances(InstanceIds=instance_ids)
    print("Stopped:", instance_ids)
```

---

## Explanation

### Connect to EC2

```python
boto3.client('ec2')
```

---

### Filter by tag

Only instances tagged:

```text
AutoStop=true
```

---

### Stop instances

```python
stop_instances()
```

---

## Schedule

Use:

* Cron
* AWS Lambda + EventBridge

Preferred in cloud: **Lambda + EventBridge**

---

## Benefits

* Cost optimization
* Fully automated

---

# 7. Automate SSL certificate expiry checking and renewal

## Objective

Check certificate expiry and renew before expiration.

---

## Check expiry script

```bash
#!/bin/bash

DOMAIN="example.com"

echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | \
openssl x509 -noout -dates
```

---

## For Let's Encrypt renewal

```bash
certbot renew --quiet
```

---

## Cron

```bash
0 3 * * * certbot renew --quiet
```

---

## Optional alert

Check days remaining and send email if < 30 days.

---

## Benefits

* Prevents certificate expiry outage
* Automatic renewal

---

# 8. Automate Linux user creation during employee onboarding

## Objective

Automatically create users.

---

## Script

```bash
#!/bin/bash

USERNAME=$1

sudo useradd -m $USERNAME
sudo passwd $USERNAME
sudo usermod -aG developers $USERNAME

echo "User created successfully"
```

---

## Explanation

### Create user

```bash
useradd -m
```

Creates home directory.

---

### Set password

```bash
passwd
```

---

### Add to group

```bash
usermod -aG
```

---

## Example

```bash
./create_user.sh john
```

---

## Benefits

* Faster onboarding
* Standardized permissions

---

# 9. Automated CI/CD pipeline using Jenkins for Kubernetes deployments

## Objective

Build, test, Dockerize, and deploy application to Kubernetes.

---

## Pipeline Flow

```text
Git push
→ Jenkins build
→ Unit test
→ Docker build
→ Push to Docker Hub
→ Deploy to Kubernetes
```

---

## Jenkinsfile

```groovy
pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'mvn clean package'
      }
    }

    stage('Docker Build') {
      steps {
        sh 'docker build -t myapp:${BUILD_NUMBER} .'
      }
    }

    stage('Push Image') {
      steps {
        sh 'docker push myapp:${BUILD_NUMBER}'
      }
    }

    stage('Deploy') {
      steps {
        sh 'kubectl apply -f deployment.yaml'
      }
    }
  }
}
```

---

## Benefits

* Automated deployment
* Faster releases
* Reduced human error

---

# 10. Automate CPU utilization monitoring and alerting

## Objective

Alert when CPU usage exceeds threshold.

---

## Script

```bash
#!/bin/bash

THRESHOLD=80

CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}' | cut -d'.' -f1)

if [ $CPU -gt $THRESHOLD ]; then
   echo "High CPU usage: $CPU%"
fi
```

---

## Explanation

### `top -bn1`

Gets current CPU stats.

---

### `100 - idle`

CPU used = 100 - idle.

---

### Threshold check

```bash
if [ $CPU -gt 80 ]
```

---

## Production-grade tools

Better use:

* **Prometheus**
* **Node Exporter**
* **Grafana**
* **Alertmanager**

---

## Benefits

* Early issue detection
* Prevent performance degradation

---

# Interview Tip

For each automation question, explain using this formula:

```text
Objective
→ Tool used
→ Script logic
→ Scheduling method
→ Monitoring/Alerting
→ Benefits
```

This sounds very strong in DevOps interviews.
