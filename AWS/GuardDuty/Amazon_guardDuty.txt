Here’s your **interview-style explanation (What, Why, How)** for GuardDuty 👇

---

# 🛡️ Amazon GuardDuty

---

# ✅ 1. WHAT is GuardDuty?

👉 **Definition**
A **threat detection service** that:

* Continuously monitors AWS accounts for **malicious or suspicious activity**
* Uses **Machine Learning (ML), anomaly detection, and threat intelligence**

---

## 🔹 Core Concept (1-line)

👉 “GuardDuty = **Intelligent threat detection for AWS environment**”

---

# ✅ 2. WHY do we use GuardDuty?

## 🔸 1. Detect Security Threats

* Identify attacks like:

  * Unauthorized access
  * Crypto mining
  * Port scanning

---

## 🔸 2. Continuous Monitoring

* Works 24/7 without manual setup

---

## 🔸 3. No Infrastructure Required

* Fully managed (no agents needed)

---

## 🔸 4. Improve Security Posture

* Early detection → faster response

---

# ✅ 3. WHAT Data Sources It Uses

GuardDuty analyzes:

| Data Source     | Purpose                   |
| --------------- | ------------------------- |
| VPC Flow Logs   | Network traffic analysis  |
| CloudTrail Logs | API activity monitoring   |
| DNS Logs        | Detect suspicious domains |

---

# ✅ 4. HOW GuardDuty Works

## 🔹 Workflow

```id="bq4t1c"
Logs (VPC, CloudTrail, DNS)
        ↓
GuardDuty Analysis (ML + Threat Intel)
        ↓
Detect Suspicious Activity
        ↓
Generate Findings
        ↓
Send Alerts (Security Hub / EventBridge)
```

---

## 🔹 Key Components

### 🔸 1. Detectors

* Core GuardDuty resource per region

---

### 🔸 2. Findings

* Alerts generated when threat is detected

👉 Includes:

* Severity (Low, Medium, High)
* Resource affected
* Description of threat

---

### 🔸 3. Threat Intelligence

* Uses:

  * AWS internal data
  * External threat feeds

---

# ✅ 5. Example Scenarios

### 🔹 Scenario 1: Suspicious Login

* Login from unusual country
  👉 GuardDuty → flags as anomaly

---

### 🔹 Scenario 2: Crypto Mining Attack

* EC2 instance starts mining crypto
  👉 GuardDuty → detects unusual CPU/network behavior

---

### 🔹 Scenario 3: Port Scanning

* Multiple ports scanned
  👉 GuardDuty → identifies reconnaissance activity

---

# ✅ 6. Key Features

* ✅ Fully managed (no setup needed)
* ✅ Continuous monitoring
* ✅ Machine learning-based detection
* ✅ Integration with other services
* ✅ Real-time alerts

---

# ✅ 7. Integration

* Sends findings to:

  * AWS Security Hub
  * EventBridge
  * Lambda
  * SNS

---

# ✅ 8. GuardDuty vs Others

| Service      | Role                   |
| ------------ | ---------------------- |
| GuardDuty    | Threat detection       |
| AWS Config   | Configuration tracking |
| CloudTrail   | API logging            |
| Security Hub | Central dashboard      |

---

# ✅ 9. Pricing

* Based on:

  * Volume of logs analyzed (VPC, DNS, CloudTrail)

---

# ✅ 10. Limitations

* ❌ Doesn’t block attacks (only detects)
* ❌ No automatic remediation (needs Lambda/SOAR)

---

# 🔥 Final Summary

* Detects **threats using logs + ML**
* Generates **security findings**
* Integrates with **Security Hub**
* Helps in **early threat detection**

---