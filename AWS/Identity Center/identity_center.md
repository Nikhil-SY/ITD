Here’s your **interview-style explanation (What, Why, How)** for Identity Center 👇

---

# 🔐 AWS IAM Identity Center

*(formerly AWS Single Sign-On – SSO)*

---

# ✅ 1. WHAT is Identity Center?

👉 **Definition**
A service that:

* Provides **centralized access management** for:

  * Multiple AWS accounts
  * Cloud applications (SaaS)
* Enables **Single Sign-On (SSO)**

---

## 🔹 Core Concept (1-line)

👉 “Identity Center = **Centralized login + access control across AWS accounts and apps**”

---

# ✅ 2. WHY do we use Identity Center?

## 🔸 1. Single Sign-On (SSO)

* Login once → access multiple AWS accounts/apps

---

## 🔸 2. Centralized Access Management

* Manage users & permissions from one place

---

## 🔸 3. Multi-Account Management

* Very useful with:

  * AWS Organizations

---

## 🔸 4. Improved Security

* Supports:

  * Multi-Factor Authentication (MFA)
  * Integration with external identity providers

---

## 🔸 5. Reduced IAM Complexity

* No need to create IAM users in each account

---

# ✅ 3. WHAT It Manages

* Users and groups
* Permissions across accounts
* Access to AWS accounts & applications

---

# ✅ 4. HOW Identity Center Works

## 🔹 Workflow

```id="2k9mqs"
User logs into Identity Center (SSO Portal)
            ↓
Authentication (Internal / External IdP)
            ↓
User selects AWS Account / Application
            ↓
Temporary Credentials (via IAM Role)
            ↓
Access Granted
```

---

## 🔹 Key Components

### 🔸 1. Identity Source

* Where users are stored:

  * Identity Center directory (default)
  * External IdP (Okta, Azure AD, etc.)

---

### 🔸 2. Permission Sets

* Define permissions (like IAM policies)

👉 Example:

* Admin access
* Read-only access

---

### 🔸 3. AWS Accounts Assignment

* Assign:

  * User/Group → Account → Permission Set

---

### 🔸 4. SSO Portal

* Web portal where users log in and choose accounts/apps

---

# ✅ 5. Example Scenario

👉 Company has 3 AWS accounts:

* Dev
* Test
* Prod

Without Identity Center:

* Separate IAM users needed in each account ❌

With Identity Center:

* Single login
* Access all accounts based on role ✅

---

# ✅ 6. Key Features

* ✅ Single Sign-On (SSO)
* ✅ Centralized user management
* ✅ Temporary credentials (more secure)
* ✅ Multi-account access
* ✅ Integration with external IdPs

---

# ✅ 7. Identity Center vs IAM

| Feature   | Identity Center    | IAM            |
| --------- | ------------------ | -------------- |
| Scope     | Multi-account      | Single account |
| Login     | SSO                | Direct login   |
| User mgmt | Centralized        | Per account    |
| Use case  | Organization level | Resource level |

---

# ✅ 8. Integration

* Works with:

  * AWS Organizations
  * IAM Roles
  * External IdPs (Okta, Azure AD)

---

# ✅ 9. Pricing

* No additional cost (you pay for underlying services)

---

# ✅ 10. Limitations

* ❌ Requires AWS Organizations for full benefits
* ❌ Initial setup can be complex

---

# 🔥 Final Summary

* Centralized **identity and access management**
* Enables **SSO across AWS accounts**
* Uses **temporary credentials for security**
* Simplifies **multi-account access**

---