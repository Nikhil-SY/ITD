Perfect 👍 — let’s go **deep, precise, and interview-ready** on SCP (Service Control Policies) in
AWS Organizations

---

# 🚀 SCP (Service Control Policies) – COMPLETE GUIDE

---

# 🧠 1. What is SCP?

**Service Control Policy (SCP)** is a policy used in AWS Organizations to **define the maximum permissions available to accounts**.

---

## 🔹 Key Definition (Interview)

👉
**“SCP does NOT grant permissions — it only restricts what actions are allowed.”**

---

## 🔹 Simple Understanding

```id="u1p9s2"
IAM → Grants permission  
SCP → Limits permission
```

---

## 🔹 Real Example

Even if IAM allows:

```json id="m3k9r1"
"ec2:*"
```

But SCP says:

```json id="x8v2p7"
"Deny ec2:TerminateInstances"
```

👉 Result:
❌ EC2 termination NOT allowed

---

# 🧱 2. Where SCP is Applied

---

## 🔹 Hierarchy

```id="p8s2n5"
Organization
   ↓
Root
   ↓
OU (Organizational Unit)
   ↓
Account
```

---

## 🔹 SCP can be attached to:

* Root
* OU
* Account

---

## 🔍 Important:

👉 SCP affects **ALL users and roles in that account**

---

# 🧠 3. How SCP Works (Evaluation Logic)

---

## 🔹 Final Permission Formula

```id="k3n9p2"
Final Access = IAM Allow ∩ SCP Allow
```

---

## 🔹 Cases:

| IAM   | SCP   | Result    |
| ----- | ----- | --------- |
| Allow | Allow | ✅ Allowed |
| Allow | Deny  | ❌ Denied  |
| Deny  | Allow | ❌ Denied  |

---

## 🔥 Golden Rule:

👉 **Explicit Deny always wins**

---

# 🧭 4. Types of SCP Policies

---

## 🔹 1. Allow List (Whitelist)

👉 Only specified actions are allowed

```json id="v9p3k1"
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

---

## 🔹 2. Deny List (Blacklist) ✅ (Most Used)

👉 Deny specific actions

```json id="c6r2m8"
{
  "Effect": "Deny",
  "Action": "ec2:TerminateInstances",
  "Resource": "*"
}
```

---

---

# 🔐 5. Important Default SCP

---

## 🔹 FullAWSAccess

👉 Default policy attached to all accounts

```id="x1p8q2"
Allows everything
```

---

### ⚠️ Important:

If you remove it → everything is blocked unless explicitly allowed

---

# ⚙️ 6. Creating SCP (Console Steps)

---

## 🔹 Step 1:

Go to AWS Organizations → Policies → Create Policy

---

## 🔹 Step 2:

Choose type → SCP

---

## 🔹 Step 3:

Write JSON policy

---

## 🔹 Step 4:

Attach to:

* Root / OU / Account

---

---

# 🔥 7. Common SCP Use Cases (VERY IMPORTANT)

---

## 🔹 1. Prevent Resource Deletion

```json id="p2n7k4"
{
  "Effect": "Deny",
  "Action": [
    "ec2:TerminateInstances",
    "rds:DeleteDBInstance"
  ],
  "Resource": "*"
}
```

---

## 🔹 2. Restrict Regions

```json id="t5q9w2"
{
  "Effect": "Deny",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": "ap-south-1"
    }
  },
  "Action": "*",
  "Resource": "*"
}
```

---

## 🔹 3. Block Root User Actions

---

## 🔹 4. Enforce Security Policies

* Disable public S3 access
* Enforce encryption

---

---

# ⚠️ 8. Common Mistakes

---

❌ Thinking SCP grants permissions
❌ Removing FullAWSAccess without alternative
❌ Blocking everything accidentally
❌ Not testing in dev OU first
❌ Applying SCP at root directly

---

---

# ⚔️ 9. SCP vs IAM

---

| Feature    | SCP               | IAM            |
| ---------- | ----------------- | -------------- |
| Scope      | Multiple accounts | Single account |
| Purpose    | Restrict          | Grant          |
| Applied at | Org/OU/Account    | User/Role      |

---

---

# 🔗 10. Real DevOps Scenario

---

## 🔹 Scenario:

Company wants strict control

---

### Structure:

```id="x9k2p6"
Root
 ├── Dev OU
 ├── Prod OU
```

---

### SCP on Prod OU:

```json id="g3r8t2"
Deny:
- Delete DB
- Terminate EC2
```

---

👉 Even admin cannot delete resources ❗

---

---

# 🧪 11. Debugging SCP Issues (VERY IMPORTANT)

---

## 🔹 Problem:

User cannot perform action

---

## 🔍 Check:

1. IAM policy
2. SCP policy
3. Root/OU level restrictions

---

## 🔹 Tool:

👉 AWS Policy Simulator

---

---

# 🧠 12. Interview Questions

---

## ❓ What is SCP?

👉 Policy to restrict permissions in AWS Organizations

---

## ❓ Does SCP grant permissions?

👉 ❌ No

---

## ❓ Where can SCP be applied?

👉 Root, OU, Account

---

## ❓ What happens if SCP denies something?

👉 Always denied

---

## ❓ What is FullAWSAccess?

👉 Default allow policy

---

## ❓ Difference between IAM and SCP?

👉 IAM grants, SCP restricts

---

---

# 🔥 FINAL SUMMARY

👉 SCP is used to:

* Enforce security across accounts
* Restrict dangerous actions
* Control permissions centrally

---