```markdown
# IAM (Identity and Access Management)

## Question 1: Explain Everything About IAM

## 1. What is IAM

IAM (Identity and Access Management) is an AWS service used to **securely control access to AWS resources**.

It helps you define:

- **Who can access AWS**
- **What actions they can perform**
- **Which resources they can access**

Example:

- Developer → Can launch EC2 instances
- Admin → Full access to AWS
- Intern → Read-only access to S3

IAM works using **authentication and authorization**.

Authentication = Who are you  
Authorization = What are you allowed to do

---

# 2. IAM Components

There are **five main components in IAM**

1. Users  
2. Groups  
3. Roles  
4. Policies  
5. Identity Providers

---

# 3. IAM User

## Definition

An IAM User represents a **person or application that interacts with AWS**.

Example users:

- DevOps Engineer
- Developer
- Application

Each user has **credentials** to access AWS.

Types of credentials:

1. Password → For AWS Console login
2. Access Key → For CLI / API access

Example user:

```

User: nikhil-devops

```

This user may have permissions like:

- Start EC2
- Stop EC2
- Upload to S3

---

# 4. IAM Group

## Definition

A Group is a **collection of IAM users**.

Instead of assigning permissions to each user, you assign permissions to a group.

Example:

Group: Developers

Users inside group:

```

nikhil
rahul
arjun

```

Permissions attached to group:

```

EC2 Full Access

```

Now all users in the group automatically get the same permissions.

Benefits:

- Easier permission management
- Avoid repetitive configurations

Example groups:

- Developers
- DevOps
- Admins
- ReadOnlyUsers

Important:

A user can belong to **multiple groups**.

---

# 5. IAM Policy

## Definition

A Policy is a **JSON document that defines permissions**.

Policies determine:

- Which actions are allowed or denied
- On which resources
- Under what conditions

Example policy:

Allow user to list S3 buckets.

```

{
"Effect": "Allow",
"Action": "s3:ListBucket",
"Resource": "*"
}

```

Key elements in policies:

Effect → Allow or Deny  
Action → What operation is allowed  
Resource → Which AWS resource

---

# 6. Types of IAM Policies

## 1. AWS Managed Policies

Policies created and maintained by AWS.

Example:

- AmazonS3FullAccess
- AmazonEC2FullAccess
- AdministratorAccess

Benefits:

- Easy to use
- Automatically updated by AWS

---

## 2. Customer Managed Policies

Policies created by users in their AWS account.

Example:

Custom policy allowing only:

- Start EC2
- Stop EC2

---

## 3. Inline Policies

Policies directly attached to a single user, group, or role.

Not reusable.

Example:

Policy attached only to user:

```

nikhil

```

---

# 7. IAM Role

## Definition

A Role is an **identity that can be assumed temporarily to gain permissions**.

Roles do not have permanent credentials.

Instead, they provide **temporary security credentials**.

---

## Example 1

EC2 instance accessing S3 bucket.

Without role:

- Access keys must be stored on server (security risk)

With role:

- EC2 instance assumes role
- Gets temporary credentials

Example role:

```

EC2-S3-Access-Role

```

Permissions:

```

Read from S3

```

---

## Example 2

Lambda accessing DynamoDB.

Lambda assumes a role like:

```

Lambda-DynamoDB-Access

```

---

# 8. IAM Role Use Cases

Common scenarios:

1. EC2 accessing S3
2. Lambda accessing DynamoDB
3. Cross-account access
4. Applications accessing AWS services

---

# 9. IAM Authentication Methods

Users authenticate using:

1. Console password
2. Access keys
3. Multi-Factor Authentication (MFA)

---

# 10. Access Keys

Used for **programmatic access**.

Example:

Used with:

- AWS CLI
- SDK
- Applications

Access keys contain:

```

Access Key ID
Secret Access Key

```

Example CLI command:

```

aws s3 ls

```

This command uses access keys to authenticate.

---

# 11. Multi-Factor Authentication (MFA)

MFA adds **extra security layer**.

User must provide:

1. Password
2. OTP from mobile device

Example:

User login flow:

```

Username
Password
OTP

```

Benefits:

- Prevents unauthorized access
- Protects sensitive operations

---

# 12. Principle of Least Privilege

This means giving **minimum permissions required to perform a task**.

Example:

Instead of:

```

AdministratorAccess

```

Give:

```

EC2StartStopAccess

```

Benefits:

- Improved security
- Reduced risk

---

# 13. IAM Role vs IAM User

| Feature | IAM User | IAM Role |
|------|------|------|
Credentials | Permanent | Temporary |
Used by | Humans / apps | AWS services |
Access keys | Yes | No |
Example | Developer login | EC2 accessing S3 |

---

# 14. IAM Best Practices

1. Never use root account for daily work  
2. Enable MFA for root user  
3. Use IAM roles instead of access keys  
4. Follow least privilege principle  
5. Rotate access keys regularly  
6. Use groups for permission management  

---

# 15. Root User

Root user is the **owner of AWS account**.

It has **full access to all AWS services**.

Root user should only be used for:

- Account setup
- Billing changes
- Critical account configurations

Best practice:

Enable **MFA for root account**.

---

# 16. Cross Account Access

Sometimes one AWS account needs access to resources in another account.

Example:

Account A → Dev account  
Account B → Production account

Account A can assume a role in Account B.

Flow:

```

User → Assume Role → Temporary Credentials → Access Resources

```

---

# 17. IAM Policy Evaluation Logic

When a request is made:

AWS checks permissions in this order.

1. Explicit Deny
2. Explicit Allow
3. Default Deny

Example:

If a policy contains:

```

Deny s3:DeleteObject

```

Then deletion is always blocked.

Even if another policy allows it.

---

# 18. IAM Use Case Example

Example scenario in company.

Team:

Developers  
DevOps  
Security

Permissions:

Developers:

- Read S3
- Deploy applications

DevOps:

- Manage EC2
- Manage Auto Scaling

Security team:

- Read logs
- Audit access

Groups created:

```

Developers
DevOps
Security

```

Policies attached accordingly.

---

# Key Interview Points

IAM stands for **Identity and Access Management**

Used to **control access to AWS resources**

Main components:

- Users
- Groups
- Roles
- Policies

Roles provide **temporary credentials**

Policies are written in **JSON**

Follow **Least Privilege Principle**

Root account should **not be used daily**
```


#########################################################################################


# Question 2: Assume Role (VERY DETAILED – WHERE + HOW)

## Real-Time Scenario

- Account A → Developer Account  
- Account B → Production Account  
- Goal → Developer in A should **read S3 in B**

---

## STEP 1: Create Role (IN ACCOUNT B ✅)

Go to:

Account B → IAM → Roles → Create Role

---

## STEP 2: Add TRUST POLICY (IN ACCOUNT B ✅)

👉 This tells **who can assume the role**

```

{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Principal": {
"AWS": "arn:aws:iam::ACCOUNT-A-ID:root"
},
"Action": "sts:AssumeRole"
}
]
}

```

✔ Created in: **Account B**  
✔ Meaning: Account A users can assume this role  

---

## STEP 3: Attach PERMISSION POLICY (IN ACCOUNT B ✅)

👉 This defines **what the role can do**

```

{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": ["s3:GetObject","s3:ListBucket"],
"Resource": "*"
}
]
}

```

✔ Created in: **Account B**  
✔ Meaning: Once assumed → can read S3  

---

## STEP 4: Give Permission to User (IN ACCOUNT A ✅)

User in Account A must have permission to assume role.

```

{
"Effect": "Allow",
"Action": "sts:AssumeRole",
"Resource": "arn:aws:iam::ACCOUNT-B-ID:role/Prod-ReadOnly-Role"
}

```

✔ Created in: **Account A**  
✔ Meaning: User is allowed to assume role in B  

---

## STEP 5: How User Uses It

### CLI Method

```

aws sts assume-role 
--role-arn arn:aws:iam::ACCOUNT-B-ID:role/Prod-ReadOnly-Role 
--role-session-name test

```

---

## STEP 6: Where Credentials Come From (VERY IMPORTANT 🔥)

STS returns:

```

AccessKeyId
SecretAccessKey
SessionToken

```

👉 These are NOT stored permanently anywhere

---

## STEP 7: Where Credentials Are STORED

They are stored:

- In CLI → `~/.aws/credentials` (temporary profile)
- In environment variables

Example:

```

export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=yyy
export AWS_SESSION_TOKEN=zzz

```

---

## STEP 8: How They Are USED

Now when user runs:

```

aws s3 ls

```

👉 AWS uses these temporary credentials to authenticate

---

# Question 3: STS (DETAILED – INTERNAL WORKING)

## Where STS Credentials Are Stored

### Case 1: CLI User

Stored in:

```

~/.aws/credentials

```

or environment variables

---

### Case 2: EC2 Instance (VERY IMPORTANT 🔥)

Credentials are stored in:

👉 **Instance Metadata Service (IMDS)**

URL inside EC2:

```

[http://169.254.169.254/latest/meta-data/iam/security-credentials/](http://169.254.169.254/latest/meta-data/iam/security-credentials/)

```

---

## How EC2 Gets Credentials

### Step-by-Step

1. Attach Role to EC2  
2. EC2 calls metadata service  
3. Metadata service calls STS  
4. STS returns temporary credentials  
5. EC2 stores them in metadata  

---

## Example

Run inside EC2:

```

curl [http://169.254.169.254/latest/meta-data/iam/security-credentials/](http://169.254.169.254/latest/meta-data/iam/security-credentials/)

```

Output:

```

MyEC2Role

```

Then:

```

curl [http://169.254.169.254/latest/meta-data/iam/security-credentials/MyEC2Role](http://169.254.169.254/latest/meta-data/iam/security-credentials/MyEC2Role)

```

Output:

```

AccessKeyId
SecretAccessKey
Token
Expiration

```

---

## How Application Uses It

When you run:

```

aws s3 ls

```

AWS SDK automatically:

- Fetches credentials from metadata  
- Uses them to authenticate  

👉 No need to store keys manually  

---

# Question 4: Federation (WHERE + HOW)

## Scenario

Company uses **Active Directory (AD)**

---

## Where Things Are Created

### Step 1: Create Identity Provider (IN AWS ACCOUNT)

IAM → Identity Providers → Add provider

Example:

```

SAML Provider (ADFS)

```

---

### Step 2: Create Role (IN AWS ACCOUNT)

Trust policy:

```

{
"Effect": "Allow",
"Principal": {
"Federated": "arn:aws:iam::ACCOUNT-ID:saml-provider/ADFS"
},
"Action": "sts:AssumeRoleWithSAML"
}

```

---

### Step 3: Attach Permissions (IN AWS)

Example:

```

Allow S3 access

```

---

## Flow

1. User logs into company portal  
2. AD authenticates user  
3. Sends SAML token to AWS  
4. AWS STS validates token  
5. Role is assumed  
6. Temporary credentials generated  

---

## Where Credentials Are Stored

- Browser session (console login)
- Temporary session token

---

# Question 5: Policy Conditions (WHERE + HOW)

## Example: Restrict S3 Access to Office IP

### Where to Create

👉 Attach to:

- IAM User / Group / Role (Account A or B depending on usage)

---

## Policy

```

{
"Effect": "Allow",
"Action": "s3:*",
"Resource": "*",
"Condition": {
"IpAddress": {
"aws:SourceIp": "192.168.1.0/24"
}
}
}

```

---

## How It Works

If request comes from:

✔ 192.168.1.x → Allowed  
❌ Other IP → Denied  

---

## Example 2: MFA Enforcement

```

{
"Effect": "Allow",
"Action": "ec2:StopInstances",
"Resource": "*",
"Condition": {
"Bool": {
"aws:MultiFactorAuthPresent": "true"
}
}
}

```

👉 Without MFA → action fails  

---

# Question 6: Permission Boundaries (WHERE + HOW)

## Where to Create

👉 Created in same account where user/role exists

---

## Scenario

Admin allows developer to create users  
But wants to restrict permissions

---

## Step 1: Create Boundary Policy

```

{
"Effect": "Allow",
"Action": ["ec2:*","s3:*"],
"Resource": "*"
}

```

---

## Step 2: Attach Boundary to User

IAM → User → Permissions Boundary → Attach

---

## Step 3: Developer Creates New User

Even if they attach:

```

"Action": "*"

```

👉 Final permissions still limited to:

- EC2  
- S3  

---

## IMPORTANT

Boundary acts like **maximum permission ceiling**

---

# Question 7: SCP (WHERE + HOW)

## Where to Create

👉 Created in **AWS Organizations (Management Account)**

---

## Applied To

- Organizational Unit (OU)
- Individual Account

---

## Scenario

Company wants:

❌ No EC2 deletion in production

---

## SCP Policy

```

{
"Effect": "Deny",
"Action": "ec2:TerminateInstances",
"Resource": "*"
}

```

---

## Where Applied

Attach SCP to:

```

Production OU

```

---

## Result

Even if user has:

```

AdministratorAccess

```

👉 Still cannot terminate EC2  

---

## Key Concept

SCP = **Account level guardrail**

---

# FINAL END-TO-END FLOW (MOST IMPORTANT 🔥)

When user makes request:

Example:

```

aws s3 ls

```

AWS checks:

1. IAM Policy → Allow?  
2. Condition → Match?  
3. Permission Boundary → Allow?  
4. SCP → Allow?  

---

## FINAL DECISION

✔ Allowed → Only if ALL pass  
❌ Denied → If ANY fails  

---

# FINAL INTERVIEW LEVEL SUMMARY

- Assume Role → Created in TARGET account (B)  
- Trust Policy → Who can assume role  
- Permission Policy → What role can do  
- STS → Generates temporary credentials  
- EC2 gets credentials via **metadata service (169.254.169.254)**  
- Credentials stored **temporarily (env / metadata / CLI)**  
- Federation → External login (AD → STS → Role)  
- Conditions → Restrict access (IP, MFA, Time)  
- Permission Boundary → Max permission for user  
- SCP → Max permission for account  

❗ Explicit DENY always wins  
```


################################################################################################

```markdown
# IAM Access Analyzer & Policy Simulator & Policy Types

---

# Question 1: IAM Access Analyzer

## Definition
IAM Access Analyzer helps you **identify resources that are accessible from outside your AWS account**.

👉 Focus: **Security auditing (who can access my resources externally)**

---

## Example 1: Public S3 Bucket

### Policy (Applied on S3 Bucket)

👉 Created in: Same account where S3 bucket exists

```

{
"Effect": "Allow",
"Principal": "*",
"Action": "s3:GetObject",
"Resource": "*"
}

```

---

## What Happens

- Bucket becomes **public**
- Anyone on internet can access ❌
- Access Analyzer detects this

---

## Output

- Resource: S3 Bucket  
- Access: Public  
- Risk: High  

---

## Example 2: Cross Account Access

### Scenario

- Account A allowed to access resource in Account B  

Policy in Account B:

```

"Principal": {
"AWS": "arn:aws:iam::ACCOUNT-A-ID:root"
}

```

---

## Result

Access Analyzer shows:

👉 External access to Account A

---

## Use Cases

- Detect public S3 buckets  
- Detect unintended cross-account access  
- Security auditing  

---

# Question 2: IAM Policy Simulator

## Definition
Policy Simulator is used to **test IAM permissions before applying them**.

👉 Focus: **Will action be allowed or denied?**

---

## Example 1: Allow + Deny

Policy:

```

{
"Effect": "Allow",
"Action": "ec2:*",
"Resource": "*"
}

```

AND

```

{
"Effect": "Deny",
"Action": "ec2:TerminateInstances",
"Resource": "*"
}

```

---

## Test

Action:

```

ec2:TerminateInstances

```

Result:

❌ Denied

👉 Explicit Deny overrides Allow

---

## Example 2: Condition Failure

Policy:

```

{
"Effect": "Allow",
"Action": "s3:*",
"Resource": "*",
"Condition": {
"IpAddress": {
"aws:SourceIp": "192.168.1.0/24"
}
}
}

```

---

## Test

Request from:

```

10.0.0.1

```

Result:

❌ Denied (Condition failed)

---

## Use Cases

- Test user permissions  
- Debug access issues  
- Validate policies before production  

---

# Question 3: Identity-Based Policy vs Resource-Based Policy

---

## 1. Identity-Based Policy

## Definition
Policy attached to:

- IAM User  
- IAM Group  
- IAM Role  

👉 Controls what **that identity can do**

---

## Example

👉 Created in: Account where user exists

```

{
"Effect": "Allow",
"Action": "s3:ListBucket",
"Resource": "*"
}

```

---

## Meaning

User can:

- List S3 buckets  

---

## Use Case

Developer needs access to S3:

Attach policy to:

```

User: nikhil

```

---

## Flow

User → IAM Policy → Access Resource

---

## 2. Resource-Based Policy

## Definition
Policy attached directly to:

- S3 bucket  
- Lambda  
- SQS  
- KMS  

👉 Controls **who can access that resource**

---

## Example (S3 Bucket Policy)

👉 Created in: Account where resource exists

```

{
"Effect": "Allow",
"Principal": "*",
"Action": "s3:GetObject",
"Resource": "*"
}

```

---

## Meaning

- Anyone can access S3 objects  

---

## Example 2: Cross Account Access

```

{
"Effect": "Allow",
"Principal": {
"AWS": "arn:aws:iam::ACCOUNT-A-ID:root"
},
"Action": "s3:GetObject",
"Resource": "*"
}

```

---

## Meaning

- Account A users can access this bucket  

---

## Flow

Resource → Policy → Allows Identity

---

# Key Difference

| Feature | Identity-Based Policy | Resource-Based Policy |
|------|------|------|
Attached to | User/Role/Group | Resource |
Controls | What identity can do | Who can access resource |
Example | IAM User policy | S3 Bucket policy |

---

# Real-Time Combined Example

## Scenario

- User in Account A  
- S3 bucket in Account B  

---

## Step 1: Identity Policy (Account A)

```

Allow s3:GetObject

```

---

## Step 2: Resource Policy (Account B)

```

Allow Account A

```

---

## Final Result

✔ Access works ONLY if BOTH allow  

---

## Important Rule

Final Access =

Identity Policy  
+ Resource Policy  

---

# Final Interview Points

- Access Analyzer → Detects external/public access  
- Policy Simulator → Tests permissions (Allow/Deny)  
- Identity Policy → Attached to user/role  
- Resource Policy → Attached to resource  
- Cross-account requires BOTH policies  

❗ Explicit Deny overrides everything  
```
