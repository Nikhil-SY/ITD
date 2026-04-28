Here’s your **complete, interview-style deep dive on AWS Config (What, Why, How)** 👇

---

# ⚙️ AWS Config

---

# ✅ 1. WHAT is AWS Config?

👉 **Definition**
AWS Config is a service that:

* Continuously **monitors, records, and evaluates AWS resource configurations**
* Maintains a **history (timeline) of changes**
* Helps ensure **compliance with rules**

---

## 🔹 Core Concept (1-line)

👉 “AWS Config = **Configuration tracking + compliance enforcement**”

---

## 🔹 What it Records

* Resource configurations (EC2, S3, IAM, VPC, etc.)
* Configuration changes over time
* Relationships between resources

👉 Example:

```
EC2 → attached to Security Group → inside VPC
```

---

# ✅ 2. WHY do we use AWS Config?

## 🔸 1. Change Tracking

* Know **what changed in infrastructure**
* Track **before & after state**

---

## 🔸 2. Compliance Monitoring

* Check if resources follow rules

👉 Example rules:

* S3 bucket should NOT be public
* Security group should NOT allow 0.0.0.0/0 on port 22

---

## 🔸 3. Auditing & Troubleshooting

* Identify misconfigurations
* Investigate security issues

---

## 🔸 4. Drift Detection

* Detect changes from expected configuration (very useful with Terraform/CloudFormation)

---

## 🔸 5. Historical Visibility

* View configuration at any point in time

---

# ✅ 3. HOW AWS Config Works (Architecture)

## 🔹 Step-by-Step Flow

```id="9mj0p9"
1. Resource Change Happens
        ↓
2. AWS Config Records Configuration
        ↓
3. Stores in S3 (Configuration History)
        ↓
4. Sends Notifications via SNS
        ↓
5. Evaluates Against Rules
        ↓
6. Marks as COMPLIANT / NON-COMPLIANT
```

---

## 🔹 Components

### 🔸 1. Configuration Recorder

* Records resource changes
* Can be:

  * All resources
  * Specific resource types

---

### 🔸 2. Delivery Channel

* Sends data to:

  * S3 bucket (history storage)
  * SNS topic (notifications)

---

### 🔸 3. Configuration Items (CI)

* Snapshot of resource at a point in time

👉 Contains:

* Resource ID
* Configuration details
* Relationships
* Timestamp

---

### 🔸 4. Config Rules

* Define compliance conditions

👉 Types:

* AWS Managed Rules (predefined)
* Custom Rules (Lambda-based)

---

### 🔸 5. Conformance Packs

* Collection of rules for standards (like CIS)

---

# ✅ 4. Example (Real Scenario)

👉 Security group modified:

### Step 1: Change happens

* Port 22 opened to 0.0.0.0/0

### Step 2: AWS Config records

* Old config vs new config

### Step 3: Rule evaluation

* Rule: “No open SSH access”

### Step 4: Result

* ❌ NON-COMPLIANT

---

# ✅ 5. Key Features

* ✅ Continuous monitoring
* ✅ Configuration history (timeline view)
* ✅ Resource relationship mapping
* ✅ Compliance evaluation
* ✅ Integration with Lambda & EventBridge

---

# ✅ 6. Supported Resources (Examples)

* EC2 instances
* S3 buckets
* IAM roles
* VPC, Subnets
* RDS databases

---

# ✅ 7. AWS Config vs CloudTrail (Quick Revision)

| Feature | AWS Config    | CloudTrail   |
| ------- | ------------- | ------------ |
| Tracks  | Configuration | API activity |
| Focus   | What changed  | Who did it   |
| History | Full timeline | Event logs   |

---

# ✅ 8. Setup (Step-by-Step – Console)

## 🔹 Step 1: Enable AWS Config

* Go to AWS Config → Get Started

## 🔹 Step 2: Configure Recorder

* Choose:

  * All resources OR specific

---

## 🔹 Step 3: Setup Delivery Channel

* Select/create:

  * S3 bucket
  * SNS topic

---

## 🔹 Step 4: Add Rules

* Choose managed rules:

  * `s3-bucket-public-read-prohibited`
  * `restricted-ssh`

---

## 🔹 Step 5: Review & Start

* AWS Config starts recording

---

# ✅ 9. Pricing (Important for Interview)

* Charged based on:

  * Configuration items recorded
  * Rule evaluations

---

# ✅ 10. Limitations

* ❌ Not real-time like CloudTrail
* ❌ Costs increase with many resources
* ❌ Doesn’t show “who” made change

---

# 🔥 Final Summary

* Tracks **resource configuration changes**
* Maintains **history + relationships**
* Evaluates **compliance using rules**
* Helps in **security, auditing, and troubleshooting**

---