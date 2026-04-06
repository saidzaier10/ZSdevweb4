import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'Zsdevweb — Développeur Web Freelance' },
  },
  {
    path: '/services',
    name: 'services',
    component: () => import('@/views/ServicesView.vue'),
    meta: { title: 'Services — Zsdevweb' },
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    component: () => import('@/views/PortfolioView.vue'),
    meta: { title: 'Portfolio — Zsdevweb' },
  },
  {
    path: '/a-propos',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
    meta: { title: 'À propos — Zsdevweb' },
  },
  {
    path: '/contact',
    name: 'contact',
    component: () => import('@/views/ContactView.vue'),
    meta: { title: 'Contact — Zsdevweb' },
  },
  {
    path: '/devis',
    name: 'quote',
    component: () => import('@/views/QuoteView.vue'),
    meta: { title: 'Demande de devis — Zsdevweb' },
  },
  {
    path: '/devis/:uuid',
    name: 'quote-detail',
    component: () => import('@/views/QuoteDetailView.vue'),
    meta: { title: 'Votre devis — Zsdevweb' },
  },
  {
    path: '/estimation',
    name: 'estimate',
    component: () => import('@/views/EstimateView.vue'),
    meta: { title: 'Estimation rapide — Zsdevweb' },
  },
  {
    path: '/audit-gratuit',
    name: 'audit',
    component: () => import('@/views/AuditView.vue'),
    meta: { title: 'Audit gratuit — Zsdevweb' },
  },
  {
    path: '/mentions-legales',
    name: 'legal',
    component: () => import('@/views/LegalView.vue'),
    meta: { title: 'Mentions légales — Zsdevweb' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

router.afterEach((to) => {
  document.title = to.meta.title || 'Zsdevweb'
})

export default router
