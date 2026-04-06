<template>
  <div>
    <section class="bg-gradient-to-br from-gray-900 to-primary-950 text-white py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Mes services</h1>
        <p class="text-gray-300 text-lg max-w-2xl mx-auto">Des solutions digitales sur mesure, livrées dans les délais, avec un code propre et maintenable.</p>
      </div>
    </section>

    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="service in services" :key="service.title" class="card hover:shadow-lg transition-shadow">
            <div :class="['w-12 h-12 rounded-xl flex items-center justify-center mb-4', service.bg]">
              <span class="text-2xl">{{ service.emoji }}</span>
            </div>
            <h3 class="font-bold text-gray-900 text-xl mb-2">{{ service.title }}</h3>
            <p class="text-gray-500 text-sm mb-4">{{ service.description }}</p>
            <ul class="space-y-2 mb-6">
              <li v-for="point in service.points" :key="point" class="flex items-center gap-2 text-sm text-gray-600">
                <svg class="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                {{ point }}
              </li>
            </ul>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-400">À partir de <strong class="text-gray-700">{{ service.startingPrice }}</strong></span>
              <RouterLink to="/devis" class="text-primary-600 text-sm font-semibold hover:underline">Devis →</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-gray-50">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-2xl font-bold text-gray-900 mb-8">Stack technique</h2>
        <div class="flex flex-wrap justify-center gap-3">
          <span v-for="tech in stack" :key="tech" class="bg-white border border-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium">{{ tech }}</span>
        </div>
      </div>
    </section>

    <section class="py-16 bg-primary-600 text-white text-center px-4">
      <h2 class="text-3xl font-bold mb-4">Prêt à démarrer ?</h2>
      <p class="text-primary-100 mb-8">Devis gratuit, réponse sous 24h.</p>
      <RouterLink to="/devis" class="bg-white text-primary-600 font-semibold px-8 py-4 rounded-xl hover:bg-gray-50 transition-colors inline-flex">
        Obtenir mon devis →
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
const services = [
  {
    title: 'Site Vitrine', emoji: '🌐', bg: 'bg-blue-50', startingPrice: '1 500€',
    description: 'Un site professionnel qui reflète votre image et convertit les visiteurs en clients.',
    points: ['Design responsive premium', 'SEO technique optimisé', 'Performance Core Web Vitals', 'Formulaire contact sécurisé'],
  },
  {
    title: 'E-commerce', emoji: '🛒', bg: 'bg-green-50', startingPrice: '4 500€',
    description: 'Boutique en ligne complète avec paiement sécurisé et gestion des commandes.',
    points: ['Stripe / PayPal / Apple Pay', 'Gestion stocks et commandes', 'Emails transactionnels', 'Dashboard analytics'],
  },
  {
    title: 'Application Web', emoji: '⚙️', bg: 'bg-purple-50', startingPrice: '6 000€',
    description: 'Applications métier sur mesure qui automatisent vos processus.',
    points: ['Vue.js 3 + Django REST', 'Auth JWT sécurisée', 'API documentée', 'Tests automatisés'],
  },
  {
    title: 'SaaS', emoji: '🚀', bg: 'bg-pink-50', startingPrice: '12 000€',
    description: 'Construisez votre produit SaaS de zéro à la mise en production.',
    points: ['Architecture multi-tenant', 'Abonnements Stripe', 'Onboarding utilisateur', 'Admin dashboard'],
  },
  {
    title: 'Refonte de site', emoji: '🔄', bg: 'bg-orange-50', startingPrice: '2 000€',
    description: 'Modernisez votre site existant pour améliorer performance et conversions.',
    points: ['Audit préalable offert', 'Migration sans perte', 'Amélioration Core Web Vitals', 'Résultats mesurables'],
  },
  {
    title: 'API & Intégrations', emoji: '🔗', bg: 'bg-cyan-50', startingPrice: '1 500€',
    description: 'Connectez vos outils et automatisez vos flux de travail.',
    points: ['API REST / GraphQL', 'Webhooks et intégrations', 'Zapier / Make', 'Documentation complète'],
  },
]

const stack = [
  'Vue.js 3', 'Nuxt.js', 'TypeScript', 'Tailwind CSS',
  'Django 5', 'Django REST Framework', 'PostgreSQL', 'Redis',
  'Docker', 'Nginx', 'Gunicorn', 'Stripe', 'JWT', 'GitHub Actions',
]
</script>
