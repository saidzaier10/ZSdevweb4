# Zsdevweb — Plateforme de génération de leads & devis automatisés

Application SaaS complète pour un développeur freelance Vue.js/Django. Machine d'acquisition client avec simulateur de projet, générateur de devis intelligent, calculateur ROI et capture de leads à chaque étape.

## Stack technique

| Couche | Technologies |
|--------|-------------|
| Frontend | Vue.js 3, Vite, Tailwind CSS, Pinia, Vue Router, Axios |
| Backend | Django 5.2, Django REST Framework, SimpleJWT |
| Base de données | PostgreSQL 16 |
| Cache | Redis 7 |
| PDF | WeasyPrint |
| Proxy | Nginx 1.25 |
| Conteneurs | Docker + Docker Compose |

## Démarrage rapide

### Prérequis
- Docker Desktop installé et lancé
- `make` disponible (Linux/macOS) ou Git Bash (Windows)

### 1. Configurer l'environnement

```bash
cp .env.example .env
# Éditer .env si nécessaire (les valeurs par défaut fonctionnent en dev)
```

### 2. Lancer en développement

```bash
make dev
```

Cela démarre :
- **Frontend** → http://localhost:5173
- **Backend API** → http://localhost:8000/api/v1/
- **Swagger UI** → http://localhost:8000/api/v1/docs/ (dev)
- **OpenAPI schema** → http://localhost:8000/api/v1/schema/ (dev)
- **Django Admin** → http://localhost:8000/admin/
- **PostgreSQL** sur port 5432
- **Redis** sur port 6379

### 3. Initialiser la base de données

```bash
make migrate    # Applique les migrations
make seed       # Charge le catalogue de services
make createsuperuser  # Crée l'admin Django
```

## Sécurité API (résumé)

- Rate limiting activé sur les endpoints publics sensibles (devis, leads, contact, audit)
- Réponses rate limit standardisées en JSON HTTP 429
- Accès PDF devis protégé par token de signature (ou utilisateur authentifié)
- Rejet des emails temporaires sur les formulaires publics
- Génération/validation OpenAPI vérifiée en CI
- Monitoring Sentry optionnel activable via variables d'environnement
- Documentation API protégée en production (accès staff admin uniquement)
- Health endpoint enrichi avec checks base de données et cache

Endpoint health API :
GET /api/v1/health/ retourne 200 (ok) ou 503 (degraded) avec checks database/cache.
GET /api/v1/health/liveness/ retourne 200 si le process est vivant.
GET /api/v1/health/readiness/ retourne 200/503 selon disponibilité DB/Redis.

## Commandes `make`

```bash
make dev          # Démarre l'environnement de développement
make prod         # Démarre l'environnement de production
make down         # Arrête tous les conteneurs
make migrate      # Lance les migrations Django
make makemig      # Crée de nouvelles migrations
make seed         # Charge les fixtures (catalogue de services)
make test         # Lance les tests unitaires
make shell        # Ouvre un shell Django
make psql         # Ouvre une console PostgreSQL
make createsuperuser  # Crée un superutilisateur Django
make logs         # Affiche les logs en temps réel
```

## Backups base de données

```bash
make backup-db
# Crée un dump compressé dans ./backups/

make restore-db FILE=/chemin/absolu/backup.sql.gz
# Restaure la base actuelle depuis un dump

make prune-backups DAYS=7
# Supprime les dumps de plus de N jours
```

## Architecture

```
ZSdevweb4/
├── backend/
│   ├── services/              # Logique métier (PricingService, QuoteService, LeadService...)
│   ├── services_catalog/      # Catalogue: catégories, types de projets, options
│   ├── quotes/                # Modèle Quote + QuoteEmailLog
│   ├── leads/                 # Capture et scoring des leads
│   ├── contacts/              # Formulaire de contact
│   ├── audit/                 # Demandes d'audit gratuit
│   ├── portfolio/             # Projets et témoignages
│   ├── marketing/             # FAQ
│   ├── company/               # CompanySettings (singleton)
│   ├── templates/
│   │   ├── emails/            # Templates email (HTML + txt)
│   │   └── pdf/               # Template PDF WeasyPrint
│   ├── fixtures/
│   │   └── initial_catalog.json  # Données seed
│   └── tests/                 # Tests unitaires
├── frontend/
│   └── src/
│       ├── stores/            # Pinia: quote (wizard), auth, catalog, ui
│       ├── composables/       # usePricing, useROI, useLeadCapture, useQuoteWizard
│       ├── views/             # Pages Vue Router
│       └── components/        # Composants réutilisables
├── nginx/                     # Config Nginx production
├── scripts/                   # Entrypoints Docker
└── docker-compose.yml         # Dev
└── docker-compose.prod.yml    # Production
```

## Fonctionnalités principales

- **Simulateur de prix** — Estimation instantanée en 30 secondes (type de projet × complexité)
- **Calculateur ROI** — Démontre la rentabilité du projet en 12 mois
- **Wizard de devis** — 6 étapes guidées avec prix temps réel et capture de lead à l'étape 5
- **Génération de devis PDF** — Via WeasyPrint avec plan de paiement 30/40/30
- **Envoi par email** — Template HTML responsive + version texte
- **Système de leads** — Score additif, déduplication par email, sources traçées
- **Admin Django** — Gestion des devis, leads, portfolio, FAQ

## Déploiement en production

```bash
cp .env.example .env
# Configurer SECRET_KEY, DATABASE_URL, EMAIL_*, FRONTEND_URL, etc.

make prod
```

Checklist recommandée avant ouverture publique :
1. Configurer `.env` production (SECRET_KEY forte, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, CSRF_TRUSTED_ORIGINS)
2. Vérifier les checks applicatifs : `/api/v1/health/liveness/` puis `/api/v1/health/readiness/`
3. Exécuter la suite CI complète (backend tests, OpenAPI validate, nginx config check)
4. Effectuer un backup initial de la base (`make backup-db`) et planifier la retention (`make prune-backups`)
5. Créer/valider l'admin staff pour accès docs production
6. Tester le parcours critique (création devis, email, PDF, signature)
7. Activer le monitoring (Sentry DSN) et vérifier la remontée d'erreurs

La configuration de production utilise :
- Gunicorn avec workers Uvicorn (`-w 4 --worker-class uvicorn.workers.UvicornWorker`)
- Nginx comme reverse proxy et serveur de fichiers statiques
- Multi-stage Docker builds pour des images légères
- Fichiers statiques servis avec cache `1y` immutable

## Tests

```bash
make test
# ou directement :
docker-compose exec backend pytest tests/ -v
```

Les tests unitaires du `PricingService` sont entièrement purs (aucun accès DB, aucune migration).

## Variables d'environnement clés

| Variable | Description | Défaut dev |
|----------|-------------|-----------|
| `SECRET_KEY` | Clé secrète Django | `change-me` |
| `DEBUG` | Mode debug | `True` |
| `DATABASE_URL` | URL PostgreSQL | `postgresql://zsdevweb:devpassword@db:5432/zsdevweb` |
| `REDIS_URL` | URL Redis | `redis://redis:6379/0` |
| `VITE_API_URL` | URL de l'API (frontend) | `http://localhost:8000` |
| `EMAIL_BACKEND` | Backend email Django | `console` (dev) |
| `FRONTEND_URL` | URL publique du frontend | `http://localhost:5173` |

Voir `.env.example` pour la liste complète.
