#!/bin/bash
# This script will perform a backup on both the DB and data files of invenio RDM

# This command will ensure that the script exits if any command within it fails.
set -e

# Ensure the backups directory exists
mkdir -p ~/backups/

# Data backup: Perform the tar command on data
echo "Initiating data backup process..."
echo "Starting files backup..."
tar -czf "~/backups/kth-rdm-files-v11-$(date +%Y-%m-%d).tar.gz" -C ~/.pyenv/versions/kth-rdm-v10-2-venv/var/instance/data/ .
echo "Files backup completed."

echo "Starting DB backup..."
# DB backup: Perform the docker command and dump the output into a file in the ~/backup directory
docker exec kth-rdm-db-1 pg_dump -U kth-rdm -Fc > ~/backups/kth-rdm-db-v11-$(date +%Y-%m-%d).dump
echo "DB backup completed."

echo "Backup operation has completed successfully."

# Restore:
# Restore files:
# unzip the files at the same location
# tar -xzvf ~/backups/kth-rdm-v11-files-$(date +%Y-%m-%d).tar.gz -C ~/.pyenv/versions/kth-rdm-v10-2-venv/var/instance
# Restore DB:
# docker exec -i kth-rdm-db-1 pg_restore -U kth-rdm -d dbname -Fc < ~/backups/kth-rdm-db-v11-$(date +%Y-%m-%d).dump
