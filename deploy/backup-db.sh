#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./deploy/backup-db.sh
#   BACKUP_DIR=/opt/backups ./deploy/backup-db.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
FILENAME="zsdevweb_${TIMESTAMP}.sql.gz"
OUTPUT_PATH="$BACKUP_DIR/$FILENAME"

mkdir -p "$BACKUP_DIR"

# Charge les variables DB depuis .env sans afficher les secrets.
set -a
source "$PROJECT_ROOT/.env"
set +a

if [[ -z "${POSTGRES_DB:-}" || -z "${POSTGRES_USER:-}" ]]; then
  echo "POSTGRES_DB/POSTGRES_USER manquants dans .env"
  exit 1
fi

if ! docker compose ps db >/dev/null 2>&1; then
  echo "Le service db n'est pas disponible. Lance d'abord docker compose up -d"
  exit 1
fi

echo "Creation du backup PostgreSQL..."
docker compose exec -T db sh -c "pg_dump -U '$POSTGRES_USER' '$POSTGRES_DB'" | gzip > "$OUTPUT_PATH"

echo "Backup cree: $OUTPUT_PATH"
