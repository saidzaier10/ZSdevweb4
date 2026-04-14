# Zsdevweb — Site Vitrine + CRM Freelance

> **Document de référence IA** — Relire ce fichier en début de chaque conversation pour restaurer le contexte complet du projet.

Application complète pour un développeur freelance web ciblant les TPE/PME de la métropole lilloise (Mouvaux, Roubaix, Tourcoing, Hem). Combine un site vitrine SEO, un simulateur de prix, un wizard de devis, un CRM de leads, et un espace client.

---

## Stack Technique

| Couche | Technologies |
|--------|-------------|
| Frontend | Vue.js 3, Vite 5, Tailwind CSS 3, Pinia, Vue Router 4, Axios 1.15 |
| Backend | Django 5.0, Django REST Framework 3.15, SimpleJWT 5.3 |
| Base de données | PostgreSQL 16 |
| Cache / Broker | Redis 7 |
| PDF | WeasyPrint 62 |
| Tâches async | Celery 5.4 + django-celery-beat 2.6 |
| Monitoring | Sentry (backend + frontend) |
| Proxy | Nginx 1.25 (prod) |
| Conteneurs | Docker + Docker Compose |
| CI/CD | GitHub Actions (.github/workflows/) |

---

## Architecture du Projet

```
ZSdevweb4/
├── backend/
│   ├── accounts/              # Auth JWT (AbstractUser, login par email)
│   ├── quotes/                # Devis (wizard, signature, PDF, emails)
│   ├── leads/                 # Leads qualifiés (scoring additif 0-100)
│   ├── contacts/              # Formulaire de contact
│   ├── portfolio/             # Portfolio + témoignages
│   ├── services_catalog/      # Catalogue (ProjectType, DesignOption, ComplexityLevel, ProjectOption)
│   ├── client_portal/         # Espace client (projets, updates, documents)
│   ├── company/               # CompanySettings singleton (cache Redis)
│   ├── audit/                 # Demandes d'audit gratuit
│   ├── marketing/             # FAQ + marketing
│   ├── services/              # Service layer (PricingService, QuoteService, LeadService, PDFService, EmailService)
│   ├── tests/                 # Suite de tests (128 collectés, 52 sans Docker)
│   └── zsdevweb/settings/     # base.py / development.py / production.py
├── frontend/
│   └── src/
│       ├── views/             # 14+ vues (Home, Services, Portfolio, PortfolioDetail, Contact, Devis, etc.)
│       ├── components/        # home/ layout/ quote/ ui/
│       ├── stores/            # Pinia: auth, catalog, quote, ui
│       ├── api/               # 11 modules API (axios avec refresh JWT auto)
│       ├── composables/       # useLeadCapture, usePricing, useROI, useTheme, useToast, useApiCache
│       └── router/            # Vue Router avec meta titles et guards
├── nginx/                     # Config Nginx prod (security headers, gzip, X-Accel-Redirect)
├── docker-compose.yml         # Dev (db, redis, backend, celery, celery-beat, frontend)
├── docker-compose.prod.yml    # Prod (+ nginx, multi-stage builds)
└── .github/workflows/         # CI (ci.yml) + Deploy (deploy.yml)
```

---

## Score de Maturité (Avril 2026)

| Catégorie | Score | Notes |
|---|---|---|
| Architecture & Scalabilité | 9/10 | Dashboard admin, SOLID/DRY, signals idempotents, Celery tasks |
| Sécurité | 9/10 | JWT HttpOnly, throttling, Sentry, pre-commit, password reset sécurisé |
| SEO | 7.5/10 | JSON-LD enrichi (LocalBusiness, AggregateRating, FAQPage, Service) |
| Performance | 8/10 | Lazy loading, WebP auto, cache API, fonts self-hosted |
| Tests & Qualité | 8.5/10 | 128 collectés (52 sans Docker) — dashboard, register, is_staff |
| Frontend (UX/DX) | 9/10 | Tableau de bord admin, inscription, skeleton loading, redirect staff |
| Infrastructure & DevOps | 8/10 | Docker mature, Sentry backend+frontend |
| Prêt pour Paiement | 3/10 | Tout à construire |
| **GLOBAL** | **8.75/10** | |

---

## Décisions Techniques Critiques

### Espace Client — Architecture
- Notifications projet : signal `post_save` → `notify_client_project_update.delay()` (Celery, SRP)
- Password reset : `PasswordResetRequestView` délègue à `send_password_reset_email.delay()` — thread HTTP libéré immédiatement, même timing quelle que soit l'existence de l'email (anti-énumération)
- `MeView` : PATCH uniquement (`http_method_names`) — PUT incompatible avec `email` read-only
- Mutation store Pinia : via action `authStore.updateUser(data)`, jamais directement depuis une vue
- Couleurs de statut centralisées dans `statusColors.js` — un seul fichier à modifier pour tous les badges

### PDF & DB — Architecture
- `Quote.pdf_generated_at` : le `PdfService` fait `update_fields=['pdf_file', 'pdf_generated_at']` en une seule requête (pas de double save)
- `ProjectDocument.quote_source` : OneToOne sur Quote (`SET_NULL`) — garantit l'absence de doublon sans logique applicative
- Double signal idempotent : `on_client_project_saved` (chemin normal) + `attach_quote_pdf_to_portal` (chemin si statut accepted précède la création du projet) — les deux vérifient `filter(quote_source=quote).exists()` avant de créer
- `notify_admin_quote_signed` Celery task — découple la notification admin du thread HTTP de signature ; `_notify_admin_signature` inline supprimé de `views.py`

### JWT Authentication
- **refresh_token** : cookie HttpOnly (set par Django via `Set-Cookie`)
- **access_token** : en mémoire Pinia uniquement (jamais dans localStorage)
- `axios.defaults.withCredentials = true` sur tous les appels
- Intercepteur axios : sur 401, appelle `/api/v1/auth/token/refresh/` automatiquement

### PricingService (stateless, sans ORM)
- `services/pricing_service.py` — méthode de classe `full_breakdown(project_type, complexity, options, discount_percent)`
- Plan de paiement 30/40/30 avec correction d'arrondi sur la 3ème tranche
- TVA 20% incluse dans le calcul
- Testé sans DB dans `tests/test_quote_service.py`

### QuoteService
- `services/quote_service.py` — méthode **d'instance** : `QuoteService().create_from_wizard(wizard_data)`
- Importe les modèles Django **localement** à l'intérieur de la fonction (pas au niveau module)
- La capture de lead est gérée via un signal `post_save` sur Quote (SRP), pas dans QuoteService
- Le reverse FK de Quote vers Lead a `related_name='quotes'` → accessible via `lead.quotes`

### Rate Limiting
- Global DRF : `AnonRateThrottle` 30/min, `UserRateThrottle` 100/min
- Scoped : `quote_create` 5/min, `contact_create` 5/min, `auth_token` 10/min
- Classe : `ScopedRateThrottle` dans les views concernées (import requis)

### Documentation API (drf-spectacular)
- `/api/v1/schema/` → OpenAPI YAML
- `/api/v1/docs/` → Swagger UI (DEBUG only, sinon staff_member_required)
- `/api/v1/redoc/` → ReDoc (DEBUG only, sinon staff_member_required)
- `SPECTACULAR_SETTINGS` avec `bearerAuth` security scheme dans `settings/base.py`

---

## Endpoints API Principaux

```
Auth
  POST /api/v1/auth/token/          # Login → access_token + refresh_token cookie
  POST /api/v1/auth/token/refresh/  # Renouvelle access_token via cookie
  POST /api/v1/auth/token/blacklist/ # Logout

Devis
  POST /api/v1/quotes/              # Crée un devis (wizard) — throttle 5/min
  GET  /api/v1/quotes/{uuid}/       # Détail devis (auth ou token)
  POST /api/v1/quotes/{uuid}/sign/  # Signature électronique
  GET  /api/v1/quotes/{uuid}/pdf/   # Génère le PDF

Contact
  POST /api/v1/contacts/            # Formulaire contact — throttle 5/min

Portfolio
  GET  /api/v1/portfolio/           # Liste des projets
  GET  /api/v1/portfolio/{slug}/    # Détail projet

Health
  GET  /api/v1/health/              # Readiness (DB + cache)
  GET  /api/v1/health/liveness/     # Liveness only
  GET  /api/v1/health/readiness/    # Readiness (alias)

Catalog
  GET  /api/v1/catalog/project-types/
  GET  /api/v1/catalog/design-options/
  GET  /api/v1/catalog/complexity-levels/
  GET  /api/v1/catalog/options/

Espace client (auth requise)
  GET  /api/v1/client-portal/projects/
  GET  /api/v1/client-portal/projects/{id}/
```

---

## État d'Avancement

### Phase 1 — Sécurité ✅ Complète
- [x] Comparaison token via `constant_time_compare`
- [x] `SECRET_KEY` sans valeur par défaut
- [x] Rate limiting global + scoped
- [x] Page 404 Vue Router (`NotFoundView.vue`)
- [x] Error handler global Vue.js
- [x] Sentry backend + frontend
- [x] Pre-commit hooks (black, isort, flake8, gitleaks)
- [x] JWT → cookie HttpOnly + mémoire Pinia
- [x] Password reset sécurisé (token Django 24h, anti-énumération, async Celery)

### Phase 2 — SEO & Performance ✅ Quasi-complète
- [x] Page portfolio détaillée `/portfolio/:slug`
- [x] Sitemap dynamique Django (StaticPagesSitemap + PortfolioSitemap)
- [x] Méta-données : og:image, canonical, twitter:card
- [x] JSON-LD : FAQPage, Service, AggregateRating, LocalBusiness
- [x] Lazy loading images + conversion WebP (signal Pillow)
- [x] Fonts self-hosted (vite-plugin-webfont-dl, Inter 400/600/700)
- [x] Cache API frontend (composable `useApiCache` TTL 5 min)
- [ ] SSR / Pre-rendering (décision en attente : vite-ssg ou Nuxt.js)

### Phase 3 — Tests ✅ Complète (sauf E2E)
- [x] 128 tests collectés (52 passent sans Docker, 20 nouveaux : dashboard, register, is_staff)
- [x] Tests API (auth, portfolio, contact, health, security)
- [x] Tests Celery (18 tests, ALWAYS_EAGER, factories)
- [x] Tests Vitest frontend — 17 tests, jsdom installé, Playwright exclu du runner
- [x] Documentation API drf-spectacular
- [ ] Tests E2E Playwright (parcours devis + signature)

### Espace Client ✅ Complet
- [x] Header avec menu utilisateur authentifié (avatar, dropdown, déconnexion)
- [x] Redirect post-login préservant l'URL d'origine
- [x] Notifications email client sur `ProjectUpdate` (Celery, retry ×3)
- [x] Mot de passe oublié + reset (`ForgotPasswordView`, `ResetPasswordView`)
- [x] Page profil `/espace-client/profil` (infos + changement mot de passe)
- [x] `statusColors.js` centralisé, composants `UserMenuDropdown` + `DarkModeToggle`
- [x] Page inscription `/inscription` (`RegisterView.vue`) — auto-login post-register, erreurs champ par champ
- [x] `RegisterSerializer` — `username` auto-généré depuis l'email, doublon email détecté, `validate_password` Django

### PDF & Base de Données ✅ Complet
- [x] `Quote.pdf_generated_at` — timestamp de la dernière génération PDF
- [x] `ProjectDocument.quote_source` — FK OneToOne vers le devis source (auto-attachment, idempotent)
- [x] Type `'quote'` dans `ProjectDocument.TYPE_CHOICES`
- [x] Signal `on_client_project_saved` → PDF du devis auto-attaché en `ProjectDocument` à la création/liaison d'un `ClientProject`
- [x] Signal `attach_quote_pdf_to_portal` → même logique déclenchée si le devis est accepté en premier
- [x] `notify_admin_quote_signed` Celery task — notification admin signature désormais async (retry ×2)

### Tableau de Bord Admin ✅ Complet
- [x] `DashboardStatsView` — endpoint `/api/v1/quotes/dashboard/` protégé `IsAdminUser`
- [x] KPIs : CA total, CA ce mois, devis total/mois/en attente/acceptés, taux de conversion, projets actifs, audits en attente
- [x] 10 devis récents avec champs : `uuid`, `quote_number`, `client_name`, `total_ttc`, `status_display`, `created_at`
- [x] 10 projets actifs avec champs : `uuid`, `title`, `client_email`, `status_display`, `progress_percent`
- [x] 10 demandes d'audit récentes : `name`, `email`, `site_url`, `objectives`, `is_processed`, `created_at`
- [x] `DashboardView.vue` — skeleton loading, KPI cards, tableau devis, liste projets, liste audits, bouton Actualiser
- [x] `is_staff` exposé dans `UserSerializer` (read-only) — guard `requiresStaff` dans le router
- [x] Redirect post-login staff → `/tableau-de-bord`, clients → `/espace-client`
- [x] Lien "Tableau de bord" dans `UserMenuDropdown` (staff uniquement, avec séparateur)

### Accessibilité ✅ Complète (Lighthouse 100)
- [x] `aria-hidden="true"` sur 58 SVG décoratifs — 35 fichiers Vue (batch script Python)
- [x] Ratio contraste WCAG AA — `text-gray-500` → `text-gray-600` sur fonds clairs (50 fichiers)
- [x] `text-gray-400` → `text-gray-500` sur fonds clairs ; footer gardé (`text-gray-400` sur `bg-gray-900`)
- [x] IDs dupliqués — `BaseInput` et `PasswordInput` utilisent `getCurrentInstance().uid` (corrige `_counter` local qui se réinitialisait à chaque instance)

### Phase 6 — Améliorations UX & Workflow ❌ Non démarrée

Objectif : atteindre le niveau des outils freelance du marché (Bonsai, HoneyBook) sans réinventer la roue.
Priorité décidée le 2026-04-14.

#### 6.1 Notifications email automatiques — PRIORITÉ HAUTE
- [ ] Email admin à chaque nouvelle demande d'audit (actuellement silencieux)
- [ ] Email admin à chaque nouveau contact et nouveau devis
- [ ] Relance automatique si devis envoyé depuis 3 jours sans réponse (Celery beat)
- [ ] Email client automatique quand son projet change de statut (signal déjà présent, à vérifier)

#### 6.2 Actions rapides depuis le dashboard — PRIORITÉ HAUTE
- [ ] Bouton "Marquer traité" sur chaque demande d'audit dans `DashboardAuditsList.vue`
  - Endpoint PATCH `api/v1/audit/{id}/` avec `is_processed=True`
  - Mise à jour optimiste côté Vue
- [ ] Bouton "Renvoyer le lien de signature" sur les devis en statut `sent`
  - Réutiliser `QuoteSendView` ou créer `QuoteResendView`

#### 6.3 Pagination + filtre + recherche — PRIORITÉ HAUTE
- [ ] Backend : `django-filter` sur `QuoteListView` (filtre status, date, search client)
- [ ] Backend : pagination DRF `PageNumberPagination` (20 par page) sur devis et audits
- [ ] Frontend : `DashboardQuotesTable` — filtre status (select), recherche nom client (input debounce 300ms), pagination
- [ ] Frontend : `DashboardAuditsList` — filtre is_processed, pagination

#### 6.4 Graphiques dashboard — PRIORITÉ MOYENNE
- [ ] Ajouter endpoint `GET /api/v1/quotes/dashboard/charts/` retournant :
  - `revenue_by_month` : CA mensuel sur 12 mois (liste de 12 valeurs)
  - `quotes_by_month` : nombre de devis par mois
- [ ] Frontend : intégrer ApexCharts (`vue3-apexcharts`) — 2 graphiques : CA 12 mois (area) + devis/mois (bar)
- [ ] Ajouter `DashboardCharts.vue` dans `DashboardView.vue`

#### 6.5 Génération de facture depuis un devis accepté — PRIORITÉ MOYENNE
- [ ] Backend : modèle `Invoice` dans `quotes/` ou nouveau module `invoices/`
  - Champs : `quote` (FK), `invoice_number`, `issued_at`, `due_date`, `pdf_file`, `status` (draft/sent/paid)
- [ ] Service `InvoiceService.create_from_quote(quote)` — pré-remplit avec 30% acompte
- [ ] PDF WeasyPrint avec template facture distinct du devis
- [ ] Endpoint `GET /api/v1/invoices/{id}/pdf/`
- [ ] Dashboard : bouton "Créer facture" sur devis acceptés sans facture

#### 6.6 Suivi des paiements (sans Stripe) — PRIORITÉ MOYENNE
- [ ] Ajouter champs sur `Quote` : `deposit_paid_at`, `balance_paid_at`, `deposit_amount`
- [ ] Dashboard : indicateurs visuels "Acompte reçu / Solde reçu" sur les devis acceptés
- [ ] Permettre la mise à jour via PATCH depuis le dashboard

#### 6.7 Messagerie interne projet — PRIORITÉ BASSE
- [ ] Modèle `ProjectMessage` dans `client_portal/` : `project` (FK), `author` (FK User), `body`, `created_at`
- [ ] Endpoint `GET/POST /api/v1/client-portal/projects/{uuid}/messages/`
- [ ] Email de notification à l'autre partie à chaque nouveau message (Celery)
- [ ] Composant `ProjectMessaging.vue` dans l'espace client + vue dashboard

#### 6.8 PWA installable — PRIORITÉ BASSE
- [ ] Ajouter `vite-plugin-pwa` dans `vite.config.js`
- [ ] `manifest.json` : nom, icônes 192/512px, `start_url`, `display: standalone`, couleur `#2563eb`
- [ ] Service worker minimal (cache-first pour assets statiques, network-first pour API)
- [ ] Bannière "Installer l'app" dans l'espace client

---

### Phase 4 — Paiement Stripe ❌ Non démarré
Architecture cible :
```
POST /api/v1/payments/create-checkout/   → Crée CheckoutSession Stripe
POST /api/v1/payments/webhook/           → Reçoit webhooks Stripe
GET  /api/v1/payments/{quote_uuid}/      → Statut paiements d'un devis
GET  /api/v1/payments/{id}/invoice/      → PDF facture

Frontend:
/devis/:uuid/payer    → Page paiement
/paiement/succes      → Confirmation
/paiement/annule      → Annulation
```
CSP nginx à adapter pour Stripe (connect-src api.stripe.com, frame-src js.stripe.com).

### Phase 5 — Long terme ❌ Non démarré
- Blog Django (levier SEO n°1)
- PWA (vite-plugin-pwa)
- Monitoring Prometheus + Grafana
- Backup DB automatisé pg_dump + S3
- Migration TypeScript progressive

---

## Démarrage Rapide

### Prérequis
- Docker Desktop installé et lancé
- `make` disponible

### Lancer en développement

```bash
cp .env.example .env
make dev
```

Services disponibles :
- **Frontend** → http://localhost:5173
- **Backend API** → http://localhost:8000/api/v1/
- **Swagger UI** → http://localhost:8000/api/v1/docs/ (DEBUG only)
- **Django Admin** → http://localhost:8000/admin/
- **PostgreSQL** → port 5432
- **Redis** → port 6379

### Initialiser la base

```bash
make migrate
make seed           # Charge le catalogue initial
make createsuperuser
```

---

## Tests

```bash
make test
# ou directement :
docker-compose exec backend pytest tests/ -v

# Frontend
cd frontend && npm test
```

### Infrastructure de test (conftest.py)
- `celery_eager_mode` (autouse) : `CELERY_TASK_ALWAYS_EAGER = True`
- `disable_email_sending` (autouse) : `EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'`
- `use_dummy_cache` (autouse) : LocMemCache en test (pas Redis)
- `factories.py` : `make_portfolio_item()`, `make_testimonial()`, helpers devis

### Points d'attention pour les tests
- `auto_now_add=True` sur `Lead.created_at` : utiliser `.update()` pour rétrodater
- `Quote.save` est patchable via `@patch('quotes.models.Quote.save', autospec=True)`
- `QuoteService` est une instance (pas static) → `QuoteService().create_from_wizard(data)`
- `ProjectType` requiert une `category` FK → créer `ProjectCategory` d'abord
- Reverse accessor Lead→Quote : `lead.quotes` (related_name='quotes')

---

## Commandes Make

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
make backup-db    # Dump PostgreSQL compressé dans ./backups/
```

---

## Variables d'Environnement Clés

| Variable | Description | Dev par défaut |
|----------|-------------|----------------|
| `SECRET_KEY` | Clé secrète Django (OBLIGATOIRE, pas de défaut en prod) | `change-me` |
| `DEBUG` | Mode debug | `True` |
| `DATABASE_URL` | URL PostgreSQL | `postgresql://zsdevweb:devpassword@db:5432/zsdevweb` |
| `REDIS_URL` | URL Redis | `redis://redis:6379/0` |
| `VITE_API_URL` | URL de l'API (frontend) | `http://localhost:8000` |
| `EMAIL_BACKEND` | Backend email Django | `console` (dev) |
| `FRONTEND_URL` | URL publique du frontend | `http://localhost:5173` |
| `SENTRY_DSN` | DSN Sentry backend | vide = désactivé |
| `VITE_SENTRY_DSN` | DSN Sentry frontend | vide = désactivé |

---

## Fonctionnalités Principales

- **Simulateur de prix** — Estimation instantanée (type × complexité × options)
- **Calculateur ROI** — Démontre la rentabilité sur 12 mois
- **Wizard de devis** — 6 étapes guidées, capture de lead à l'étape 5
- **Génération PDF** — WeasyPrint, plan 30/40/30
- **Emails** — Templates HTML responsive + texte brut
- **Leads** — Score additif, déduplication email, sources traçées
- **Portfolio** — Projets avec slug, WebP auto, page détail
- **Espace client** — Suivi projets, documents, mises à jour
- **Admin Django** — Gestion devis, leads, portfolio, FAQ, CompanySettings

---

## Décisions en Attente

1. **SSR** — Nuxt.js (migration lourde) ou vite-ssg (pré-rendu statique) ?
2. **Stripe** — Checkout (redirection) ou Elements (formulaire intégré) ?
3. **Blog** — Avant ou après le paiement ?
4. **TypeScript** — Migration progressive ou rester en JS ?

---

## Historique Récent (Avril 2026)

| Date | Action |
|------|--------|
| 2026-04-10 | Audit initial complet |
| 2026-04-10 | Phase 1 Sécurité — items 1-9 complétés |
| 2026-04-10 | Phase 2 SEO — portfolio detail, sitemap, JSON-LD, WebP, fonts, cache API |
| 2026-04-10 | Phase 3 Tests — 108/108 passent (API, Celery, Vitest, health, security, docs) |
| 2026-04-10 | Architecture — drf-spectacular (Swagger + ReDoc) |
| 2026-04-10 | JWT localStorage → cookie HttpOnly + mémoire Pinia |
| 2026-04-10 | Bugfixes — doublon drf_spectacular, ScopedRateThrottle manquant, related_name quotes |
| 2026-04-10 | Dépendances — axios 1.15.0 (CVE SSRF), suppression doublons requirements.txt |
| 2026-04-14 | Espace client — header auth, redirect login, notifications email (Celery) |
| 2026-04-14 | Auth — password reset async, change-password, page profil |
| 2026-04-14 | Refacto — UserMenuDropdown, DarkModeToggle, statusColors.js |
| 2026-04-14 | Bugfixes build — StatusBadge export, vite-plugin-sitemap robots, Vitest include, jsdom |
| 2026-04-14 | DRY — email reset Celery, MeView PATCH-only, updateUser action Pinia |
| 2026-04-14 | PDF + DB — `pdf_generated_at`, `quote_source` FK, signals auto-attachment, `notify_admin_quote_signed` Celery |
| 2026-04-14 | Auth — page inscription `/inscription`, auto-login, username auto-généré, liens header |
| 2026-04-14 | Dashboard admin — `DashboardStatsView` (IsAdminUser), KPIs + devis récents + projets actifs |
| 2026-04-14 | Dashboard — `is_staff` dans UserSerializer, guard `requiresStaff`, redirect staff post-login |
| 2026-04-14 | Tests — 128 collectés (+20 : dashboard, register, is_staff) |
| 2026-04-14 | A11y — `aria-hidden="true"` batch sur 58 SVG décoratifs (35 fichiers) |
| 2026-04-14 | A11y — ratio contraste WCAG AA : `text-gray-500`→`text-gray-600` / `text-gray-400`→`text-gray-500` (52 fichiers) |
| 2026-04-14 | A11y — IDs dupliqués : `BaseInput` + `PasswordInput` → `getCurrentInstance().uid` |
| 2026-04-14 | Dashboard — demandes d'audit : `recent_audits` + KPI `audits_pending`, `DashboardAuditsList.vue` |
| 2026-04-14 | Phase 6 planifiée — notifications email, actions dashboard, pagination/filtre, graphiques, factures, paiements, messagerie, PWA |
