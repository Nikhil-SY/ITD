Great 👍 Let’s do a **real-world, step-by-step setup of Route 53** in a practical way (like you’ll do in job/project).

---

# 🚀 Scenario

You want to host:

```
www.myapp.com → Load Balancer → EC2 instances
```

---

# 🧭 Step 1: Create Hosted Zone

## 🔹 Steps:

1. Login to **Amazon Web Services Console**
2. Go to **Route 53**
3. Click **Hosted Zones**
4. Click **Create Hosted Zone**

### 🔹 Fill details:

* Domain Name: `myapp.com`
* Type: **Public Hosted Zone**

👉 Click **Create**

---

## 🔹 Output:

You’ll get:

* **NS Records** (Name Servers)
* **SOA Record**

📌 Example:

```
ns-123.awsdns-45.com
ns-678.awsdns-12.net
```

---

# 🌐 Step 2: Update Domain Name Servers

👉 If you bought domain from:

* GoDaddy / Namecheap / etc.

## 🔹 Steps:

1. Go to domain provider
2. Find **DNS / Nameserver settings**
3. Replace with Route 53 NS records

📌 Example:

```
Old → GoDaddy NS
New → AWS Route 53 NS
```

⏳ Takes ~5–30 minutes (DNS propagation)

---

# 🖥️ Step 3: Create Infrastructure (EC2 + ALB)

## 🔹 3.1 Launch EC2 Instances

1. Go to EC2
2. Launch 2 instances
3. Install web server:

```bash
sudo yum install httpd -y
sudo systemctl start httpd
echo "Hello from Server 1" > /var/www/html/index.html
```

---

## 🔹 3.2 Create Application Load Balancer

1. Go to EC2 → Load Balancers
2. Click **Create Load Balancer**
3. Choose **Application Load Balancer**

### 🔹 Configure:

* Scheme: Internet-facing
* Listeners: HTTP (80)
* Target Group: Add EC2 instances

---

## 🔹 Output:

You’ll get:

```
my-alb-123456.ap-south-1.elb.amazonaws.com
```

---

# 🌍 Step 4: Create Record in Route 53

## 🔹 Steps:

1. Go to Hosted Zone → `myapp.com`
2. Click **Create Record**

---

## 🔹 Create Alias Record:

* Record Name: `www`
* Record Type: **A**
* Enable: ✅ Alias
* Target: Select ALB

👉 Save

---

## 🔹 Result:

```
www.myapp.com → ALB → EC2
```

---

# 🧪 Step 5: Test

Open browser:

```
http://www.myapp.com
```

✅ You should see:

* "Hello from Server 1"
* or Server 2 (load balanced)

---

# ⚡ Step 6: Add Health Check + Failover

---

## 🔹 6.1 Create Health Check

1. Go to Route 53 → Health Checks
2. Click **Create Health Check**

### Configure:

* Endpoint: ALB DNS
* Protocol: HTTP
* Path: `/`

---

## 🔹 6.2 Create Failover Records

### Primary Record:

* Name: `www`
* Type: A (Alias → ALB)
* Routing Policy: **Failover**
* Type: Primary
* Attach Health Check

---

### Secondary Record:

* Name: `www`
* Type: A
* Value: S3 static site OR backup server
* Routing Policy: Failover
* Type: Secondary

---

## 🔹 Result:

```
If ALB healthy → traffic goes to ALB
If ALB fails → traffic goes to backup
```

---

# 🌎 Step 7: Weighted Routing (Optional)

👉 For deployments

## Example:

| Server  | Weight |
| ------- | ------ |
| Old App | 80     |
| New App | 20     |

---

## 🔹 Steps:

* Create 2 records
* Same name
* Set routing policy = Weighted

---

# 🌍 Step 8: Latency-Based Routing (Optional)

👉 Multi-region setup

## Example:

* Mumbai ALB
* US ALB

Route 53 automatically routes based on latency

---

# 🔒 Step 9: Private Hosted Zone (Internal Apps)

## 🔹 Steps:

1. Create Hosted Zone
2. Select **Private**
3. Attach VPC

---

## Example:

```
internal.myapp.com → private EC2 IP
```

---

# 🧠 Real Interview Architecture

```
User → Route 53
       ↓
    ALB (Alias Record)
       ↓
   EC2 (Multi AZ)
       ↓
Health Check
       ↓
Failover → S3 Backup
```

---

# ⚠️ Common Mistakes

❌ Not updating nameservers
❌ Using CNAME at root domain
❌ Wrong TTL during testing
❌ Health check not attached

---

# 🎯 Pro Tips (Important for Interviews)

* Always use **Alias instead of CNAME for AWS resources**
* Keep TTL low (e.g., 60 sec) during testing
* Use **Weighted routing for blue/green deployments**
* Combine **Health Check + Failover**

---