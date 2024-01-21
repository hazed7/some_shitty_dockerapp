#!/bin/bash

DB_HOST="db"
DB_PORT="5432"
DB_USER="${POSTGRES_USER}"
DB_NAME="${POSTGRES_DB}"
DB_PASSWORD="${POSTGRES_PASSWORD}"

BACKUP_DIR="/backups"
BACKUP_NAME="db_backup_$(date +%Y%m%d%H%M%S).sql"

export PGPASSWORD="$DB_PASSWORD"

pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -F c > "$BACKUP_DIR/$BACKUP_NAME"

unset PGPASSWORD

echo "Backup created: $BACKUP_NAME"
