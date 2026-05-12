# Storage Notes

# Question 1: Different Types of Storage in AWS

## Definition
Storage is used to store and retrieve data in cloud infrastructure.

In AWS, storage services are mainly divided into three categories based on how data is stored and accessed.

---

# 1. Block Storage

## Definition
Block storage divides data into fixed-size blocks and stores them separately.  
Each block has a unique identifier, and the operating system combines them to form files.

Example in AWS:
- Amazon Elastic Block Store (EBS)

Architecture:

Application  
↓  
Operating System  
↓  
EBS Volume  
↓  
Physical Storage  

---

## Characteristics

- Works like a hard disk
- Can attach to EC2 instances
- Suitable for databases and operating systems
- Supports low latency and high performance

---

# 2. File Storage

## Definition
File storage stores data in a hierarchical structure using files and folders.

Example in AWS:
- Amazon Elastic File System (EFS)

Folder Structure Example:

Folder  
 ├ File1  
 ├ File2  
 └ File3  

Characteristics:

- Uses Network File System (NFS) protocol
- Multiple EC2 instances can access the same storage
- Good for shared file systems

---

# 3. Object Storage

## Definition
Object storage stores data as objects instead of blocks or files.

Each object contains:
- Data
- Metadata
- Unique ID

Example in AWS:
- Amazon Simple Storage Service (S3)

Bucket Example:

Bucket  
 ├ Object1  
 ├ Object2  
 └ Object3  

Characteristics:

- Highly scalable
- Stores unstructured data
- Accessible through HTTP/HTTPS
- Used for backups, images, videos, and logs

---

# Storage Type Comparison

| Storage Type | Example | Use Case |
|------|------|------|
| Block Storage | EBS | Databases, OS |
| File Storage | EFS | Shared file systems |
| Object Storage | S3 | Backup, images, logs |

---

# Question 2: Different Types of EBS Volumes

EBS volumes are block storage devices attached to EC2 instances.

Volume Types:

1. General Purpose SSD (gp2 / gp3)
2. Provisioned IOPS SSD (io1 / io2)
3. Throughput Optimized HDD (st1)
4. Cold HDD (sc1)

---

## gp3 (General Purpose SSD)

Balanced performance and cost.

Use cases:
- Application servers
- Development environments
- Boot volumes

---

## io1 / io2 (Provisioned IOPS SSD)

High performance storage.

Use cases:
- Enterprise databases
- Financial systems
- High transaction workloads

---

## st1 (Throughput Optimized HDD)

Designed for large sequential workloads.

Use cases:
- Big data processing
- Log processing
- Data warehouses

---

## sc1 (Cold HDD)

Lowest cost storage.

Use cases:
- Backups
- Archival storage

---

# Question 3: Difference Between IOPS and Throughput

## IOPS (Input Output Operations Per Second)

Represents how many read/write operations a disk can perform per second.

Example:

5000 operations per second  
IOPS = 5000

Best for workloads with many small operations like:

- Databases
- Transaction systems

---

## Throughput

Represents the amount of data transferred per second.

Measured in:

MB/s or GB/s

Example:

200 MB per second  
Throughput = 200 MB/s

Best for workloads like:

- Video processing
- Big data
- Backup systems

---

## Comparison

| Feature | IOPS | Throughput |
|------|------|------|
| Measures | Number of operations | Amount of data |
| Unit | Ops/sec | MB/s |
| Example Workload | Database | Data analytics |

---

# Question 4: SSD vs HDD

## SSD (Solid State Drive)

Uses flash memory chips.

Characteristics:

- Very fast
- No moving parts
- Low latency
- Expensive

Use cases:

- Databases
- OS disks
- High performance applications

---

## HDD (Hard Disk Drive)

Uses spinning magnetic disks.

Characteristics:

- Mechanical parts
- Slower
- Higher latency
- Cheaper

Use cases:

- Backup
- Archive
- Large datasets

---

## Comparison

| Feature | SSD | HDD |
|------|------|------|
| Speed | Fast | Slow |
| Moving Parts | No | Yes |
| Latency | Low | Higher |
| Cost | Expensive | Cheap |

---

# Question 5: How to Use a Secondary EBS Volume Attached to EC2

When a new EBS volume is attached to EC2, it must be:

1. Detected
2. Formatted
3. Mounted

Only then it becomes usable.

---

# Step 1: Connect to EC2

Command:

ssh ec2-user@public-ip

Explanation:

ssh → Secure Shell command used to connect to remote Linux servers  
ec2-user → default user in Amazon Linux  
public-ip → IP address of EC2 instance

---

# Step 2: Check Attached Disks

Command:

lsblk

Explanation:

lsblk → List block devices command

Purpose:

Shows all storage devices attached to the system.

Example Output:

xvda   8:0   0   8G   0 disk
└─xvda1
xvdf   8:80  0  10G   0 disk

Explanation:

xvda → root disk (OS disk)  
xvdf → newly attached EBS volume

---

# Step 3: Create File System (Format the Disk)

Command:

sudo mkfs -t ext4 /dev/xvdf

Explanation:

sudo → run command with root privileges  
mkfs → make filesystem command  
-t → specify filesystem type  
ext4 → filesystem format  
/dev/xvdf → disk device name

Purpose:

Prepares the disk so the operating system can store files.

---

# Step 4: Create Mount Directory

Command:

sudo mkdir /data

Explanation:

mkdir → make directory  
/data → folder where the disk will be mounted

Purpose:

Creates a location where the disk will appear in the system.

---

# Step 5: Mount the Volume

Command:

sudo mount /dev/xvdf /data

Explanation:

mount → attaches a storage device to the filesystem  
/dev/xvdf → disk device  
/data → mount location

After mounting, the disk becomes accessible through /data.

---

# Step 6: Verify the Disk

Command:

df -h

Explanation:

df → disk filesystem usage  
-h → human readable format (GB/MB)

Purpose:

Shows all mounted disks and their usage.

Example:

Filesystem     Size  Used  Avail  Mounted on
/dev/xvdf      10G   1%    /data

---

# Step 7: Make Mount Permanent

Command:

sudo nano /etc/fstab

Explanation:

nano → text editor  
/etc/fstab → file system table

Purpose:

Stores mount configuration so disks automatically mount after reboot.

Add entry:

/dev/xvdf   /data   ext4   defaults,nofail   0   2

Meaning:

device → /dev/xvdf  
mount location → /data  
filesystem → ext4  
options → defaults,nofail

---

# Question 6: What is ext4 and XFS

These are **file systems used in Linux to organize data on disks**.

A filesystem defines how data is stored, retrieved, and managed on a disk.

---

# ext4 (Fourth Extended File System)

Most widely used Linux filesystem.

Characteristics:

- Stable and reliable
- Good performance
- Supports large files
- Supports journaling

Journaling means:

System records changes before writing data to disk, preventing data corruption during crashes.

Use cases:

- General Linux servers
- OS disks
- Application servers

---

# XFS File System

High performance filesystem designed for large-scale workloads.

Characteristics:

- High throughput
- Better for large files
- Faster parallel operations
- Good for big data workloads

Use cases:

- Large storage servers
- Big data
- High performance systems

---

# ext4 vs XFS Comparison

| Feature | ext4 | XFS |
|------|------|------|
| Stability | Very stable | Stable |
| Performance | Good | Better for large files |
| Best For | General Linux systems | High throughput workloads |
| Max File Size | Large | Very large |
| Journaling | Yes | Yes |

---

# Important Interview Points

- Secondary EBS must be **formatted and mounted**
- Use commands:
  - lsblk
  - mkfs
  - mount
  - df -h
- ext4 → common Linux filesystem
- XFS → high throughput filesystem
- Mount persistence is configured in **/etc/fstab**