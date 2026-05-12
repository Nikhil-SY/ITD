# AWS Networking Notes (Today)

---

# Question 1: What are Stateful and Stateless in AWS?

## Definition

### Stateful

A **stateful service remembers the state of a connection**.
If a request is allowed, the **response is automatically allowed** without requiring another rule.

```
Request allowed → Response automatically allowed
```

---

### Stateless

A **stateless service does NOT remember the state of a connection**.
Both **incoming and outgoing traffic must be explicitly allowed by rules**.

```
Request allowed ≠ Response allowed
Separate rules needed for both directions
```

---

## AWS Examples

### Stateful

**Security Groups**

Used with:

* EC2
* RDS
* Load Balancers
* EFS
* Lambda in VPC
* EKS worker nodes

Example:

```
Inbound: Allow HTTP (80)
```

Response traffic is **automatically allowed**.

---

### Stateless

**Network ACL**

Applied at **subnet level**.

Example:

```
Inbound: Allow HTTP (80)
Outbound: Allow Ephemeral Ports (1024–65535)
```

Both directions must be allowed.

---

## Architecture

```
Internet
   ↓
Network ACL (Stateless)
   ↓
Subnet
   ↓
Security Group (Stateful)
   ↓
EC2
```

---

# Question 2: OSI Model

## Definition

The **OSI (Open Systems Interconnection) Model** explains **how network communication happens between systems** using **7 layers**.

---

## 7 Layers

| Layer | Name         | Function                |
| ----- | ------------ | ----------------------- |
| 7     | Application  | User applications       |
| 6     | Presentation | Encryption & formatting |
| 5     | Session      | Session management      |
| 4     | Transport    | Data delivery           |
| 3     | Network      | IP routing              |
| 2     | Data Link    | MAC addressing          |
| 1     | Physical     | Cables & signals        |

---

## Easy Memory Trick

```
All People Seem To Need Data Processing
```

---

# Question 3: Ports

## Definition

A **port is a logical endpoint used by applications for communication**.

```
IP Address → Device
Port → Application
```

Example:

```
192.168.1.10:80
```

---

## Most Used Ports

| Port | Protocol       | Use               |
| ---- | -------------- | ----------------- |
| 22   | SSH            | Remote login      |
| 21   | FTP            | File transfer     |
| 25   | SMTP           | Send mail         |
| 53   | DNS            | Domain resolution |
| 80   | HTTP           | Web traffic       |
| 443  | HTTPS          | Secure web        |
| 3306 | MySQL          | Database          |
| 5432 | PostgreSQL     | Database          |
| 6379 | Redis          | Cache             |
| 3389 | RDP            | Windows remote    |
| 8080 | HTTP alternate | Jenkins           |

---

# Question 4: ENI (Elastic Network Interface)

## Definition

An **Elastic Network Interface (ENI)** is a **virtual network card attached to an EC2 instance inside a VPC**.

```
ENI = Virtual Network Card for EC2
```

---

## Components of ENI

An ENI contains:

```
Private IP
Public IP
Elastic IP
MAC Address
Security Groups
Network Interface ID
```

---

## Types of ENI

### Primary ENI

* Automatically created when instance launches
* Cannot be detached

```
EC2
 └ Primary ENI
```

---

### Secondary ENI

Additional interfaces that can be attached manually.

```
EC2
 ├ Primary ENI
 └ Secondary ENI
```

---

## DevOps Example

```
EC2
 ├ ENI 1 → Application network
 └ ENI 2 → Management network
```

---

# Question 5: VPC and Subnets

---

# What is VPC?

## Definition

A **Virtual Private Cloud (VPC)** is a **logically isolated virtual network in AWS where you launch your resources**.

```
AWS Cloud
   ↓
VPC (Your private network)
```

---

## Example

```
VPC CIDR: 10.0.0.0/16
```

---

# What is a Subnet?

A **Subnet is a smaller network inside a VPC** used to divide the VPC network.

Example:

```
VPC
 ├ Subnet 1
 ├ Subnet 2
 └ Subnet 3
```

---

## Types of Subnets

### Public Subnet

A subnet that **has access to the internet**.

```
Internet
   ↓
Internet Gateway
   ↓
Public Subnet
   ↓
EC2
```

Used for:

* Load balancers
* Web servers
* Bastion hosts

---

### Private Subnet

A subnet that **does not have direct internet access**.

```
Internet
   ↓
Public Subnet
   ↓
NAT Gateway
   ↓
Private Subnet
   ↓
EC2 / Database
```

Used for:

* Application servers
* Databases
* Internal services

---

# Question 6: Tenancy in AWS

---

# Definition

**Tenancy defines how EC2 instances are placed on the underlying physical hardware in AWS.**

It determines **whether your instance runs on shared hardware or dedicated hardware**.

```
Tenancy = Hardware allocation for EC2
```

---

# Types of Tenancy

AWS provides **three tenancy options**.

| Tenancy Type       | Description                                                |
| ------------------ | ---------------------------------------------------------- |
| Shared (Default)   | Instances share physical hardware with other AWS customers |
| Dedicated Instance | Instances run on hardware dedicated to your account        |
| Dedicated Host     | Entire physical server is dedicated to your account        |

---

# 1. Shared Tenancy (Default)

This is the **most commonly used option**.

Characteristics:

* Multiple AWS customers share the same physical server
* AWS manages isolation between tenants
* Lowest cost

Example:

```
Physical Server
 ├ Customer A EC2
 ├ Customer B EC2
 └ Customer C EC2
```

Used for:

* Most applications
* DevOps environments
* Web applications

---

# 2. Dedicated Instance

In this model:

* The **physical server is dedicated to your AWS account**
* Other AWS customers cannot use that server

Example:

```
Physical Server
 ├ EC2 Instance (Your Account)
 ├ EC2 Instance (Your Account)
 └ EC2 Instance (Your Account)
```

Used when:

* Regulatory compliance is required
* Security requirements are strict

---

# 3. Dedicated Host

A **Dedicated Host gives you an entire physical server**.

You can control:

* Instance placement
* Number of instances
* Licensing

Example:

```
Dedicated Host

 ├ EC2 Instance
 ├ EC2 Instance
 └ EC2 Instance
```

Used for:

* License-bound software
* Oracle
* Microsoft SQL Server
* Windows Server BYOL (Bring Your Own License)

---

# Comparison

| Feature                 | Shared | Dedicated Instance | Dedicated Host |
| ----------------------- | ------ | ------------------ | -------------- |
| Hardware Shared         | Yes    | No                 | No             |
| Physical Server Control | No     | No                 | Yes            |
| Cost                    | Lowest | Medium             | Highest        |
| Licensing Control       | No     | Limited            | Full           |

---

# Real DevOps Example

Most DevOps workloads use:

```
Shared Tenancy
```

Example:

```
Auto Scaling Group
   ↓
Multiple EC2 Instances
   ↓
Shared AWS Hardware
```

This reduces cost and allows **elastic scaling**.

---

# Important Interview Points

* **Tenancy determines hardware allocation for EC2 instances**
* Default option is **Shared Tenancy**
* **Dedicated Instance** gives hardware isolation
* **Dedicated Host** provides full control over the physical server
* Used mainly for **compliance and licensing requirements**.

# Question 7: What is CIDR?

## Definition

**CIDR (Classless Inter-Domain Routing)** is a method for allocating IP addresses and routing IP packets. It allows you to specify IP address ranges more flexibly than the old class-based system.

A **CIDR block** is written as:
// Represents an IP address in CIDR notation.
// Format: <IP_address>/<prefix_length>
// Example: 192.168.1.0/24
// This line represents a CIDR (Classless Inter-Domain Routing) notation for an IP network.
// Format: <IP_address>/<prefix_length>
// - <IP_address>: The starting IP address of the network.
// - <prefix_length>: The number of bits in the network portion of the address (e.g., 24 for a /24 network).
//
// The number of usable IP addresses in the network can be calculated as follows:
//   Number of IPs = 2^(32 - prefix_length)
// For example, a /24 network (prefix_length = 24) contains 2^(32-24) = 256 IP addresses.
//
// Note: In IPv4, typically the first address is reserved as the network address and the last as the broadcast address,
// so the number of usable host IPs is usually (2^(32 - prefix_length)) - 2.
<IP_address>/<prefix_length>