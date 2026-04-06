#!/bin/sh
set -e

echo "⏳ Attente de la base de données..."
python manage.py wait_for_db

echo "📦 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Démarrage de Gunicorn (prod)..."
exec gunicorn zsdevweb.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
