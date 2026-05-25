here are **solutions for Questions 11–20**.

---

# 11. Automate restarting failed services (Nginx/Apache) in Linux

## Objective

Automatically detect if a service (like **Nginx** or **Apache**) has stopped and restart it.

---

## Approach

* Check service status
* If inactive → restart service
* Log the action
* Schedule via **cron**

---

## Script (Bash)

```bash
#!/bin/bash

SERVICE="nginx"
LOG_FILE="/var/log/service_monitor.log"

STATUS=$(systemctl is-active $SERVICE)

if [ "$STATUS" != "active" ]; then
    echo "$(date): $SERVICE is down. Restarting..." >> $LOG_FILE
    systemctl restart $SERVICE
    echo "$(date): $SERVICE restarted." >> $LOG_FILE
fi
```

---

## Explanation

### Check service status

```bash
systemctl is-active nginx
```

Possible outputs:

* active
* inactive
* failed

---

### Restart service

```bash
systemctl restart nginx
```

---

## Cron schedule

```bash
*/5 * * * * /home/nikhil/service_monitor.sh
```

Checks every **5 minutes**.

---

## Benefits

* Automatic recovery
* Reduced downtime
* No manual intervention

---

# 12. Automate temporary Kubernetes namespace cleanup

## Objective

Delete temporary namespaces (dev/test/feature namespaces) after expiry.

---

## Example

Namespaces:

```text
test-feature1
test-feature2
temp-dev
```

---

## Script

```bash
#!/bin/bash

for ns in $(kubectl get ns --no-headers | awk '{print $1}' | grep "^test-")
do
   echo "Deleting namespace: $ns"
   kubectl delete namespace $ns
done
```

---

## Explanation

### List namespaces

```bash
kubectl get ns
```

---

### Filter temporary namespaces

```bash
grep "^test-"
```

Only namespaces starting with `test-`.

---

### Delete namespace

```bash
kubectl delete namespace <name>
```

---

## Safer production approach

Use label-based deletion:

```bash
kubectl get ns -l cleanup=true
```

Much safer than name matching.

---

## Benefits

* Frees cluster resources
* Avoids namespace clutter
* Saves cloud cost

---

# 13. Automate backup file uploads to AWS S3

## Objective

Upload backups automatically to **Amazon S3**.

---

## Script (AWS CLI)

```bash
#!/bin/bash

BACKUP_DIR="/backup"
BUCKET="s3://my-company-backups"

aws s3 sync $BACKUP_DIR $BUCKET
```

---

## Explanation

### Sync files

```bash
aws s3 sync
```

Uploads only changed/new files.

---

### Example

Local:

```text
/backup/db_backup.sql
```

Uploaded to:

```text
s3://my-company-backups/db_backup.sql
```

---

## Add timestamped archive

```bash
tar -czf backup_$(date +%F).tar.gz /backup
aws s3 cp backup_$(date +%F).tar.gz $BUCKET
```

---

## Benefits

* Offsite backup
* Disaster recovery
* Highly durable storage

---

# 14. Automate Terraform provisioning for multiple environments

## Objective

Provision infrastructure separately for:

* dev
* test
* prod

---

## Folder structure

```text
terraform/
 ├── modules/
 ├── dev/
 ├── test/
 └── prod/
```

---

## Example variable file

### `dev.tfvars`

```hcl
instance_type = "t2.micro"
```

### `prod.tfvars`

```hcl
instance_type = "t3.large"
```

---

## Deployment command

```bash
terraform init
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

---

## Automation script

```bash
#!/bin/bash

ENV=$1

terraform init
terraform apply -var-file=${ENV}.tfvars -auto-approve
```

Usage:

```bash
./deploy.sh prod
```

---

## Benefits

* Reusable code
* Environment consistency
* Faster provisioning

---

# 15. Automate Kubernetes rollout restart after config changes

## Objective

Restart pods after ConfigMap/Secret changes without downtime.

---

## Command

```bash
kubectl rollout restart deployment myapp
```

---

## Script

```bash
#!/bin/bash

kubectl apply -f configmap.yaml
kubectl rollout restart deployment myapp
kubectl rollout status deployment myapp
```

---

## Explanation

### Apply config change

```bash
kubectl apply -f configmap.yaml
```

---

### Restart pods gradually

```bash
kubectl rollout restart deployment myapp
```

Kubernetes performs **rolling update**:

* Old pod terminated one by one
* New pod starts
* Zero downtime

---

## Benefits

* Picks up config changes
* No manual pod deletion
* Zero downtime deployment

---

# 16. Automate cleanup of merged Git branches

## Objective

Delete local branches already merged into main.

---

## Script

```bash
#!/bin/bash

git checkout main
git pull

git branch --merged | grep -v "\*\|main" | xargs git branch -d
```

---

## Explanation

### Find merged branches

```bash
git branch --merged
```

---

### Exclude current branch and main

```bash
grep -v "\*\|main"
```

---

### Delete branches

```bash
git branch -d
```

---

## Benefits

* Clean repository
* Easier navigation
* Removes stale branches

---

# 17. Automate MySQL database backups with retention policy

## Objective

Backup MySQL daily and delete old backups.

---

## Script

```bash
#!/bin/bash

DB_NAME="mydb"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%F)

mkdir -p $BACKUP_DIR

mysqldump -u root -pMyPassword $DB_NAME > $BACKUP_DIR/${DB_NAME}_$DATE.sql

find $BACKUP_DIR -type f -mtime +7 -delete
```

---

## Explanation

### Create dump

```bash
mysqldump
```

Exports SQL backup.

---

### Retention cleanup

```bash
find ... -mtime +7
```

Deletes backups older than 7 days.

---

## Cron

```bash
0 1 * * * /home/nikhil/mysql_backup.sh
```

---

## Benefits

* Automated DB protection
* Fast restore capability

---

# 18. Monitor Kubernetes node health automatically

## Objective

Detect unhealthy cluster nodes.

---

## Basic command

```bash
kubectl get nodes
```

Possible statuses:

* Ready
* NotReady
* Unknown

---

## Script

```bash
#!/bin/bash

NOT_READY=$(kubectl get nodes --no-headers | grep -v " Ready ")

if [ ! -z "$NOT_READY" ]; then
   echo "Unhealthy nodes detected:"
   echo "$NOT_READY"
fi
```

---

## Better production tools

Use:

* **Prometheus**
* **Node Exporter**
* **Grafana**
* **Alertmanager**

---

## Important metrics

Monitor:

* CPU
* Memory
* Disk pressure
* Network
* Node Ready status

---

## Benefits

* Early failure detection
* Prevents application impact

---

# 19. Automate application health checks using HTTP status monitoring

## Objective

Check application endpoint health continuously.

---

## Script

```bash
#!/bin/bash

URL="https://myapp.com/health"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ "$STATUS" != "200" ]; then
   echo "Application unhealthy. Status: $STATUS"
fi
```

---

## Explanation

### Curl HTTP status

```bash
curl -w "%{http_code}"
```

Returns:

* 200 → healthy
* 500 → server error
* 404 → not found

---

## Health endpoint example

```text
/health
/actuator/health
/status
```

---

## Benefits

* Quick app validation
* Detect outages immediately

---

# 20. Monitor cron service health and job execution

## Objective

Ensure:

* Cron daemon is running
* Scheduled jobs execute successfully

---

## Check cron service

```bash
systemctl status cron
```

or

```bash
systemctl status crond
```

---

## Script

```bash
#!/bin/bash

SERVICE="cron"

if ! systemctl is-active --quiet $SERVICE; then
   echo "Cron service is down!"
fi
```

---

## Monitor job execution logs

Linux cron logs:

```bash
grep CRON /var/log/syslog
```

or

```bash
grep CRON /var/log/cron
```

---

## Best practice for cron jobs

Redirect output:

```bash
0 2 * * * /home/nikhil/backup.sh >> /var/log/backup.log 2>&1
```

This helps verify execution.

---

## Benefits

* Detect failed scheduled jobs
* Ensure automation reliability

---

# Quick Interview Pattern for Questions 11–20

Use this answer structure:

```text
1. Problem statement
2. Tool/command used
3. Script explanation
4. Scheduling method
5. Monitoring/logging
6. Benefits
```

This makes your DevOps interview answers clear and professional.
