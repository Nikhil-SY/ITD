# Order matters: **`growpart` first, then `resize2fs`**

Correct sequence:

```text
1. Increase EBS size in AWS
2. growpart       → expand partition
3. resize2fs      → expand filesystem
4. Verify with df -h
```

### Why?

Think of layers:

```text
Disk (EBS)
   ↓
Partition
   ↓
Filesystem
   ↓
Files
```

You must expand **outer layer first**.

So:

* **`growpart`** → makes the **partition** bigger
* **`resize2fs`** → makes the **filesystem inside that partition** bigger

You cannot usually resize the filesystem beyond the partition size.

---

# Example

Before resize:

```text
/dev/xvdf   (disk)       20G
└─/dev/xvdf1 (partition) 10G
Filesystem (ext4)        10G
```

### Step 1: Expand partition

```bash
sudo growpart /dev/xvdf 1
```

After:

```text
/dev/xvdf   (disk)       20G
└─/dev/xvdf1 (partition) 20G
Filesystem (ext4)        still 10G
```

### Step 2: Expand filesystem

```bash
sudo resize2fs /dev/xvdf1
```

After:

```text
/dev/xvdf   (disk)       20G
└─/dev/xvdf1 (partition) 20G
Filesystem (ext4)        20G
```

---

# When can you skip `growpart`?

If your disk **has no partition**, for example:

```text
/dev/xvdf   mounted directly
```

(no `/dev/xvdf1`)

Then you can directly run:

```bash
sudo resize2fs /dev/xvdf
```

No `growpart` needed.

Check with:

```bash
lsblk
```

### If you see this:

```text
xvdf
└─xvdf1
```

✅ Use **`growpart` first**

### If you see this:

```text
xvdf
```

✅ Use **`resize2fs` directly**

---

# Interview One-Liner

**Use `growpart` first to expand the partition, then use `resize2fs` (or `xfs_growfs`) to expand the filesystem so the operating system can use the additional disk space.**


####################################################################################################



# How to Resize **Amazon Elastic Block Store (EBS)** Volume on **Amazon Elastic Compute Cloud (EC2)**

Resizing means increasing disk size, for example:

```text
10 GiB → 20 GiB
```

Important: **Amazon EBS supports increasing size online (without detaching).**

Flow:

```text
Modify EBS volume size
   ↓
AWS expands block storage
   ↓
Operating system detects bigger disk
   ↓
Expand partition (sometimes)
   ↓
Expand filesystem
   ↓
Application can use extra space
```

---

# 1. What actually happens?

Think of it like:

```text
EBS volume = Hard disk
Filesystem = Formatted usable space
```

When you increase EBS from **10 GiB to 20 GiB**:

```text
Disk becomes 20 GiB
Filesystem may still show 10 GiB
```

You must **expand the filesystem too**.

---

# 2. Step 1: Check current disk size

Run:

```bash
lsblk
```

### What `lsblk` does

Shows all block devices and sizes.

Example:

```text
NAME      SIZE
xvda       20G
xvdf       10G
```

Here:

* `xvdf` = EBS disk
* Current size = `10G`

Also check mounted usage:

```bash
df -h
```

Example:

```text
/dev/xvdf   10G   2G   8G   20%   /data
```

---

# 3. Step 2: Modify EBS size in **Amazon Web Services**

Go to:

[AWS Management Console](https://console.aws.amazon.com/?utm_source=chatgpt.com)
→ **EC2**
→ **Elastic Block Store → Volumes**
→ Select your volume
→ **Actions → Modify volume**

![Image](https://images.openai.com/static-rsc-4/HmiMMtdQ64tUes0OCDMBhuxCHKQ8tMlyGgcBSNglpaqGICsby-STHxA-sdj9RXeV0PS_tju0ECwWrQlZ3KEGfWgJvFEIaIcuNkTxivrb1sxCbksfKLhVq6rLgSiub5QqF87yglYsXCkG_eIIdEFL7p75xsc_dW4VwJ6xgT67HBMQ6NfpkjMxRXfLydqessvR?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/gpe99FzP20mO_zaLbmHt7ZDEGgBxHxVszVwN14VSFk18LS_Yf8IfaMOSSWEgrizhN-mAcX--564M0I9A6mqEnP8R0GHedWeKmI5943nhIrEpKxfoSyiM_TW2jdxnBwsYpdGyEbRcMeXZwO-hL4K4Dmk6K1zMwPDiwerEKWDq79TinbaoV-If_Y1cacEv__tI?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/E0yBbiMpZOeIKngA9JSMhP4rNsRB_n7rt_hpJREdyqzNUz9v0hgiSSZm3yoU2auAxTOPB6krQSShTS5pLhihrqOEL5y1YPU1OT-Dm8Rz6DwxdmYZ18Xhc4xYsm4VDNHAgSaGkEJqWz1Zwi6DE0EUT_f342OoUmTICPsB6FiDFO8efj1E1VuvnNxa7zU-hdS-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CoNVbm8sPYlR4MR90XiYsL-76BiTrPE2qXI6g1QlYVHX5V-u3C6Udex_PWeQr82hmE3xcE4kS0uHnvgussxjbGqTs5V0SrlU3ysi9X6hAvjtqI55mceQmU6HoNmg4IfAFhq4aDlNSP3RzNWBbV5dKxDCa8tyZ8fNyrWyNGsG-yf-aBJoOyR4H3qPDcH5HDqF?purpose=fullsize)

Change:

```text
Size: 10 → 20
```

Click **Modify** → **Yes**

---

# 4. Step 3: Wait for AWS to finish resizing

Check volume state in console:

```text
modifying → optimizing → completed
```

You can also check using CLI:

```bash
aws ec2 describe-volumes-modifications
```

### What this does

Shows modification progress.

Example:

```text
ModificationState: optimizing
```

---

# 5. Step 4: Make Linux detect the new size

Run:

```bash
lsblk
```

Example now:

```text
NAME      SIZE
xvdf       20G
```

Good—Linux sees bigger disk.

But filesystem may still be 10 GiB:

```bash
df -h
```

```text
/dev/xvdf   10G
```

That means filesystem expansion is still needed.

---

# 6. Step 5: Expand the filesystem

This depends on filesystem type.

Check filesystem:

```bash
df -Th
```

Example:

```text
/dev/xvdf   ext4
```

---

## Case A: **ext4 filesystem** (most common)

Run:

```bash
sudo resize2fs /dev/xvdf
```

### What this does

* `resize2fs` = expand ext filesystem
* Uses newly available disk space

Example output:

```text
Resizing the filesystem...
The filesystem is now 5242880 blocks long.
```

---

## Case B: **xfs filesystem**

Common on **Amazon Linux 2**

Run:

```bash
sudo xfs_growfs /data
```

### What this does

Expands **XFS** filesystem.

Important:

For XFS, you grow using the **mount point**, not the device.

---

# 7. Step 6: Verify the resize

Run:

```bash
df -h
```

Now:

```text
/dev/xvdf   20G
```

Success.

---

# Special Case: If volume has a partition

Sometimes disk looks like:

```text
xvdf
└─xvdf1
```

That means:

* `xvdf` = disk
* `xvdf1` = partition

Then you must expand partition first.

Check:

```bash
lsblk
```

Example:

```text
xvdf      20G
└─xvdf1   10G
```

Partition still old size.

---

## Expand partition

Install tool if needed:

```bash
sudo yum install -y cloud-utils-growpart
```

Or on Ubuntu:

```bash
sudo apt install cloud-guest-utils
```

Then run:

```bash
sudo growpart /dev/xvdf 1
```

### What this does

* `growpart` = enlarge partition
* `/dev/xvdf` = disk
* `1` = partition number (`xvdf1`)

After that:

```bash
sudo resize2fs /dev/xvdf1
```

or:

```bash
sudo xfs_growfs /data
```

---

# Full Example

Current:

```text
EBS size = 10G
Mounted at /data
Filesystem = ext4
```

Commands:

```bash
# Check current
lsblk
df -h

# Modify in AWS console (10 → 20)

# Verify OS sees new size
lsblk

# Expand filesystem
sudo resize2fs /dev/xvdf

# Confirm
df -h
```

Result:

```text
/dev/xvdf   20G
```

---

# Common issues

## `df -h` still shows old size

Cause:

Filesystem not expanded.

Fix:

```bash
sudo resize2fs /dev/xvdf
```

---

## `resize2fs: Bad magic number`

Cause:

Filesystem is **xfs**, not ext4.

Check:

```bash
df -Th
```

Use:

```bash
sudo xfs_growfs /data
```

---

## Partition not resized

If `xvdf1` exists, use:

```bash
sudo growpart /dev/xvdf 1
```

---

# Important limitations

✅ Increase size: supported
❌ Decrease size: not supported directly

To shrink:

* Create snapshot
* Create smaller volume
* Restore data

---

# Interview One-Liner

**To resize an Amazon EBS volume, first increase the volume size in AWS, then make the operating system detect the new capacity, expand the partition if needed, and finally grow the filesystem using tools like `resize2fs` or `xfs_growfs`.**
