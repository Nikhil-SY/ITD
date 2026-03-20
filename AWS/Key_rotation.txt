## 🔐 AWS Key Rotation – Detailed Step-by-Step

---

# 🔹 What is Key Rotation?

> Process of **replacing old access/encryption keys with new ones** without breaking applications.

---

# 🔹 Why Required?

* Reduce risk if keys are leaked
* Meet compliance (SOC2, PCI-DSS)
* Limit long-term misuse
* Improve overall security posture

---

# 🔹 Types Covered

1. **IAM Access Key Rotation (Manual)**
2. **KMS Key Rotation (Automatic)**

---

# 🔹 1. IAM Access Key Rotation (DETAILED)

## 🧠 Important Concepts

* Each IAM user can have **max 2 access keys**
* Rotation = **Create → Switch → Disable → Delete**

---

## 🔄 Step-by-Step Process

---

## ✅ Step 1: Identify Existing Keys

### 📍 Go to:

* AWS Console → IAM → Users → *Select User* → **Security Credentials**

### 🔍 Check:

* Active keys
* Last used date

👉 If key is old → rotate it

---

## ✅ Step 2: Create New Access Key

### Action:

* Click **Create Access Key**

### Output:

* Access Key ID
* Secret Access Key

⚠️ Important:

* Download or copy immediately (won’t be shown again)

---

## ✅ Step 3: Update Application with New Key

### Where keys are used:

* Environment variables
* Config files
* CI/CD tools (Jenkins, GitHub Actions)

---

### 💡 Example (Linux EC2):

```bash
export AWS_ACCESS_KEY_ID=NEW_KEY
export AWS_SECRET_ACCESS_KEY=NEW_SECRET
```

---

### 💡 Example (Jenkins):

* Go to Credentials → Update with new keys

---

## ✅ Step 4: Test Application

### Verify:

* API calls working
* S3 access working
* No authentication errors

---

### 🚫 If Not Tested:

👉 Risk of production failure after deleting old key

---

## ✅ Step 5: Disable Old Key

### Action:

* Change status → **Inactive**

### Why?

* Safe fallback if something breaks

---

## ✅ Step 6: Monitor for Issues

* Check logs:

  * **AWS CloudTrail**
  * Application logs

👉 If no issues → proceed

---

## ✅ Step 7: Delete Old Key

### Action:

* Permanently remove old key

👉 Now rotation is complete ✅

---

## 🔄 Final Flow

```id="jiv99c"
Old Key → New Key Created → App Updated → Test → Disable Old → Delete Old
```

---

# 🔹 2. KMS Key Rotation (DETAILED)

## 🧠 Concept

* AWS rotates **encryption key material internally**
* No need to update application

---

## ✅ Step-by-Step

---

## Step 1: Go to KMS

* AWS Console → KMS → Customer Managed Keys

---

## Step 2: Select Key

* Choose your encryption key

---

## Step 3: Enable Rotation

* Click **Key Rotation**
* Enable **Automatic Rotation**

---

## 🧠 What Happens Internally?

* AWS creates new key material every year
* Old keys still used to decrypt old data
* Same Key ID is maintained

---

## ✅ No Downtime

* Apps continue working without any change

---

# 🔹 Real-Time DevOps Use Case (VERY IMPORTANT)

## 🚀 Scenario:

* App running in EC2
* Using IAM access key to access S3

---

## ❌ Problem:

* Key leaked in GitHub

---

## ✅ Solution:

### Step 1: Create new key

### Step 2: Update in:

* EC2 environment variables
* Jenkins pipeline

### Step 3: Restart app

```bash
sudo systemctl restart myapp
```

### Step 4: Disable old key

### Step 5: Delete old key

---

## 🔐 Result:

* Hacker cannot use old key
* App works with new key

---

# 🔹 Best Practices (Interview Highlight)

### ✅ Use IAM Roles instead of Keys

* No manual rotation required

---

### ✅ Rotation Frequency

* Every **60–90 days**

---

### ✅ Monitoring

* Use:

  * AWS CloudTrail
  * AWS Config

---

### ❌ Avoid

* Hardcoding keys in code
* Sharing keys in email/chat

---

# 🔹 IAM Role vs Access Key

| Feature  | IAM Role    | Access Key         |
| -------- | ----------- | ------------------ |
| Rotation | Automatic   | Manual             |
| Security | High        | Medium             |
| Usage    | EC2, Lambda | CLI, external apps |

---

# 🎯 Simple Memory Trick

> **“Create → Update → Test → Disable → Delete”**

---

# 🔁 Interview Follow-up Questions

* How to automate key rotation?
* What is AWS Secrets Manager rotation?
* What happens if key is deleted before updating app?

---