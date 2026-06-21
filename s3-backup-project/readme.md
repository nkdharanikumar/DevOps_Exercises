# AWS S3 Backup and Restore Solution

## Project Overview

This project demonstrates a simple and effective backup and disaster recovery solution using Amazon S3 and Linux Shell Scripting.

The solution creates compressed backups of application files and configuration files, stores them securely in Amazon S3, and provides an automated restoration process to recover data in case of accidental deletion, corruption, or server failure.

---

## Problem Statement

In modern infrastructure, application files and configuration files are critical assets. If these files are accidentally deleted, corrupted, or lost due to server failure, the application may stop functioning.

Without a proper backup strategy:

* Application source code may be lost
* Configuration files may become unavailable
* Recovery can be time-consuming
* Business operations may be interrupted
* Manual reconstruction may be required

To avoid these issues, organizations implement backup and disaster recovery mechanisms.

---

## Objective

The primary objectives of this project are:

* Create backups of application files and configuration files
* Compress data into a single archive
* Store backups securely in Amazon S3
* Demonstrate disaster recovery through restoration
* Automate backup and restore operations using Shell Scripts

---

## Technologies Used

| Technology           | Purpose                   |
| -------------------- | ------------------------- |
| Linux (Ubuntu)       | Operating System          |
| Bash Shell Scripting | Automation                |
| AWS S3               | Remote Backup Storage     |
| AWS CLI              | Communication with AWS    |
| tar                  | Archiving and Compression |

---

## Project Architecture

```text
Application Files
       +
Configuration Files
       |
       v
Create tar.gz Archive
       |
       v
Upload to Amazon S3
       |
       v
Disaster Simulation
(Delete Files)
       |
       v
Download Backup
       |
       v
Restore Application
```

---

## Project Structure

```text
aws-s3-backup-restore/
│
├── opt/
│   └── myapp/
│       ├── app.py
│       └── index.html
│
├── etc/
│   └── myapp/
│       ├── config.yaml
│       └── db.conf
│
├── backup.sh
├── restore.sh
│
└── README.md
```

---

# Step 1: Create Application Files

Create project directories:

```bash
mkdir -p opt/myapp
mkdir -p etc/myapp
```

Create application files:

```bash
echo "print('Hello DevOps')" > opt/myapp/app.py

echo "<h1>Backup Demo</h1>" > opt/myapp/index.html
```

Create configuration files:

```bash
echo "environment=production" > etc/myapp/config.yaml

echo "database=mysql" > etc/myapp/db.conf
```

Verify:

```bash
tree .
```

Expected Structure:

```text
opt/myapp/app.py
opt/myapp/index.html

etc/myapp/config.yaml
etc/myapp/db.conf
```

---

# Step 2: Configure AWS CLI

Verify AWS CLI installation:

```bash
aws --version
```

Configure AWS credentials:

```bash
aws configure
```

Provide:

```text
AWS Access Key ID
AWS Secret Access Key
Region
Output Format
```

Verify connectivity:

```bash
aws s3 ls
```

---

# Step 3: Create Amazon S3 Bucket

Navigate to:

AWS Console → S3 → Create Bucket

Example Bucket Name:

```text
dk-devops-backup-2026
```

Configuration:

* Block Public Access: Enabled
* Versioning: Optional
* Region: Same as AWS CLI Region

Purpose:

The S3 bucket acts as remote storage for backup archives.

---

# Step 4: Create Manual Backup

Navigate to project directory:

```bash
cd aws-s3-backup-restore
```

Create archive:

```bash
tar -czf backup-v1.tar.gz opt etc
```

Explanation:

| Option | Meaning             |
| ------ | ------------------- |
| c      | Create archive      |
| z      | Compress using gzip |
| f      | Specify filename    |

Verify archive contents:

```bash
tar -tzf backup-v1.tar.gz
```

Expected Output:

```text
opt/
opt/myapp/
opt/myapp/app.py
opt/myapp/index.html

etc/
etc/myapp/
etc/myapp/config.yaml
etc/myapp/db.conf
```

Verify archive size:

```bash
ls -lh backup-v1.tar.gz
```

---

# Step 5: Upload Backup to S3

Upload archive:

```bash
aws s3 cp backup-v1.tar.gz s3://YOUR_BUCKET_NAME/
```

Example:

```bash
aws s3 cp backup-v1.tar.gz s3://dk-devops-backup-2026/
```

Verify upload:

```bash
aws s3 ls s3://YOUR_BUCKET_NAME/
```

Example Output:

```text
2026-06-21 22:28:37 362 backup-v1.tar.gz
```

---

# Step 6: Simulate Disaster

To demonstrate recovery capability, remove the application and configuration directories:

```bash
rm -rf opt
rm -rf etc
```

Verify:

```bash
tree .
```

Expected:

```text
.
└── backup-v1.tar.gz
```

This simulates:

* Accidental file deletion
* Server corruption
* Data loss scenarios

---

# Step 7: Restore From Backup

Download archive from S3:

```bash
aws s3 cp s3://YOUR_BUCKET_NAME/backup-v1.tar.gz .
```

Extract archive:

```bash
tar -xzf backup-v1.tar.gz
```

Verify restoration:

```bash
tree .
```

Expected:

```text
opt/
etc/

opt/myapp/app.py
opt/myapp/index.html

etc/myapp/config.yaml
etc/myapp/db.conf
```

Recovery completed successfully.

---

# Automated Backup Script

Create file:

```bash
nano backup.sh
```

Content:

```bash
#!/bin/bash

DATE=$(date +%Y-%m-%d-%H-%M-%S)

BACKUP_NAME="backup-$DATE.tar.gz"

tar -czf $BACKUP_NAME opt etc

aws s3 cp $BACKUP_NAME s3://YOUR_BUCKET_NAME/

echo "Backup completed: $BACKUP_NAME"
```

Make executable:

```bash
chmod +x backup.sh
```

Run:

```bash
./backup.sh
```

---

# Automated Restore Script

Create file:

```bash
nano restore.sh
```

Content:

```bash
#!/bin/bash

LATEST=$(aws s3 ls s3://YOUR_BUCKET_NAME/ | sort | tail -n 1 | awk '{print $4}')

echo "Downloading $LATEST"

aws s3 cp s3://YOUR_BUCKET_NAME/$LATEST .

tar -xzf $LATEST

echo "Restore completed"
```

Make executable:

```bash
chmod +x restore.sh
```

Run:

```bash
./restore.sh
```

---

# How the Backup Script Works

```text
Generate Timestamp
        |
        v
Create Compressed Archive
        |
        v
Upload to S3
        |
        v
Display Success Message
```

Example Backup Name:

```text
backup-2026-06-21-22-45-10.tar.gz
```

Benefits:

* No overwriting
* Historical backups maintained
* Easier recovery

---

# How the Restore Script Works

```text
Identify Latest Backup
         |
         v
Download From S3
         |
         v
Extract Archive
         |
         v
Restore Files
```

This ensures the most recent backup is always restored.

---

# Advantages of This Solution

* Simple to implement
* Cost-effective storage using S3
* Automated backup process
* Fast disaster recovery
* Scalable for larger applications
* Easy integration with cron jobs
* Follows basic DevOps backup practices

---

# Future Enhancements

* Enable S3 Versioning
* Lifecycle Policies
* Scheduled Backups using Cron
* Backup Encryption
* Email Notifications
* Multi-Region Replication
* Backup Monitoring Dashboard

---

# Learning Outcomes

Through this project, the following concepts were learned:

* Linux File Management
* Shell Scripting
* Data Compression using tar
* AWS S3 Operations
* AWS CLI Usage
* Backup and Recovery Concepts
* Disaster Recovery Fundamentals
* Automation in DevOps

---

# Conclusion

This project successfully demonstrates a complete backup and restore workflow using Amazon S3 and Shell Scripting. Application and configuration files were archived, uploaded to remote cloud storage, and restored successfully after simulated data loss. The implementation highlights core DevOps practices such as automation, disaster recovery, cloud storage integration, and infrastructure reliability.
