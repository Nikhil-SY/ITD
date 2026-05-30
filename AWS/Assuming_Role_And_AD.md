---

# 🎯 Goal

Set up:

👉 **Azure AD (IdP) → AWS (Service Provider) using SAML**
👉 Users click a link → automatically log into AWS → assume IAM Role

---

# 🧠 High-Level Architecture

```
User → Azure AD (Authentication)
     → SAML Assertion
     → AWS IAM Role (Authorization)
     → AWS Console Access
```

---

# 🔹 STEP 1: Create SAML Provider in AWS

## ✅ Why?

AWS needs to **trust Azure AD** → this is done via SAML provider.

---

## 🔧 Steps in AWS

1. Go to **IAM → Identity Providers**
2. Click **Add provider**
3. Choose:

   * Provider type: `SAML`
   * Name: `AzureAD`
4. Upload **Metadata XML file from Azure AD** (we’ll generate this later)

---

## 📌 What is Metadata XML?

It contains:

* Azure AD public certificate
* SSO URL
* Issuer details

👉 AWS uses this to **verify SAML responses**

---

# 🔹 STEP 2: Create IAM Role for SAML

## ✅ Why?

This is the role users will assume after login.

---

## 🔧 Steps

1. Go to **IAM → Roles → Create Role**
2. Select:

   * **SAML 2.0 federation**
   * Choose provider: `AzureAD`
3. Select:

   * `Allow programmatic and console access`

---

## 🔐 Trust Policy (IMPORTANT)

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::<ACCOUNT_ID>:saml-provider/AzureAD"
  },
  "Action": "sts:AssumeRoleWithSAML",
  "Condition": {
    "StringEquals": {
      "SAML:aud": "https://signin.aws.amazon.com/saml"
    }
  }
}
```

### 🔍 Explanation:

* Only Azure AD users can assume role
* Only valid AWS SAML audience allowed

---

# 🔹 STEP 3: Attach Permissions to Role

## ✅ Why?

This defines **what user can do after login**

---

### Example:

#### 🔓 Admin access

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

#### OR your custom policies (like your example)

---

# 🔹 STEP 4: Setup Azure AD Enterprise Application

## ✅ Why?

Azure needs to know:
👉 “AWS is a trusted application”

---

## 🔧 Steps in Azure Portal

1. Go to **Azure Portal**
2. Navigate to:

   * Azure Active Directory → Enterprise Applications
3. Click:

   * **New Application**
4. Search:

   * “AWS”
5. Select:

   * **AWS (SAML-based)**

---

# 🔹 STEP 5: Configure SAML in Azure AD

Go to:
👉 **Single Sign-On → SAML**

---

## 🔧 Fill these values:

### 1. Identifier (Entity ID)

```
urn:amazon:webservices
```

### 2. Reply URL (ACS URL)

```
https://signin.aws.amazon.com/saml
```

### 3. Sign-on URL (optional)

```
https://console.aws.amazon.com/
```

---

# 🔹 STEP 6: Download Metadata XML

In Azure:

* Go to SAML config page
* Download:
  👉 **Federation Metadata XML**

---

## 🔁 Now go back to AWS

Upload this XML in:
👉 IAM → Identity Provider

---

# 🔹 STEP 7: Configure Role Mapping (VERY IMPORTANT)

## ✅ Why?

Azure must tell AWS:
👉 “Which role this user should assume”

---

## 🔧 In Azure → Attributes & Claims

Add new claim:

### Name:

```
https://aws.amazon.com/SAML/Attributes/Role
```

### Value:

```
arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>,arn:aws:iam::<ACCOUNT_ID>:saml-provider/AzureAD
```

---

## 🧠 Format:

```
<Role ARN>,<SAML Provider ARN>
```

---

# 🔹 STEP 8: Assign Users / Groups in Azure

## 🔧 Steps:

1. Go to:

   * Enterprise App → Users and Groups
2. Assign:

   * Users or Groups

---

## 🧠 Why?

Only assigned users can access AWS

---

# 🔹 STEP 9: Test Login

## 🔧 Steps:

1. Go to:

   * Azure My Apps portal OR App URL
2. Click:

   * AWS app

---

## 🔄 Flow:

* Azure authenticates user
* Sends SAML response
* AWS validates
* Role assumed
* Console opens

---

# 🔥 END-TO-END FLOW (Interview Ready)

1. User clicks AWS app
2. Redirected to Azure AD
3. Azure checks session (SSO)
4. Generates SAML Assertion
5. Sends to AWS
6. AWS validates signature
7. Calls STS AssumeRoleWithSAML
8. Temporary credentials issued
9. User logged into AWS

---

# ⚠️ Common Mistakes (VERY IMPORTANT)

### ❌ Wrong Role ARN format

→ Login fails

### ❌ Metadata not updated

→ Signature error

### ❌ Time mismatch

→ SAML expired error

### ❌ Missing claims

→ No role assigned

---

# 🔐 Security Best Practices

* Use **least privilege policies**
* Avoid `iam:*` unless needed
* Rotate certificates (Azure metadata)
* Use **MFA in Azure AD**
* Limit session duration

---

# 🔥 Real DevOps Tip

If you are using:

* Terraform
* Multi-account AWS

👉 Use:

* AWS IAM Identity Center (SSO)
* Or automate:

  * IAM roles
  * SAML provider
  * Policies

---

# 🎯 One-Line Interview Summary

> “To set up Azure AD to AWS SAML federation, we create a SAML provider in AWS using Azure metadata, define IAM roles with trust policies, configure an enterprise application in Azure with SAML settings, map roles via claims, and assign users, enabling seamless SSO using AssumeRoleWithSAML.”

---
