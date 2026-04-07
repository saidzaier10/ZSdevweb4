<template>
  <div>
    <section class="bg-gradient-to-br from-gray-900 to-primary-950 text-white py-20 px-4">
      <div class="max-w-4xl mx-auto">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <div class="w-32 h-32 bg-primary-600 rounded-3xl flex items-center justify-center text-5xl flex-shrink-0">
            👨‍💻
          </div>
          <div>
            <h1 class="text-4xl font-bold mb-2">Bonjour, je suis Zsdevweb</h1>
            <p class="text-primary-300 text-lg mb-2">Développeur web freelance full-stack</p>
            <p class="text-gray-300">Vue.js · Django · PostgreSQL · Docker</p>
          </div>
        </div>
      </div>
    </section>

    <section class="py-20 bg-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
          <div class="lg:col-span-2 space-y-6">
            <h2 class="text-2xl font-bold text-gray-900">Mon parcours</h2>
            <p class="text-gray-600 leading-relaxed">
              Développeur web freelance avec plus de 5 ans d'expérience, je me spécialise dans la création
              d'applications web modernes et performantes. Mon approche : construire des produits qui génèrent
              de vraie valeur business, pas juste des sites vitrines.
            </p>
            <p class="text-gray-600 leading-relaxed">
              J'ai travaillé avec des startups, des PME et des indépendants dans des secteurs variés :
              e-commerce, immobilier, services B2B, SaaS. Chaque projet est une opportunité de construire
              quelque chose qui fonctionne vraiment.
            </p>

            <h3 class="text-xl font-bold text-gray-900 mt-8">Ma philosophie</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div v-for="value in values" :key="value.title" class="p-4 bg-gray-50 rounded-xl">
                <div class="text-2xl mb-2">{{ value.emoji }}</div>
                <h4 class="font-semibold text-gray-900 mb-1">{{ value.title }}</h4>
                <p class="text-sm text-gray-500">{{ value.description }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-6">
            <div class="card">
              <h3 class="font-semibold text-gray-900 mb-4">En chiffres</h3>
              <dl class="space-y-3">
                <div v-for="stat in stats" :key="stat.label" class="flex justify-between items-center">
                  <dt class="text-gray-500 text-sm">{{ stat.label }}</dt>
                  <dd class="font-bold text-primary-600">{{ stat.value }}</dd>
                </div>
              </dl>
            </div>

            <div class="card">
              <h3 class="font-semibold text-gray-900 mb-4">Me contacter</h3>
              <div class="space-y-3">
                <a href="mailto:contact@zsdevweb.fr" class="flex items-center gap-2 text-sm text-gray-600 hover:text-primary-600">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                  contact@zsdevweb.fr
                </a>
              </div>
              <RouterLink to="/contact" class="btn-primary w-full justify-center mt-4">
                Envoyer un message
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const values = [
  { emoji: '🎯', title: 'Orienté résultats', description: 'Chaque ligne de code doit servir un objectif business concret.' },
  { emoji: '🔍', title: 'Transparent', description: 'Communication claire, délais respectés, pas de mauvaises surprises.' },
  { emoji: '⚡', title: 'Rapide', description: 'Des projets livrés dans les délais, sans sacrifier la qualité.' },
  { emoji: '🔧', title: 'Maintenable', description: 'Code propre, documenté, que vous pourrez faire évoluer.' },
]

const stats = [
  { label: 'Projets livrés', value: '30+' },
  { label: 'Années d\'expérience', value: '5' },
  { label: 'Clients satisfaits', value: '100%' },
  { label: 'Délai moyen', value: '< 6 sem.' },
]

import { useHead } from '@unhead/vue'

useHead({
  title: 'À propos de Zsdevweb — Développeur Web TPE/PME à Mouvaux',
  meta: [
    { name: 'description', content: 'Développeur freelance basé à Mouvaux. Construisons des applications web modernes et performantes. Découvrez mon parcours et mon approche centrée sur les résultats.' },
    { property: 'og:title', content: 'À propos de Zsdevweb' },
    { property: 'og:description', content: 'Développeur web freelance à Mouvaux. Découvrez ma philosophie.' }
  ]
})
</script>
