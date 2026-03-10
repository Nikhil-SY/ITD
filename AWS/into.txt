# AWS Notes (Your Questions + Explanations)

---

# Question 1: What is an Availability Zone and a Local Zone in AWS?

## 1. Availability Zone (AZ)

### Definition

An **Availability Zone (AZ)** is a **physically separate data center or group of data centers within an AWS Region**, designed to be **isolated from failures in other Availability Zones while still being connected with high-speed networking**.

### Explanation

An **AWS Region** contains multiple **Availability Zones**. Each AZ has independent:

* Power
* Cooling
* Networking
* Physical infrastructure

If one AZ fails, workloads in another AZ **continue running**.

Example:

```text
Region (Mumbai)
   ├ AZ1
   ├ AZ2
   └ AZ3
```

Example architecture:

```text
Internet
   ↓
Load Balancer
   ↓
EC2 (AZ1)
EC2 (AZ2)
```

---

# 2. Local Zone

## Definition

A **Local Zone** is an **extension of an AWS Region placed closer to users** to provide **very low latency access to AWS services**.

### Explanation

Sometimes the AWS region is far from users. This increases latency.

AWS deploys **Local Zones near major cities** to reduce latency while still connecting to the **parent region**.

Example:

```text
Users (Bangalore)
        ↓
AWS Local Zone
        ↓
Mumbai Region
```

---

# Question 2: What is an Edge Location?

## Definition

An **Edge Location** is a **small AWS data center used to cache and deliver content closer to users**.

Main services using Edge Locations:

* CloudFront
* Route 53
* AWS Shield
* AWS WAF

Example:

```text
User
 ↓
Edge Location (Cache)
 ↓
Origin Server (AWS Region)
```

---

# Question 3: Reliability, High Availability, Fault Tolerance, Disaster Recovery

## Reliability

### Definition

**Reliability** is the **ability of a system to perform consistently without failures over time**.

Example:

```text
System runs continuously without crashes
```

---

## High Availability

### Definition

**High Availability (HA)** means **systems remain accessible with minimal downtime**.

Example:

```text
Load Balancer
   ↓
EC2 (AZ1)
EC2 (AZ2)
```

If AZ1 fails → AZ2 continues serving traffic.

---

## Fault Tolerance

### Definition

**Fault Tolerance** means **system continues operating even if a component fails**.

Example:

```text
Load Balancer
   ↓
Server1
Server2
Server3
```

If one server fails, the system continues working.

---

## Disaster Recovery

### Definition

**Disaster Recovery (DR)** is the **strategy used to recover systems after a major disaster such as region failure, cyber attack, or natural disaster**.

Example:

```text
Primary Region → Mumbai
Backup Region → Singapore
```

---

# Question 4: On-Prem, Public Cloud, Private Cloud, Hybrid Cloud, Multi-Cloud

## On-Premises

### Definition

Infrastructure **hosted in the company’s own data center and managed by the organization**.

Example:

```text
Company Data Center
   ├ Application Server
   ├ Database Server
   ├ Storage
   └ Networking
```

---

## Public Cloud

### Definition

Infrastructure **owned and managed by cloud providers and accessed via internet**.

Examples:

* AWS
* Azure
* Google Cloud

Example:

```text
User
 ↓
Internet
 ↓
AWS Cloud
```

---

## Private Cloud

### Definition

Cloud infrastructure **dedicated to one organization**.

Example technologies:

* VMware
* OpenStack

---

## Hybrid Cloud

### Definition

Combination of **On-Premises infrastructure and Public Cloud**.

Example:

```text
On-Prem Data Center
       ↓
   VPN / Direct Connect
       ↓
      AWS Cloud
```

---

## Multi-Cloud

### Definition

Using **multiple cloud providers simultaneously**.

Example:

```text
AWS → Application
Azure → Database
Google Cloud → Analytics
```

---

# Question 5: AWS EC2 Instance Types (Family Codes and Use Cases)

## What is an EC2 Instance Type?

### Definition

An **EC2 Instance Type defines the compute capacity of a virtual machine**, including:

* CPU
* Memory
* Storage
* Network

---

## General Purpose

Family Codes:

```
T (t2, t3, t4g)
M (m5, m6)
```

Use cases:

* Web servers
* Development environments
* Small databases

---

## Compute Optimized

Family Code:

```
C (c5, c6)
```

Use cases:

* High CPU applications
* Gaming servers
* Scientific computing

---

## Memory Optimized

Family Codes:

```
R
X
Z
```

Use cases:

* In-memory databases
* Big data analytics

---

## Storage Optimized

Family Codes:

```
I
D
H
```

Use cases:

* Data warehousing
* NoSQL databases
* Log processing

---

## Accelerated Computing

Family Codes:

```
P
G
F
Inf
```

Use cases:

* AI / ML
* Deep learning
* Video rendering

---

# Question 6: On-Demand Instances vs Reserved Instances

## On-Demand Instances

### Definition

**On-Demand instances allow you to pay for compute capacity by the hour or second without long-term commitment.**

Example:

```text
Launch EC2 → Run for few hours → Stop → Pay only for usage
```

Use cases:

* Development
* Testing
* Temporary workloads

---

## Reserved Instances

### Definition

**Reserved Instances provide large discounts when you commit to using EC2 for 1 or 3 years.**

Benefits:

* Up to ~75% cheaper than On-Demand.

Use cases:

* Production servers
* Long-running workloads

---

# Question 7: Spot Instances and Savings Plans

## Spot Instances

### Definition

**Spot Instances allow you to use unused AWS compute capacity at very low prices (up to 90% cheaper).**

Important point:

AWS can terminate them **with 2-minute notice**.

Use cases:

* Batch processing
* CI/CD jobs
* ML training

---

## Savings Plans

### Definition

**Savings Plans give discounted pricing when you commit to using a specific amount of compute per hour for 1 or 3 years.**

Types:

1. Compute Savings Plan
2. EC2 Instance Savings Plan

---

# Question 8: What is AMI (Amazon Machine Image)?

## Definition

An **AMI (Amazon Machine Image)** is a **preconfigured template used to launch EC2 instances**.

It contains:

* Operating system
* Application software
* Configuration
* Required packages

Simple meaning:

```text
AMI = Template used to create EC2 instances
```

---

## Example

```text
AMI
 ├ OS (Linux/Windows)
 ├ Installed Software
 ├ Application Code
 └ Configuration

        ↓

Launch EC2 Instance
```

---

## DevOps Example

If you configure:

* Ubuntu
* Java
* Nginx
* Application

You can create an **AMI**.

Then every new EC2 instance launched from that AMI will already contain everything.

---

# Question 9: Difference Between AMI, Snapshot, and EBS Volume

This is a **very common DevOps interview question**.

---

# 1. EBS Volume

## Definition

An **EBS (Elastic Block Store) Volume** is a **persistent block storage device attached to an EC2 instance**.

It works like a **hard disk for the EC2 server**.

Example:

```text
EC2 Instance
     ↓
EBS Volume (Disk Storage)
```

Characteristics:

* Persistent storage
* Data remains even if instance stops
* Can attach/detach to EC2

Use cases:

* OS disk
* Database storage
* Application storage

---

# 2. Snapshot

## Definition

A **Snapshot is a backup of an EBS volume stored in Amazon S3**.

Example:

```text
EBS Volume
     ↓
Snapshot (Backup)
     ↓
Stored in S3
```

Purpose:

* Backup
* Disaster recovery
* Creating new volumes

Example workflow:

```text
EBS Volume
   ↓
Create Snapshot
   ↓
Restore to new EBS Volume
```

---

# 3. AMI

## Definition

An **AMI is a template used to launch EC2 instances**, created from **snapshots of EBS volumes plus configuration information**.

Example:

```text
EC2 Instance
   ↓
EBS Volume
   ↓
Snapshot
   ↓
AMI
```

AMI contains:

* OS
* Applications
* Configuration
* Snapshot of disk

---

# Relationship Between Them

```text
EC2 Instance
     ↓
EBS Volume (Disk)
     ↓
Snapshot (Backup)
     ↓
AMI (Template to create new EC2)
```

---

# Key Differences

| Feature  | EBS Volume      | Snapshot          | AMI                  |
| -------- | --------------- | ----------------- | -------------------- |
| Type     | Storage         | Backup            | Template             |
| Purpose  | Store data      | Backup disk       | Launch EC2 instances |
| Location | Attached to EC2 | Stored in S3      | Stored in AWS        |
| Use Case | Disk for server | Disaster recovery | Create servers       |

---

# Easy Way to Remember

```text
EBS → Disk

Snapshot → Backup of disk

AMI → Template to create EC2
```

---

