#!/bin/bash

DB_NAME="monitoring"
DB_USER="db"
BACKUP_DIR="./backups"
CONTAINER="servermonitoringsystem-db-1"
BACKUP_FILE="$1"

mkdir -p "$BACKUP_DIR"


cat "$BACKUP_FILE" | docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME"

echo "Przywrócono bazę '$DB_NAME' z pliku: $BACKUP_FILE"

