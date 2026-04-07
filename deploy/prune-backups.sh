#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./deploy/prune-backups.sh
#   BACKUP_DIR=/opt/backups BACKUP_RETENTION_DAYS=14 ./deploy/prune-backups.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "Dossier backup introuvable: $BACKUP_DIR"
  exit 0
fi

echo "Suppression des backups > ${RETENTION_DAYS} jours dans $BACKUP_DIR"
find "$BACKUP_DIR" -type f -name 'zsdevweb_*.sql.gz' -mtime +"$RETENTION_DAYS" -print -delete

echo "Retention appliquee"
