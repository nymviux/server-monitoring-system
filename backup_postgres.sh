#!/bin/bash

DB_NAME="monitoring"
DB_USER="db"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"


docker exec -t servermonitoringsystem-db-1 pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

echo "Backup zapisany do: $BACKUP_FILE"
