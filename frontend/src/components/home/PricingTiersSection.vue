<template>
  <section class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="section-title">Choisissez votre offre</h2>
        <p class="section-subtitle mx-auto">Des tarifs transparents adaptés à chaque étape de votre croissance.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          v-for="tier in tiers"
          :key="tier.name"
          :class="[
            'card relative',
            tier.featured ? 'ring-2 ring-primary-500 shadow-xl' : ''
          ]"
        >
          <div v-if="tier.featured" class="absolute -top-3 left-1/2 -translate-x-1/2">
            <span class="bg-primary-600 text-white text-xs font-bold px-4 py-1 rounded-full">
              Populaire
            </span>
          </div>

          <div class="mb-6">
            <h3 class="font-bold text-gray-900 text-xl mb-1">{{ tier.name }}</h3>
            <p class="text-gray-500 text-sm">{{ tier.description }}</p>
            <div class="mt-4">
              <span class="text-4xl font-bold text-gray-900">{{ tier.price }}</span>
              <span class="text-gray-500 text-sm ml-1">à partir de</span>
            </div>
          </div>

          <ul class="space-y-3 mb-8">
            <li v-for="feature in tier.features" :key="feature" class="flex items-center gap-2 text-sm">
              <svg class="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span class="text-gray-600">{{ feature }}</span>
            </li>
          </ul>

          <RouterLink
            to="/devis"
            :class="tier.featured ? 'btn-primary w-full justify-center' : 'btn-secondary w-full justify-center'"
          >
            Obtenir un devis
          </RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const tiers = [
  {
    name: 'Essentiel',
    price: '1 500€',
    description: 'Pour lancer votre présence en ligne',
    featured: false,
    features: ['Site vitrine 5 pages', 'Design responsive', 'Formulaire contact', 'Hébergement 1 an inclus', 'Livraison sous 3 semaines'],
  },
  {
    name: 'Pro',
    price: '4 000€',
    description: 'Pour développer votre activité',
    featured: true,
    features: ['Site complet jusqu\'à 15 pages', 'Design premium sur mesure', 'Blog / CMS', 'SEO avancé', 'Analytics', 'Support 3 mois', 'Livraison sous 6 semaines'],
  },
  {
    name: 'Premium',
    price: '8 000€',
    description: 'Pour dominer votre marché',
    featured: false,
    features: ['Application web complète', 'E-commerce ou SaaS', 'Intégrations API', 'Espace client', 'Formation équipe', 'Support 6 mois', 'Délai sur mesure'],
  },
]
</script>
