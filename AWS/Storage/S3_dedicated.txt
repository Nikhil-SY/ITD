```id="s3storage"
# S3 Storage

# Question 1: Explain Everything About Amazon S3 (Simple Storage Service)

## Definition
Amazon S3 (Simple Storage Service) is an **object storage service** used to store and retrieve any amount of data from anywhere on the internet.

Data is stored as **objects inside containers called buckets**.

Structure:

Bucket  
 ├ Object (file)  
 ├ Object (image)  
 └ Object (video)

Each object contains:

- Data (actual file)
- Metadata (information about the file)
- Key (unique identifier)

Maximum object size:

0 bytes – 5 TB

Durability:

99.999999999% (11 nines)

---

# Question 2: Important Components of S3

## Bucket

A **bucket** is a container used to store objects.

Example bucket name:

```

nikhil-backup-data

```

Rules for bucket names:

- Must be globally unique
- Length: 3 – 63 characters
- Only lowercase letters, numbers, hyphen
- No spaces
- Cannot use uppercase letters

Example:

```

nikhil-prod-backup

```

---

## Object

Object is the **actual file stored in S3**.

Examples:

- photo.jpg
- logs.txt
- database.sql
- video.mp4

Each object contains:

- Key (file name)
- Data
- Metadata

Example:

```

Key: photo.jpg
Size: 2MB
Storage Class: Standard

```

---

## Key

A **key** is the unique identifier for an object.

Example:

```

logs/app1/log1.txt

```

S3 internally uses **flat storage**, but keys create a **folder-like structure**.

---

# Question 3: Creating an S3 Bucket

Steps:

1. Login to AWS Console  
2. Go to **Services → S3**  
3. Click **Create Bucket**  
4. Enter **Bucket Name**  
5. Select **Region**  
6. Configure **Public Access**  
7. Click **Create Bucket**

---

# Question 4: S3 Storage Classes and Their Use Cases

Storage classes help **optimize cost depending on access frequency**.

## S3 Standard
Used for **frequently accessed data**.

Use cases:

- Website images
- Application assets
- Mobile apps
- Streaming data

---

## S3 Intelligent Tiering
Automatically moves objects to cheaper tiers depending on access pattern.

Use cases:

- Social media photos
- User generated content
- Applications with unpredictable access patterns

---

## S3 Standard-IA (Infrequent Access)
Used for **data accessed rarely but requires quick retrieval**.

Use cases:

- Database backups
- Disaster recovery backups

---

## S3 One Zone-IA
Stored in **single Availability Zone**.

Use cases:

- Temporary files
- Re-creatable data
- Dev/test backups

---

## Glacier Instant Retrieval
Archive storage with **millisecond retrieval**.

Use cases:

- Medical records
- Media archives

---

## Glacier Flexible Retrieval
Retrieval takes **minutes to hours**.

Use cases:

- Long-term backup storage

---

## Glacier Deep Archive
Cheapest storage.

Retrieval time: **up to 12 hours**

Use cases:

- Compliance data
- Government records
- Legal archives

---

# Question 5: Multi-AZ Storage in S3

S3 automatically stores objects across **multiple Availability Zones in a region**.

Example region:

Mumbai (ap-south-1)

Possible AZs:

- ap-south-1a
- ap-south-1b
- ap-south-1c

When object is uploaded:

```

image.jpg

```

S3 replicates copies across multiple AZs.

Purpose:

- High durability
- Protection from AZ failure

Durability:

99.999999999%

---

# Question 6: S3 Lifecycle Rule

## Definition

A **Lifecycle Rule** automatically:

- Moves objects between storage classes
- Deletes objects after a specified time

Purpose:

- Reduce storage cost
- Automate data management

---

## Example Lifecycle Flow

Day 0 → S3 Standard  
Day 30 → Move to Standard-IA  
Day 90 → Move to Glacier  
Day 365 → Delete object

---

## Lifecycle Actions

### Transition

Move objects to cheaper storage.

Example:

```

30 days → Standard-IA
90 days → Glacier

```

---

### Expiration

Delete objects automatically.

Example:

```

Delete object after 365 days

```

---

# Question 7: S3 Bucket Policy

## Definition

A **Bucket Policy** is a **JSON-based access control policy attached to an S3 bucket** that defines who can access the bucket and what actions they can perform.

It controls permissions at **bucket level**.

Example actions controlled:

- Upload objects
- Download objects
- Delete objects

---

## Example Use Case

Allow users to **download files from a public bucket**.

Example policy idea:

```

Allow public read access to objects

```

Common scenarios:

1. Allow CloudFront to access bucket
2. Allow another AWS account to access bucket
3. Allow public website access

---

# Question 8: S3 Transfer Acceleration

## Definition

**S3 Transfer Acceleration** speeds up file uploads to S3 by using the **AWS global edge location network**.

It reduces latency when uploading files from distant locations.

---

## How it Works

Without acceleration:

User → Internet → S3 Region

With acceleration:

User → Nearest Edge Location → AWS Backbone Network → S3 Bucket

This improves upload speed.

---

# Question 9: MFA in S3 (Multi-Factor Authentication)

## Definition

**MFA (Multi-Factor Authentication)** adds an extra security layer when performing sensitive S3 operations.

User must provide:

1. Password
2. MFA code (OTP from device)

---

## MFA Delete

MFA Delete prevents **accidental or malicious deletion of objects**.

When enabled, users must provide:

- Account password
- MFA token

to perform operations like:

- Delete object versions
- Disable versioning

---

# Question 10: Checksum in Amazon S3

## Definition

A **Checksum** is a value calculated from file data that is used to **verify data integrity during upload and download**.

It ensures the **file stored in S3 is identical to the original file**.

If data corruption occurs during transfer, checksum values will not match.

---

## Supported Algorithms

- CRC32  
- CRC32C  
- SHA1  
- SHA256  

---

# Question 11: Static Website Hosting in S3

## Definition

**Static Website Hosting** in S3 allows you to **host a static website directly from an S3 bucket without using a web server like Apache or Nginx**.

A **static website** contains files that do not change dynamically.

Examples:

- HTML
- CSS
- JavaScript
- Images

These files are simply **served to users through HTTP**.

---

# Example Static Website Files

Example website structure:

```

index.html
style.css
script.js
logo.png

```

These files are uploaded to an **S3 bucket**, and users access them through a public URL.

---

# Architecture of Static Website Hosting

User → Internet → S3 Bucket → Website Files

Example flow:

1. User opens website URL
2. Request goes to S3 bucket
3. S3 returns the file (HTML page)
4. Browser renders the website

---

# Steps to Enable Static Website Hosting

Step 1

Create an S3 bucket.

Example:

```

nikhil-static-website

```

---

Step 2

Upload website files.

Example:

```

index.html
error.html
style.css
image.png

```

---

Step 3

Enable Static Website Hosting.

Go to:

```

Bucket → Properties → Static Website Hosting

```

Enable:

```

Enable Static Website Hosting

```

---

Step 4

Configure **index document**.

Example:

```

index.html

```

This file loads when users open the website.

---

Step 5

Configure **error document**.

Example:

```

error.html

```

This file loads if page is not found.

---

Step 6

Make bucket objects **public**.

Add bucket policy allowing public read access.

Example policy idea:

```

Allow public read access

```

---

Step 7

Access the website using S3 website endpoint.

Example URL:

```

[http://bucket-name.s3-website-region.amazonaws.com](http://bucket-name.s3-website-region.amazonaws.com)

```

Example:

```

[http://nikhil-static-website.s3-website-ap-south-1.amazonaws.com](http://nikhil-static-website.s3-website-ap-south-1.amazonaws.com)

```

---

# Static Website Hosting Use Cases

1. Personal portfolio website
2. Company landing page
3. Documentation website
4. Frontend hosting for web applications

Example architecture:

User → CloudFront (optional) → S3 static website

---

# Advantages of S3 Static Website Hosting

- Very low cost
- Highly scalable
- No server management
- High durability
- Easy deployment

---

# Limitations

- Only supports **static content**
- Cannot run backend code
- No server-side processing

Dynamic features require services like:

- EC2
- Lambda
- API Gateway

---

# Important S3 Limits

Object size:

0 bytes – 5 TB

Bucket limit per AWS account:

10,000 buckets

---

# Key Interview Points

- S3 is **object storage**
- Objects stored inside **buckets**
- Maximum object size **5 TB**
- Data stored across **multiple Availability Zones**
- Lifecycle rules automate **data transitions and deletion**
- Bucket policies control **bucket access**
- Transfer Acceleration speeds up **global uploads**
- MFA Delete protects **critical data**
- Checksum ensures **data integrity**
- S3 can host **static websites without a web server**
```
