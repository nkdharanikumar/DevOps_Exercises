#!/bin/bash

DATE=$(date +%Y-%m-%d-%H-%M-%S)

BACKUP_NAME="backup-$DATE.tar.gz"

tar -czf $BACKUP_NAME opt etc

aws s3 cp $BACKUP_NAME s3://dk-s3-backup-project/

echo "Backup completed: $BACKUP_NAME"
