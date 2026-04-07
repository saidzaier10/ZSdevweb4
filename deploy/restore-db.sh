#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./deploy/restore-db.sh /absolute/path/to/backup.sql.gz

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /absolute/path/to/backup.sql.gz"
  exit 1
fi

BACKUP_FILE="$1"
if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Fichier introuvable: $BACKUP_FILE"
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

set -a
source "$PROJECT_ROOT/.env"
set +a

if [[ -z "${POSTGRES_DB:-}" || -z "${POSTGRES_USER:-}" ]]; then
  echo "POSTGRES_DB/POSTGRES_USER manquants dans .env"
  exit 1
fi

echo "Restauration de la base $POSTGRES_DB depuis $BACKUP_FILE"
zcat "$BACKUP_FILE" | docker compose exec -T db sh -c "psql -U '$POSTGRES_USER' -d '$POSTGRES_DB'"

echo "Restauration terminee"
