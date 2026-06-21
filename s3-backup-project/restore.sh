#!/bin/bash

LATEST=$(aws s3 ls s3://dk-s3-backup-project/ | sort | tail -n 1 | awk '{print $4}')

echo "Downloading $LATEST"

aws s3 cp s3://dk-s3-backup-project/$LATEST .

tar -xzf $LATEST

echo "Restore completed"
