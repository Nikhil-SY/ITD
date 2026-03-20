```markdown id="mxrkt1"
# AWS Messaging Services (SNS & SQS)

---

# Question 1: Amazon SNS (Simple Notification Service)

## Definition
Amazon SNS is a **fully managed publish/subscribe (pub-sub) messaging service**.

👉 It is used to **send messages to multiple subscribers simultaneously (fan-out)**.

---

# Core Terminology (VERY IMPORTANT 🔥)

## 1. Publisher
👉 The **source/service that sends a message**

Examples:

- Application (Order Service)
- EC2 instance
- Lambda function  

---

## 2. Topic
👉 A **logical communication channel** in SNS where messages are sent

Think of Topic like:

📢 Broadcast channel

Example:

```

order-topic

```id="sns1"

---

## 3. Subscriber
👉 The **endpoint that receives messages from SNS**

Types:

- Email  
- SMS  
- SQS Queue  
- Lambda  
- HTTP/HTTPS  

---

## 4. Publish
👉 The action of **sending a message to a topic**

When you publish:

- SNS sends message to ALL subscribers  

---

# How SNS Works (Flow)

Publisher → SNS Topic → All Subscribers  

---

# SNS Types (VERY DETAILED 🔥)

---

## 1. SNS Standard Topic

### Definition
Standard SNS provides:

- At least once delivery  
- Best effort ordering  

---

### Characteristics

- Messages may be delivered multiple times  
- Order is NOT guaranteed  
- High throughput  

---

### Example Use Case

### Scenario: Notification System

When order is placed:

- Email sent  
- SMS sent  

Order of messages does NOT matter  

---

### Example

Messages:

```

Order Placed
Order Shipped

```id="sns_std1"

Possible delivery:

```

Order Shipped
Order Placed

```id="sns_std2"

👉 Order may change  

---

### When to Use

- Alerts  
- Notifications  
- Logging systems  

---

## 2. SNS FIFO Topic

### Definition
FIFO = First In First Out

Provides:

- Exactly once delivery  
- Strict ordering  

---

### Characteristics

- No duplicate messages  
- Order is preserved  
- Lower throughput  

---

### Requirements

- Must use `.fifo` in topic name  

Example:

```

order-topic.fifo

```id="sns_fifo1"

---

### Message Group ID (VERY IMPORTANT 🔥)

Defines ordering group

Example:

```

MessageGroupId: order-123

```id="sns_fifo2"

---

### Example Use Case

### Scenario: Payment Processing

Steps must be in order:

1. Order Created  
2. Payment Done  
3. Invoice Generated  

---

### Example

Messages:

```

Step1 → Step2 → Step3

```id="sns_fifo3"

Delivery:

✔ Step1 → Step2 → Step3 (same order)

---

### When to Use

- Financial systems  
- Payment processing  
- Order workflows  

---

# Question 2: Amazon SQS (Simple Queue Service)

## Definition
Amazon SQS is a **fully managed message queue service** used to **decouple applications**.

👉 Messages are stored and processed asynchronously.

---

# Core Terminology

## 1. Producer
👉 Sends message to queue  

---

## 2. Queue
👉 Stores messages  

Example:

```

order-queue

```id="sqs1"

---

## 3. Consumer
👉 Processes messages  

---

## 4. Message
👉 Data inside queue  

Example:

```

Order ID: 12345

```id="sqs2"

---

# SQS Types (VERY DETAILED 🔥)

---

## 1. Standard Queue

### Definition
Provides:

- At least once delivery  
- Best effort ordering  

---

### Characteristics

- Messages may be duplicated  
- Order not guaranteed  
- Very high throughput  

---

### Example

Messages sent:

```

M1, M2, M3

```id="sqs_std1"

Possible receive:

```

M2, M1, M3

```id="sqs_std2"

👉 Order not guaranteed  

---

### Duplicate Example

```

M1 processed twice

```id="sqs_std3"

👉 Must handle duplicates in application  

---

### Use Case

- Log processing  
- Background jobs  
- Notifications  

---

## 2. FIFO Queue

### Definition
Provides:

- Exactly once processing  
- Strict ordering  

---

### Characteristics

- No duplicate messages  
- Order preserved  
- Lower throughput  

---

### Naming Rule

Queue name must end with:

```

.fifo

```id="sqs_fifo1"

Example:

```

order-queue.fifo

```id="sqs_fifo2"

---

### Message Group ID (VERY IMPORTANT 🔥)

Defines ordering group

Example:

```

MessageGroupId: order-123

```id="sqs_fifo3"

---

### Deduplication ID

Prevents duplicate messages

Example:

```

MessageDeduplicationId: 12345

```id="sqs_fifo4"

---

### Example Use Case

### Scenario: Banking System

Transactions must be processed in order:

1. Debit  
2. Credit  

---

### Example

Messages:

```

Debit → Credit

```id="sqs_fifo5"

Processing:

✔ Debit first  
✔ Credit next  

---

### When to Use

- Banking systems  
- Payment processing  
- Order workflows  

---

# SNS + SQS Combined (VERY IMPORTANT 🔥)

## Scenario: Microservices Architecture

Order Service → SNS Topic →  
→ SQS Queue (Email Service)  
→ SQS Queue (Billing Service)  
→ SQS Queue (Shipping Service)  

---

## Flow

1. Order created  
2. SNS publishes event  
3. Each SQS queue gets message  
4. Services process independently  

---

# Standard vs FIFO (Final Comparison)

| Feature | Standard | FIFO |
|------|------|------|
Delivery | At least once | Exactly once |
Ordering | Not guaranteed | Strict |
Throughput | High | Lower |
Duplicates | Possible | Not allowed |

---

# Final Interview Points

- SNS → Push-based (fan-out)  
- SQS → Pull-based (queue)  
- Standard → Fast but no order guarantee  
- FIFO → Ordered but slower  
- MessageGroupId → Maintains order  
- DeduplicationId → Avoid duplicates  

👉 Use FIFO only when **order is critical**  
👉 Use Standard for **high performance systems**  
```


############################### SNS + SQS combined ################################################

# Additional: SNS + SQS Combined Use Case (DETAILED 🔥)

---

## Why Combine SNS and SQS?

👉 SNS alone = Push to multiple systems  
👉 SQS alone = Queue for processing  

👉 Together = **Scalable + Decoupled + Reliable architecture**

---

## Real-Time Scenario: E-commerce Order System

When an order is placed, multiple services must act:

- Email Service → Send confirmation  
- Billing Service → Process payment  
- Shipping Service → Prepare delivery  

---

## Problem Without SNS + SQS

If Order Service directly calls all services:

```

Order Service → Email Service
→ Billing Service
→ Shipping Service

```

❌ Tight coupling  
❌ If one service fails → whole flow fails  
❌ Not scalable  

---

## Solution Using SNS + SQS

---

## Architecture

```

Order Service (Publisher)
↓
SNS Topic
↓
┌───────────────┬───────────────┬───────────────┐
↓               ↓               ↓
SQS Queue      SQS Queue      SQS Queue
(Email)        (Billing)      (Shipping)
↓               ↓               ↓
Email Service  Billing Service Shipping Service

```

---

## Step-by-Step Flow

### Step 1: Order Placed

Order Service publishes message to SNS:

```

Order ID: 12345
Status: Created

```

---

### Step 2: SNS Fan-out

SNS sends SAME message to:

- Email Queue  
- Billing Queue  
- Shipping Queue  

---

### Step 3: SQS Queues Store Messages

Each queue stores message independently.

👉 Even if one service is down → message is safe  

---

### Step 4: Consumers Process Messages

- Email service reads from Email Queue  
- Billing service reads from Billing Queue  
- Shipping service reads from Shipping Queue  

---

## Key Advantages

### 1. Decoupling

Services do not depend on each other  

---

### 2. Fault Tolerance

If Billing fails:

✔ Message stays in queue  
✔ Retry later  

---

### 3. Scalability

- Increase consumers for heavy load  
- Each service scales independently  

---

### 4. Reliability

- No message loss  
- DLQ handles failures  

---

## Important Configuration (VERY IMPORTANT 🔥)

### Subscribe SQS to SNS

Steps:

1. Create SNS Topic  
2. Create SQS Queue  
3. Go to SNS → Create Subscription  
4. Select protocol:

```

Amazon SQS

```

5. Choose SQS queue  

---

### Allow SNS to Send to SQS (Policy REQUIRED 🔥)

👉 Add this policy to SQS queue

```

{
"Effect": "Allow",
"Principal": {
"Service": "sns.amazonaws.com"
},
"Action": "sqs:SendMessage",
"Resource": "arn:aws:sqs:REGION:ACCOUNT-ID:queue-name",
"Condition": {
"ArnEquals": {
"aws:SourceArn": "arn:aws:sns:REGION:ACCOUNT-ID:topic-name"
}
}
}

```

---

## Why This Policy is Needed

👉 By default:

❌ SNS CANNOT send messages to SQS  

👉 This policy allows:

✔ SNS → SQS communication  

---

## Real Interview Explanation (Best Answer 🔥)

👉 “SNS is used for fan-out messaging and SQS is used for decoupling.  
We combine SNS and SQS to ensure that messages are distributed to multiple services reliably, and each service processes them independently using queues.”

---

## When to Use SNS + SQS

- Microservices architecture  
- Event-driven systems  
- Order processing systems  
- Notification pipelines  

---

## Final Key Point

👉 SNS = Distribution  
👉 SQS = Storage + Processing  

👉 Together = **Highly scalable event-driven architecture**
```

---