#!/bin/sh
set -e

echo "⏳ Attente de la base de données..."
python manage.py wait_for_db

echo "📦 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🌱 Chargement des fixtures (si nécessaire)..."
python manage.py loaddata fixtures/initial_catalog.json 2>/dev/null || echo "  → Fixtures déjà chargées ou non trouvées"

echo "✅ Démarrage du serveur Django (dev)..."
exec python manage.py runserver 0.0.0.0:8000
