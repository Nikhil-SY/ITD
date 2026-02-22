---

# 🎯 What is `os` Module in Python?

`os` module provides a way to:

* Interact with the **Operating System**
* Work with files & directories
* Manage environment variables
* Execute system commands
* Handle paths

It acts as a bridge between:

```text
Python Script  ↔  Operating System
```

Used heavily in DevOps automation.

---

# 🔹 1️⃣ os.getcwd() – Get Current Directory

```python
import os

print(os.getcwd())
```

### ✅ Output:

```
/home/nikhil/project
```

### 🔥 DevOps Use Case:

Before running deployment script, check current working directory.

---

# 🔹 2️⃣ os.chdir() – Change Directory

```python
import os

os.chdir("/var/log")
print(os.getcwd())
```

### ✅ Output:

```
/var/log
```

### 🔥 Real Use Case:

Move into build workspace before executing scripts.

---

# 🔹 3️⃣ os.listdir() – List Files

```python
import os

print(os.listdir())
```

### ✅ Output:

```
['file1.txt', 'deploy.sh', 'config.yml']
```

### 🔥 Use Case:

Loop through log files and archive them.

---

# 🔹 4️⃣ os.mkdir() – Create Directory

```python
import os

os.mkdir("backup")
```

Creates folder `backup`.

### 🔥 DevOps Use Case:

Create dynamic build folder:

```
backup_2026_02_21
```

---

# 🔹 5️⃣ os.makedirs() – Create Nested Directory

```python
os.makedirs("logs/app/2026", exist_ok=True)
```

### Use Case:

Create structured log folders automatically.

---

# 🔹 6️⃣ os.remove() – Delete File

```python
os.remove("old.log")
```

### Use Case:

Auto-clean old logs in cron job.

---

# 🔹 7️⃣ os.rmdir() – Remove Empty Directory

```python
os.rmdir("backup")
```

---

# 🔹 8️⃣ os.system() – Run Shell Command

```python
import os

os.system("ls -l")
```

### Output:

```
total 0
-rw-r--r-- file1.txt
```

⚠ Not recommended for advanced usage → use `subprocess`.

### DevOps Use Case:

Restart service:

```python
os.system("sudo systemctl restart nginx")
```

---

# 🔹 9️⃣ os.environ – Environment Variables

```python
import os

print(os.environ["HOME"])
```

### Output:

```
/home/nikhil
```

### DevOps Use Case:

Read AWS credentials:

```python
aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
```

---

# 🔹 🔟 os.path – Work with Paths

### Check if file exists

```python
import os

print(os.path.exists("config.yml"))
```

### Output:

```
True
```

### Get absolute path

```python
print(os.path.abspath("config.yml"))
```

---

# 🔥 Real DevOps Automation Example

## 🎯 Problem:

Delete all `.log` files older than 7 days.

## ✅ Solution:

```python
import os
import time

path = "/var/log/myapp"

now = time.time()

for file in os.listdir(path):
    full_path = os.path.join(path, file)

    if os.path.isfile(full_path):
        file_age = now - os.path.getmtime(full_path)

        if file_age > 7 * 86400:
            os.remove(full_path)
            print(f"Deleted {file}")
```

### 💡 Real Use Case:

Auto log rotation for production server.

---

# 🔥 Another Real Example (CI/CD Use Case)

## 🎯 Problem:

Create build directory dynamically.

```python
import os
from datetime import datetime

build_name = datetime.now().strftime("build_%Y%m%d_%H%M")

os.makedirs(build_name)

print(f"{build_name} created")
```

Used in:

* Jenkins pipeline scripts
* Deployment automation

---

# 🎯 Interview Summary Answer

`os` module allows:

* File & directory manipulation
* Environment variable access
* Running OS commands
* Cross-platform path handling

Used in:

* CI/CD automation
* Log cleanup
* Deployment scripts
* Server health checks

---

# 🔥 Advanced DevOps Tip

For production scripts:

Instead of:

```python
os.system()
```

Use:

```python
import subprocess
```

More secure and controllable.

---

If you want next, I can explain:

* Difference between `os` vs `subprocess`
* Real CI/CD pipeline Python automation script
* How to combine os + boto3 for AWS automation
* Mini DevOps project using Python

Tell me 👌🔥




#########################OS + Boto3##################################
Excellent Nikhil 👌🔥
Now we’re entering **real DevOps automation level**.

You already have AWS + DevOps background, so this is very useful for interviews and real projects.

---

# 🎯 What is boto3?

`boto3` = Official Python SDK for
Amazon Web Services

It allows Python to:

* Create EC2 instances
* Manage S3 buckets
* Restart servers
* Manage IAM roles
* Automate infrastructure

---

# 🎯 Why Combine `os` + `boto3`?

Because in DevOps automation:

| `os` Module                 | `boto3`                 |
| --------------------------- | ----------------------- |
| Reads environment variables | Connects to AWS         |
| Handles files               | Creates cloud resources |
| Runs shell commands         | Controls AWS services   |
| Gets runtime inputs         | Automates infra         |

Together → Powerful automation scripts.

---

# 🔥 Real-World Scenario 1

## 🎯 Problem:

Stop all EC2 instances using environment-based configuration.

---

## ✅ Step 1: Store AWS Credentials as Environment Variables

In Linux:

```bash id="k0x1zz"
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="ap-south-1"
```

---

## ✅ Step 2: Python Script Using `os + boto3`

```python
import os
import boto3

# Read region from environment variable
region = os.environ.get("AWS_DEFAULT_REGION")

# Create EC2 client
ec2 = boto3.client("ec2", region_name=region)

# Describe running instances
response = ec2.describe_instances(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
)

instance_ids = []

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_ids.append(instance["InstanceId"])

# Stop instances
if instance_ids:
    ec2.stop_instances(InstanceIds=instance_ids)
    print("Stopped instances:", instance_ids)
else:
    print("No running instances found")
```

---

## ✅ Output Example

```text
Stopped instances: ['i-0123456789abcdef0']
```

---

# 🔥 Real DevOps Use Case

👉 Schedule this script using cron
👉 Auto stop non-production servers at night
👉 Save AWS cost

---

# 🔥 Real-World Scenario 2

## 🎯 Problem:

Upload Jenkins backup to S3 automatically.

---

## ✅ Script

```python
import os
import boto3

# Path from OS
backup_path = "/var/lib/jenkins"

# S3 bucket name from environment variable
bucket_name = os.environ.get("BACKUP_BUCKET")

s3 = boto3.client("s3")

for root, dirs, files in os.walk(backup_path):
    for file in files:
        full_path = os.path.join(root, file)
        s3.upload_file(full_path, bucket_name, file)

print("Backup uploaded successfully")
```

---

## 🔥 DevOps Use Case

* Backup Jenkins data
* Backup logs
* Store build artifacts

---

# 🔥 Real-World Scenario 3

## 🎯 Problem:

Trigger AWS Lambda after deployment

```python
import os
import boto3

lambda_name = os.environ.get("LAMBDA_FUNCTION")

lambda_client = boto3.client("lambda")

response = lambda_client.invoke(
    FunctionName=lambda_name,
    InvocationType="Event"
)

print("Lambda triggered")
```

---

# 🎯 Why Use `os.environ` Instead of Hardcoding?

❌ Bad Practice:

```python
aws_key = "ABC123"
```

✅ Good Practice:

```python
aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
```

Reason:

* Secure
* CI/CD friendly
* Works in Jenkins, Docker, GitHub Actions

---

# 🔥 Production-Level Pattern

In CI/CD (like Jenkins):

1️⃣ Jenkins stores credentials
2️⃣ Injects as environment variables
3️⃣ Python script reads using `os.environ`
4️⃣ boto3 performs AWS action

Clean and secure.

---

# 🎯 Interview Answer

**Q: How do you combine os and boto3 for AWS automation?**

👉 Use `os` to:

* Read environment variables
* Manage files
* Handle runtime inputs

👉 Use `boto3` to:

* Interact with AWS services
* Automate EC2, S3, IAM, Lambda

Used in:

* Auto-scaling scripts
* Backup automation
* Cost optimization
* CI/CD deployment automation

---

# 🔥 Advanced DevOps Enhancement

Instead of raw credentials, use:

* IAM Role attached to EC2
* Instance profile authentication
* `boto3` automatically detects credentials

More secure.

---
