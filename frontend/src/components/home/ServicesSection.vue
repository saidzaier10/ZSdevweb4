<template>
  <section id="services" class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="section-title">Ce que je construis pour vous</h2>
        <p class="section-subtitle mx-auto">
          Des solutions digitales sur mesure, pensées pour la performance et la conversion.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="service in services"
          :key="service.title"
          class="card group hover:shadow-lg transition-shadow duration-300"
        >
          <div :class="['w-12 h-12 rounded-xl flex items-center justify-center mb-4', service.bg]">
            <component :is="service.icon" :class="['w-6 h-6', service.iconColor]" />
          </div>
          <h3 class="font-bold text-gray-900 text-lg mb-2">{{ service.title }}</h3>
          <p class="text-gray-600 text-sm leading-relaxed mb-4">{{ service.description }}</p>
          <ul class="space-y-1">
            <li
              v-for="point in service.points"
              :key="point"
              class="flex items-center gap-2 text-sm text-gray-600"
            >
              <svg class="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ point }}
            </li>
          </ul>
        </div>
      </div>

      <div class="text-center mt-12">
        <RouterLink to="/services" class="btn-secondary">
          Voir tous les services →
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
const services = [
  {
    title: 'Site Vitrine',
    description: 'Un site professionnel qui reflète votre image et convertit les visiteurs en clients.',
    bg: 'bg-blue-50',
    iconColor: 'text-blue-600',
    icon: 'svg-globe',
    points: ['Design premium sur mesure', 'SEO optimisé', 'Responsive mobile', 'Performance maximale'],
  },
  {
    title: 'E-commerce',
    description: 'Une boutique en ligne complète avec paiement sécurisé et gestion des commandes.',
    bg: 'bg-green-50',
    iconColor: 'text-green-600',
    icon: 'svg-cart',
    points: ['Stripe / PayPal intégré', 'Gestion stocks', 'Tableau de bord', 'Analytics e-commerce'],
  },
  {
    title: 'Application Web',
    description: 'Des applications métier sur mesure qui automatisent vos processus.',
    bg: 'bg-purple-50',
    iconColor: 'text-purple-600',
    icon: 'svg-code',
    points: ['Vue.js + Django', 'API REST sécurisée', 'Authentification JWT', 'Architecture scalable'],
  },
  {
    title: 'Refonte de site',
    description: 'Modernisez votre site existant pour améliorer performance et conversions.',
    bg: 'bg-orange-50',
    iconColor: 'text-orange-600',
    icon: 'svg-refresh',
    points: ['Audit gratuit préalable', 'Migration sans perte', 'Amélioration Core Web Vitals', 'Résultats mesurables'],
  },
  {
    title: 'API & Intégrations',
    description: 'Connectez vos outils et automatisez vos flux de travail.',
    bg: 'bg-pink-50',
    iconColor: 'text-pink-600',
    icon: 'svg-api',
    points: ['API REST / GraphQL', 'Webhooks', 'Intégrations Zapier / Make', 'Documentation complète'],
  },
  {
    title: 'SaaS sur mesure',
    description: 'Construisez votre produit SaaS de zéro à la mise en production.',
    bg: 'bg-cyan-50',
    iconColor: 'text-cyan-600',
    icon: 'svg-saas',
    points: ['Architecture multi-tenant', 'Abonnements Stripe', 'Onboarding', 'Admin dashboard'],
  },
]
</script>
