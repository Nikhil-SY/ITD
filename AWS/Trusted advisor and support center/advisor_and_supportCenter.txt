Got it 👍 — here’s the **same interview-style breakdown (What, Why, How)** for both services.

---

# 🛡️ AWS Trusted Advisor

---

# ✅ 1. WHAT is Trusted Advisor?

👉 **Definition**
A service that:

* Provides **real-time recommendations** to optimize:

  * Cost
  * Security
  * Performance
  * Fault tolerance
  * Service limits

---

## 🔹 Core Concept (1-line)

👉 “Trusted Advisor = **AWS expert recommendations for best practices**”

---

# ✅ 2. WHY do we use it?

## 🔸 1. Cost Optimization

* Identify unused resources
  👉 Example: Idle EC2, unattached EBS volumes

---

## 🔸 2. Security Improvements

* Detect risky configurations
  👉 Example: Open security groups (0.0.0.0/0)

---

## 🔸 3. Performance Boost

* Suggest better resource usage

---

## 🔸 4. Fault Tolerance

* Ensure high availability
  👉 Example: Check for multi-AZ usage

---

## 🔸 5. Service Limits Monitoring

* Avoid hitting AWS limits

---

# ✅ 3. HOW it Works

## 🔹 Workflow

```id="yb5ckb"
AWS Resources
     ↓
Trusted Advisor Checks
     ↓
Best Practice Analysis
     ↓
Recommendations + Alerts
```

---

## 🔹 Categories of Checks

| Category          | Example            |
| ----------------- | ------------------ |
| Cost Optimization | Idle load balancer |
| Security          | Public S3 bucket   |
| Fault Tolerance   | No backup enabled  |
| Performance       | Underutilized EC2  |
| Service Limits    | Approaching limit  |

---

## 🔹 Types of Checks

* Basic checks → Free tier
* Full checks → Business/Enterprise support plan

---

# ✅ 4. Example Scenario

👉 You forgot to delete an unused EBS volume

* Trusted Advisor detects:

  * ❌ Unused resource
  * 💰 Suggests cost saving

---

# ✅ 5. Key Features

* ✅ Best practice recommendations
* ✅ Easy dashboard
* ✅ Cost-saving insights
* ✅ No setup required

---

# 🔥 Final Summary

* Acts like a **cloud consultant**
* Helps optimize **cost, security, performance**
* Gives **actionable recommendations**

---

---

# 🎧 AWS Support Center

---

# ✅ 1. WHAT is Support Center?

👉 **Definition**
A portal to:

* Create and manage **AWS support tickets (cases)**
* Get help from AWS engineers

---

## 🔹 Core Concept (1-line)

👉 “Support Center = **Place to contact AWS support team**”

---

# ✅ 2. WHY do we use it?

## 🔸 1. Technical Issues

* EC2 not starting
* RDS connection issues

---

## 🔸 2. Billing Queries

* Unexpected charges
* Refund requests

---

## 🔸 3. Account Issues

* Login problems
* Service limits increase

---

## 🔸 4. Guidance & Architecture Help

* Best practices from AWS experts

---

# ✅ 3. HOW it Works

## 🔹 Workflow

```id="qz9n7s"
User raises support case
        ↓
AWS assigns support engineer
        ↓
Communication via ticket/email
        ↓
Issue resolved
```

---

## 🔹 Types of Support Cases

| Type          | Description            |
| ------------- | ---------------------- |
| Technical     | Service-related issues |
| Billing       | Cost & payment         |
| Account       | Login/access           |
| Service limit | Increase quota         |

---

## 🔹 Support Plans

| Plan       | Features               |
| ---------- | ---------------------- |
| Basic      | Only billing support   |
| Developer  | Business hours support |
| Business   | 24/7 support           |
| Enterprise | Dedicated TAM          |

---

# ✅ 4. Example Scenario

👉 Your production app is down

* Go to Support Center
* Create **high priority ticket**
* AWS engineer helps troubleshoot

---

# ✅ 5. Key Features

* ✅ Ticket-based support system
* ✅ Priority handling (based on plan)
* ✅ Direct AWS expert help
* ✅ Case tracking

---

# 🔥 Final Summary

* Used for **getting help from AWS**
* Handles **technical + billing + account issues**
* Critical for **production environments**

---

# ⚖️ Trusted Advisor vs Support Center (Quick Revision)

| Feature     | Trusted Advisor | Support Center   |
| ----------- | --------------- | ---------------- |
| Purpose     | Recommendations | Issue resolution |
| Type        | Automated       | Human support    |
| Use case    | Optimization    | Troubleshooting  |
| Interaction | Dashboard       | Tickets          |

---