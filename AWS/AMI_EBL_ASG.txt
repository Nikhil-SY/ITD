# AWS Notes (Questions 10–14)

---

# Question 10: What is AMI (Amazon Machine Image)?

## Definition

An **Amazon Machine Image (AMI)** is a **preconfigured template used to launch EC2 instances**.

It contains everything required to create a virtual server such as:

* Operating System
* Application software
* Configuration files
* Required libraries
* Storage configuration

Simple meaning:

```
AMI = Template used to create EC2 instances
```

---

## Example

```
AMI
 ├ Operating System
 ├ Installed Software
 ├ Application Code
 └ Configuration

        ↓

Launch EC2 Instance
```

---

## Real DevOps Example

Suppose you configure an EC2 server with:

* Ubuntu OS
* Java installed
* Nginx installed
* Application deployed

Instead of repeating this setup every time:

```
Configured EC2
      ↓
Create AMI
      ↓
Launch multiple identical EC2 servers
```

This is useful for:

* Auto Scaling
* Fast infrastructure creation
* Consistent environments

---

## Types of AMI

### 1. AWS Managed AMI

Provided by AWS.

Examples:

* Amazon Linux
* Ubuntu
* Windows Server

---

### 2. AWS Marketplace AMI

Provided by third-party vendors.

Examples:

* Jenkins
* MongoDB
* WordPress

---

### 3. Custom AMI

Created by users from their own EC2 instances.

Use cases:

* Preconfigured application servers
* Production environments
* Auto Scaling templates

---

# Question 11: Difference Between AMI, Snapshot, and EBS Volume

---

# 1. EBS Volume

## Definition

**Elastic Block Store (EBS)** is a **persistent block storage device attached to an EC2 instance**.

It works like a **hard disk for the server**.

Example:

```
EC2 Instance
     ↓
EBS Volume (Disk Storage)
```

Use cases:

* Operating system disk
* Database storage
* Application storage

---

# 2. Snapshot

## Definition

A **Snapshot** is a **backup of an EBS volume stored in Amazon S3**.

Example:

```
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

---

# 3. AMI

An **AMI is created using snapshots of EBS volumes plus configuration information**.

Example:

```
EC2 Instance
     ↓
EBS Volume
     ↓
Snapshot
     ↓
AMI
```

---

# Relationship

```
EC2 Instance
     ↓
EBS Volume
     ↓
Snapshot
     ↓
AMI
```

---

# Key Differences

| Feature  | EBS Volume      | Snapshot          | AMI            |
| -------- | --------------- | ----------------- | -------------- |
| Type     | Storage         | Backup            | Template       |
| Purpose  | Store data      | Backup disk       | Launch EC2     |
| Location | Attached to EC2 | Stored in S3      | AWS service    |
| Use Case | Server disk     | Disaster recovery | Launch servers |

---

# Question 12: Launch Template vs Launch Configuration

These are **templates used by Auto Scaling Groups to launch EC2 instances**.

---

# Launch Configuration

## Definition

A **Launch Configuration** is a template used by **Auto Scaling Groups to launch EC2 instances**.

It includes:

* AMI
* Instance type
* Security group
* Key pair
* Storage
* User data scripts

Example:

```
Launch Configuration
   ├ AMI
   ├ Instance Type
   ├ Security Group
   ├ Key Pair
   └ Storage
```

---

## Important Characteristics

* Cannot be modified
* No versioning
* Must create a new configuration for changes
* Considered a legacy feature

---

# Launch Template

## Definition

A **Launch Template** is the **modern and advanced version of Launch Configuration**.

It supports:

* Versioning
* More AWS features
* Better flexibility

Example:

```
Launch Template
   ├ AMI
   ├ Instance Type
   ├ IAM Role
   ├ Security Group
   ├ Storage
   └ Networking
```

---

# Versioning vs Modification

### Launch Configuration

* Immutable (cannot modify)
* Need to create a new configuration for every change

Example:

```
LC-v1 → t3.micro
LC-v2 → t3.small
LC-v3 → t3.medium
```

---

### Launch Template

Supports **versioning**.

Example:

```
Launch Template

Version 1 → t3.micro
Version 2 → t3.small
Version 3 → t3.medium
```

Benefits:

* Easy rollback
* Organized management
* Change tracking

---

# Key Difference

| Feature            | Launch Configuration | Launch Template    |
| ------------------ | -------------------- | ------------------ |
| Versioning         | Not supported        | Supported          |
| Modification       | Not allowed          | Create new version |
| Features           | Limited              | Advanced           |
| AWS Recommendation | Legacy               | Recommended        |

---

# Question 13: Auto Scaling Group (ASG)

## Definition

An **Auto Scaling Group automatically increases or decreases EC2 instances based on demand**.

Goals:

* Maintain availability
* Handle traffic spikes
* Reduce manual management

```
ASG = Automatic scaling of EC2 instances
```

---

# How ASG Decides When to Scale

Auto Scaling uses:

* CloudWatch metrics
* Scaling policies

Example policy:

```
CPU > 70% → Add instances
CPU < 30% → Remove instances
```

Workflow:

```
CloudWatch Metric
      ↓
Threshold crossed
      ↓
Scaling Policy
      ↓
Auto Scaling Group
      ↓
Launch or terminate EC2
```

---

# ASG Capacity Settings

### Minimum Capacity

Minimum instances always running.

Example:

```
Minimum = 2
```

---

### Desired Capacity

Number of instances ASG tries to maintain.

Example:

```
Desired = 3
```

---

### Maximum Capacity

Maximum instances allowed.

Example:

```
Maximum = 10
```

---

# Types of Scaling

### Target Tracking

Maintain a specific metric.

Example:

```
Target CPU = 50%
```

---

### Step Scaling

Scale based on thresholds.

Example:

```
CPU > 60% → Add 1 instance
CPU > 80% → Add 2 instances
```

---

### Scheduled Scaling

Scale based on time.

Example:

```
9 AM → Increase instances
11 PM → Reduce instances
```

---

# How Requests Are Served Using ELB + ASG

Architecture:

```
User
 ↓
Internet
 ↓
Load Balancer
 ↓
Auto Scaling Group
 ↓
EC2 Instances
```

---

## Request Flow

1. User sends request
2. DNS resolves to Load Balancer
3. Load Balancer distributes traffic
4. Requests reach EC2 instances

Example:

```
ELB
 ├ Request 1 → EC2-1
 ├ Request 2 → EC2-2
 └ Request 3 → EC2-3
```

---

# When Traffic Increases

```
CPU > threshold
     ↓
CloudWatch Alarm
     ↓
ASG launches new instances
```

Example:

```
Before: 3 instances
After: 5 instances
```

Load balancer automatically starts sending traffic to new servers.

---

# Question 14: Types of Load Balancers in AWS

AWS provides three main load balancers:

1. Application Load Balancer (ALB)
2. Network Load Balancer (NLB)
3. Classic Load Balancer (CLB)

---

# Application Load Balancer (ALB)

Works at **Layer 7 (Application Layer)**.

Routes traffic based on:

* URL path
* Host name
* HTTP headers

Example:

```
ALB
 ├ /user → User Service
 ├ /order → Order Service
 └ /payment → Payment Service
```

Use cases:

* Microservices
* APIs
* Container-based apps

---

# Network Load Balancer (NLB)

Works at **Layer 4 (Transport Layer)**.

Routes traffic using:

* IP address
* Port number
* TCP / UDP

Example:

```
Users
 ↓
NLB
 ↓
EC2 Instances
```

Use cases:

* High-performance applications
* Real-time systems
* Gaming platforms

---

# Classic Load Balancer (CLB)

Older load balancer.

Supports:

* Layer 4
* Layer 7

But has limited features.

Mostly used in **legacy systems**.

---

# OSI Layer Comparison

| Load Balancer             | OSI Layer   |
| ------------------------- | ----------- |
| Application Load Balancer | Layer 7     |
| Network Load Balancer     | Layer 4     |
| Classic Load Balancer     | Layer 4 & 7 |

---

# Easy Way to Remember

```
ALB → Smart routing (Layer 7)

NLB → High performance (Layer 4)

CLB → Old load balancer
```

---