.PHONY: dev prod build down logs shell migrate seed test lint help

# ============================================
# ZSDEVWEB — Makefile
# ============================================

help:
	@echo ""
	@echo "  ZSDEVWEB — Commandes disponibles"
	@echo "  ================================"
	@echo "  make dev        → Démarrer en mode développement"
	@echo "  make prod       → Démarrer en mode production"
	@echo "  make build      → Rebuilder les images Docker"
	@echo "  make down       → Arrêter les conteneurs"
	@echo "  make logs       → Voir les logs"
	@echo "  make shell      → Shell Django"
	@echo "  make migrate    → Appliquer les migrations"
	@echo "  make makemig    → Créer les migrations"
	@echo "  make seed       → Charger les données de démo"
	@echo "  make test       → Lancer les tests"
	@echo "  make lint       → Linter le code"
	@echo "  make superuser  → Créer un superutilisateur"
	@echo "  make psql       → Ouvrir psql"
	@echo ""

# === Développement ===

dev:
	@cp -n .env.example .env 2>/dev/null || true
	docker compose up --build

dev-bg:
	@cp -n .env.example .env 2>/dev/null || true
	docker compose up --build -d

down:
	docker compose down

down-v:
	docker compose down -v

build:
	docker compose build

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-frontend:
	docker compose logs -f frontend

# === Production ===

prod:
	docker compose -f docker-compose.prod.yml up --build -d

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

# === Django ===

shell:
	docker compose exec backend python manage.py shell

migrate:
	docker compose exec backend python manage.py migrate

makemig:
	docker compose exec backend python manage.py makemigrations

seed:
	docker compose exec backend python manage.py loaddata fixtures/initial_catalog.json
	docker compose exec backend python manage.py loaddata fixtures/portfolio_demo.json

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

collectstatic:
	docker compose exec backend python manage.py collectstatic --noinput

# === Base de données ===

psql:
	docker compose exec db psql -U zsdevweb -d zsdevweb

db-shell:
	docker compose exec db sh

# === Tests ===

test:
	docker compose exec backend pytest -v

test-cov:
	docker compose exec backend pytest --cov=. --cov-report=html -v

# === Qualité de code ===

lint:
	docker compose exec backend flake8 .
	docker compose exec frontend npm run lint

format:
	docker compose exec backend black .
	docker compose exec backend isort .

# === Utilitaires ===

ps:
	docker compose ps

restart-backend:
	docker compose restart backend

restart-frontend:
	docker compose restart frontend
