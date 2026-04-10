# 🔍 AUDIT COMPLET ZSDEVWEB — Avril 2026

> **⚠️ FICHIER DE RÉFÉRENCE POUR ASSISTANT IA**
> Ce fichier contient l'audit complet de l'application et le plan d'action priorisé.
> À consulter en début de chaque conversation pour avoir le contexte.
> Mis à jour au fur et à mesure de l'avancement.

---

## 📖 Contexte du Projet

- **Nom :** Zsdevweb — Site vitrine + CRM freelance (développeur web)
- **Stack :** Django 5 (REST) + Vue.js 3 (Vite) + PostgreSQL + Redis + Celery + Docker
- **Cible :** TPE/PME de la métropole lilloise (Mouvaux, Roubaix, Tourcoing, Hem)
- **Objectifs :** Scalabilité, ajout de pages, paiement en ligne (Stripe), SEO local fort

### Architecture actuelle

```
ZSdevweb4/
├── backend/                    # Django 5 + DRF
│   ├── accounts/               # Auth JWT (AbstractUser, email login)
│   ├── quotes/                 # Devis (wizard, signature, PDF, emails)
│   ├── leads/                  # Leads qualifiés (scoring 0-100)
│   ├── contacts/               # Formulaire contact
│   ├── portfolio/              # Portfolio + témoignages
│   ├── services_catalog/       # Catalogue tarifs (ProjectType, Design, Complexity, Options)
│   ├── client_portal/          # Espace client (projets, updates, documents)
│   ├── company/                # Settings singleton (CompanySettings)
│   ├── audit/                  # Audit gratuit
│   ├── marketing/              # Marketing
│   ├── services/               # Service layer (pricing, quotes, PDF, email, recommendations)
│   ├── tests/                  # 2 fichiers seulement (pricing + quote service)
│   └── zsdevweb/settings/      # base.py / development.py / production.py
├── frontend/                   # Vue.js 3 + Vite + Tailwind CSS 3 + Pinia
│   ├── src/views/              # 14 vues (Home, Services, Portfolio, Contact, Devis, etc.)
│   ├── src/components/         # home/ layout/ quote/ ui/
│   ├── src/stores/             # auth, catalog, quote, ui
│   ├── src/api/                # 11 modules API (axios avec refresh JWT)
│   ├── src/composables/        # useLeadCapture, usePricing, useROI, useTheme, useToast
│   └── src/router/             # Vue Router avec meta titles
├── nginx/                      # Config nginx prod (security headers, gzip, X-Accel-Redirect)
├── docker-compose.yml          # Dev (db, redis, backend, celery, celery-beat, frontend)
├── docker-compose.prod.yml     # Prod (+ nginx, multi-stage builds)
└── .github/workflows/          # CI (ci.yml) + Deploy (deploy.yml)
```

### Points forts existants
- API versionnée `/api/v1/`
- Service layer propre (PricingService découplé de l'ORM)
- Celery pour async (emails, PDF, crons)
- JWT avec refresh token + OptionalJWTAuthentication
- Docker multi-stage prod avec user non-root
- UUID sur entités publiques
- Singleton CompanySettings avec cache Redis
- SEO : @unhead/vue, JSON-LD, robots.txt, sitemap plugin
- Healthchecks sur tous les services Docker

---

## 📊 Score de Maturité (Avril 2026)

| Catégorie | Score | Notes |
|---|---|---|
| Architecture & Scalabilité | 8/10 | drf-spectacular (Swagger/ReDoc), doc API complète |
| Sécurité | 9/10 | JWT cookie HttpOnly, throttling spécifique, Sentry, pre-commit |
| SEO | 7.5/10 | JSON-LD enrichi (LocalBusiness, AggregateRating, FAQPage, Service) |
| Performance | 8/10 | Lazy loading, WebP auto, cache API, fonts self-hosted |
| Tests & Qualité | 8.5/10 | 108 tests passent — API, Celery, Vitest, health, security, docs |
| Frontend (UX/DX) | 8/10 | Cache API, composables, Vitest, manque TypeScript |
| Infrastructure & DevOps | 8/10 | Docker mature, Sentry backend+frontend |
| Prêt pour Paiement | 3/10 | Tout à construire |
| **GLOBAL** | **8.5/10** | |

---

## 🔴 FAILLES CRITIQUES À CORRIGER EN PRIORITÉ

### 1. Timing attack sur tokens de signature (quotes/views.py)
- **Fichier :** `backend/quotes/views.py` lignes 148 et 182
- **Statut :** ✅ Corrigé — `constant_time_compare` utilisé

### 2. SECRET_KEY avec valeur par défaut
- **Fichier :** `backend/zsdevweb/settings/base.py` ligne 12
- **Statut :** ✅ Corrigé — `config('SECRET_KEY')` sans default

### 3. Aucun rate limiting sur endpoints publics
- **Statut :** ✅ Corrigé — DRF global (30/min anon, 100/min user) + `ScopedRateThrottle` sur `QuoteCreateView` (5/min) et `ContactRequestCreateView` (5/min)

### 4. JWT tokens dans localStorage (XSS vulnérable)
- **Fichier :** `frontend/src/stores/auth.js` + `frontend/src/api/axios.js`
- **Problème :** `localStorage.setItem('access_token', ...)` vulnérable XSS
- **Fix recommandé :** refresh_token en cookie HttpOnly, access_token en mémoire
- **Statut :** ✅ Corrigé — refresh_token HttpOnly, access_token en mémoire Pinia, withCredentials

---

## 📋 PLAN D'ACTION PRIORISÉ

### Phase 1 — Sécurité & Stabilité (1-2 semaines)

- [x] 1. Corriger comparaison token → `constant_time_compare` ✅
- [x] 2. Supprimer default SECRET_KEY en prod ✅
- [x] 3. Ajouter rate limiting endpoints publics ✅ (ScopedRateThrottle 5/min sur quotes + contacts)
- [x] 4. Ajouter throttling DRF global `AnonRateThrottle` + `UserRateThrottle` ✅ (30/min anon, 100/min user)
- [x] 5. Ajouter page 404 catch-all dans Vue Router ✅ (NotFoundView.vue)
- [x] 6. Ajouter error handler global Vue.js `app.config.errorHandler` ✅
- [x] 7. Configurer Sentry backend + frontend ✅ (activé via SENTRY_DSN + VITE_SENTRY_DSN)
- [x] 8. Ajouter pre-commit hooks (black, isort, flake8, gitleaks) ✅
- [x] 9. Migrer JWT vers cookie HttpOnly ✅ (refresh_token en HttpOnly, access_token en mémoire Pinia, withCredentials)

### Phase 2 — SEO & Performance (2-3 semaines)

- [ ] 9. Implémenter SSR/pre-rendering pour le SEO (3-5 jours)
  - Options : Nuxt.js (migration lourde) / vite-ssg / Prerender.io
- [x] 10. Créer page portfolio détaillée `/portfolio/:slug` ✅ (PortfolioDetailView.vue + API slug)
- [x] 11. Sitemap dynamique Django avec pages portfolio ✅ (sitemaps.py : StaticPagesSitemap + PortfolioSitemap)
- [x] 12. Compléter méta-données : og:image, canonical, twitter:card ✅ (toutes les vues principales)
- [x] 13. Données structurées : FAQPage ✅, Service ✅, AggregateRating ✅, LocalBusiness ✅ (HomeView + ServicesView)
- [x] 14. Lazy loading images + conversion WebP backend ✅ (signal Pillow, `<picture>` + WebP dans PortfolioSection + PortfolioDetail)
- [x] 15. Optimiser fonts ✅ (vite-plugin-webfont-dl, Inter 400/600/700, Jakarta Sans 600/700)
- [x] 16. Cache API frontend ✅ (composable `useApiCache` avec TTL 5 min, partagé entre composants)

### Phase 3 — Tests & Qualité (2-3 semaines)

- [x] 17. Tests API backend (auth, portfolio, contact, health) ✅ — `tests/test_api_endpoints.py` + `tests/factories.py`
- [x] 18. Tests Celery tasks ✅ (conftest.py + ALWAYS_EAGER + 18 tests : expire, cleanup, generate, lead follow-ups)
- [x] 19. Tests unitaires frontend ✅ (Vitest + useApiCache.test.js + authStore.test.js)
- [ ] 20. Tests E2E — Playwright (parcours devis + signature + espace client) (2 jours)
- [ ] 21. Migration TypeScript progressive frontend (ongoing)
- [x] 22. Documentation API avec drf-spectacular ✅ (/api/docs/ Swagger + /api/redoc/ en DEBUG)

### Phase 4 — Paiement Stripe (3-4 semaines)

- [ ] 23. Créer module `backend/payments/` (models, views, serializers) (3 jours)
  - Models : Payment, PaymentIntent, Invoice
  - Services : stripe_service.py, invoice_service.py
  - Webhooks : signature verification + idempotence
- [ ] 24. Intégrer Stripe SDK backend (`stripe`) + frontend (`@stripe/stripe-js`) (2 jours)
- [ ] 25. Webhooks Stripe avec signature verification (1 jour)
- [ ] 26. Page paiement frontend — Stripe Checkout ou Elements (2 jours)
- [ ] 27. Génération factures PDF automatiques (2 jours)
- [ ] 28. Adapter CSP nginx pour Stripe (font-src, connect-src, frame-src) (1h)
- [ ] 29. Tests paiement avec mocks Stripe (2 jours)
- [ ] 30. Refactorer Quote → QuotePricing + PaymentPlan (2 jours)

### Phase 5 — Scalabilité Long Terme (continu)

- [ ] 31. Blog Django + vues frontend (1 semaine) — levier SEO n°1
- [ ] 32. PWA / mode offline avec vite-plugin-pwa (2 jours)
- [ ] 33. Monitoring Prometheus + Grafana (2 jours)
- [ ] 34. Backup DB automatisé pg_dump + S3/Backblaze (3h)
- [ ] 35. Internationalisation vue-i18n (1 semaine)
- [ ] 36. Audit accessibilité WCAG 2.1 AA (2 jours)
- [ ] 37. Multi-tenancy SaaS si pertinent (3+ semaines)

---

## 🔧 DÉTAILS TECHNIQUES PAR CATÉGORIE

### Architecture — Améliorations clés

**Quote = God Model (25+ champs) → Refactoriser :**
```
Quote (base)
├── QuoteClient (infos client dénormalisées)
├── QuotePricing (snapshot prix, OneToOne)
└── PaymentPlan (échéances, prépare Stripe)
```

**Documentation API manquante → drf-spectacular :**
```python
# requirements.txt
drf-spectacular==0.28.x

# settings/base.py
INSTALLED_APPS += ['drf_spectacular']
REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

# urls.py
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
```

### SEO — Problème n°1 : SPA sans SSR

L'app est une SPA pure. Les moteurs reçoivent `<div id="app"></div>` vide.
**Solutions par priorité :**
1. Nuxt.js (SSR complet) — migration complète, meilleur résultat
2. vite-ssg (pre-rendering statique) — bon compromis
3. Prerender.io (service externe) — solution rapide temporaire

**Pages portfolio individuelles manquantes :**
- Ajouter route `/portfolio/:slug` dans Vue Router
- Créer `PortfolioDetailView.vue` avec données structurées par projet
- Ajouter au sitemap dynamique

**Données structurées à ajouter :**
- `FAQPage` → section FAQ page accueil
- `Service` → page services
- `AggregateRating` → témoignages
- `BreadcrumbList` → navigation
- `LocalBusiness` → enrichir le JSON-LD existant

### Performance — Actions clés

- Images : `loading="lazy"` + WebP + srcset (django-imagekit)
- Fonts : self-host Inter + Jakarta Sans, 3 poids max (400, 500, 700)
- Cache API : @tanstack/vue-query ou composable useApiCache
- CSP nginx à adapter pour Google Fonts ET Stripe

### Paiement Stripe — Architecture cible

```
POST /api/v1/payments/create-checkout/    → Crée CheckoutSession Stripe
POST /api/v1/payments/webhook/            → Reçoit webhooks Stripe
GET  /api/v1/payments/{quote_uuid}/       → Statut paiements d'un devis
GET  /api/v1/payments/{id}/invoice/       → PDF facture

Frontend:
/devis/:uuid/payer    → Page paiement (Stripe Checkout redirect ou Elements)
/paiement/succes      → Confirmation
/paiement/annule      → Annulation
```

**CSP nginx à modifier pour Stripe :**
```nginx
font-src 'self' https://fonts.gstatic.com;
connect-src 'self' https://api.stripe.com;
frame-src https://js.stripe.com https://hooks.stripe.com;
script-src 'self' https://js.stripe.com;
```

---

## 📝 DÉCISIONS EN ATTENTE (à valider par le développeur)

1. **SSR vs Pre-rendering** — Nuxt.js ou solution plus légère ?
2. **Stripe Checkout vs Elements** — Redirection ou formulaire intégré ?
3. **Blog** — Prioriser avant ou après le paiement ?
4. **TypeScript** — Migration progressive ou rester en JS ?
5. **Phase de démarrage** — Commencer par la sécurité (recommandé) ?

---

## 📅 HISTORIQUE DES MODIFICATIONS

| Date | Action | Statut |
|---|---|---|
| 2026-04-10 | Audit initial complet | ✅ Fait |
| 2026-04-10 | Phase 1 — Sécurité : items 1-8 complétés | ✅ Fait |
| 2026-04-10 | Phase 2 — SEO : items 10-13 complétés (portfolio detail, sitemap, JSON-LD) | ✅ Fait |
| 2026-04-10 | Phase 2 — Performance : WebP signal Pillow, lazy loading, cache API useApiCache | ✅ Fait |
| 2026-04-10 | Phase 3 — Tests API endpoints (auth, portfolio, contact, health) | ✅ Fait |
| 2026-04-10 | Phase 2 — Fonts self-hosted (vite-plugin-webfont-dl, poids réduits) | ✅ Fait |
| 2026-04-10 | Phase 3 — Tests Celery (18 tests, ALWAYS_EAGER, factories) | ✅ Fait |
| 2026-04-10 | Phase 3 — Tests Vitest (useApiCache + authStore, 15 tests) | ✅ Fait |
| 2026-04-10 | Architecture — drf-spectacular (Swagger + ReDoc en DEBUG) | ✅ Fait |
| 2026-04-10 | Phase 1 — JWT localStorage → cookie HttpOnly + mémoire Pinia | ✅ Fait |
| 2026-04-10 | Tests — 108/108 passent (health, security, docs, celery, quote service) | ✅ Fait |
| 2026-04-10 | Bugfixes — drf_spectacular doublon, ScopedRateThrottle manquant, related_name quotes | ✅ Fait |
| | Phase 2 — SEO : SSR/pre-rendering | ❌ En attente |
| | Phase 3 — Tests E2E Playwright | ❌ En attente |
| | Phase 4 — Paiement Stripe | ❌ En attente |
| | Phase 4 — Paiement | ❌ En attente |
| | Phase 5 — Scalabilité | ❌ En attente |

### Prochaines étapes recommandées

1. **Module payments/** (paiement) — Intégration Stripe (**étape majeure suivante**)
   - `backend/payments/` : models Payment/PaymentIntent, stripe_service.py, webhooks
   - Frontend : page `/devis/:uuid/payer`, Stripe Checkout, pages succès/annulation
   - Adapter CSP nginx pour Stripe (font-src, connect-src, frame-src)
2. **Tests E2E Playwright** (qualité) — Parcours devis wizard + signature + espace client
3. **SSR / Pre-rendering** (SEO) — Décision architecture : vite-ssg ou Nuxt.js
4. **Migration TypeScript** (qualité) — Progressive, commencer par les composables
