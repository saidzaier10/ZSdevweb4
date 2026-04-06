<template>
  <div>
    <section class="bg-gradient-to-br from-gray-900 to-primary-950 text-white py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Portfolio</h1>
        <p class="text-gray-300 text-lg">Des projets concrets, des résultats mesurables.</p>
      </div>
    </section>

    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div v-if="loading" class="flex justify-center py-20">
          <LoadingSpinner size="lg" />
        </div>

        <div v-else-if="projects.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="project in projects" :key="project.id" class="card group hover:shadow-xl transition-all duration-300">
            <div class="bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl aspect-video mb-4 overflow-hidden">
              <img v-if="project.image" :src="project.image" :alt="project.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
              <div v-else class="w-full h-full flex items-center justify-center">
                <span class="text-4xl">💻</span>
              </div>
            </div>
            <h3 class="font-bold text-gray-900 text-lg mb-1">{{ project.title }}</h3>
            <p class="text-gray-500 text-sm mb-3">{{ project.tagline }}</p>
            <div class="flex flex-wrap gap-1 mb-4">
              <span v-for="tech in (project.tech_stack || []).slice(0, 4)" :key="tech"
                class="text-xs bg-primary-50 text-primary-700 px-2 py-0.5 rounded-md font-medium">
                {{ tech }}
              </span>
            </div>
            <div class="flex gap-3">
              <a v-if="project.url" :href="project.url" target="_blank" rel="noopener" class="text-sm text-primary-600 font-medium hover:underline">
                Voir le site →
              </a>
              <a v-if="project.github_url" :href="project.github_url" target="_blank" rel="noopener" class="text-sm text-gray-500 hover:text-gray-700">
                GitHub
              </a>
            </div>
          </div>
        </div>

        <!-- État vide avec démos -->
        <div v-else class="space-y-8">
          <p class="text-center text-gray-400 mb-8">Portfolio en cours de mise à jour. Voici un aperçu de mes réalisations :</p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="demo in demoProjects" :key="demo.title" class="card">
              <div :class="['rounded-xl aspect-video mb-4 flex items-center justify-center', demo.bg]">
                <span class="text-4xl">{{ demo.emoji }}</span>
              </div>
              <h3 class="font-bold text-gray-900 mb-1">{{ demo.title }}</h3>
              <p class="text-gray-500 text-sm mb-3">{{ demo.description }}</p>
              <div class="flex flex-wrap gap-1">
                <span v-for="tech in demo.stack" :key="tech" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">{{ tech }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-primary-600 text-white text-center px-4">
      <h2 class="text-2xl font-bold mb-4">Votre projet sera ici demain</h2>
      <RouterLink to="/devis" class="bg-white text-primary-600 font-semibold px-8 py-4 rounded-xl hover:bg-gray-50 transition-colors inline-flex mt-2">
        Démarrer mon projet →
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { portfolioApi } from '@/api/portfolio.js'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const projects = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await portfolioApi.getProjects()
    projects.value = data.results || data
  } catch { projects.value = [] }
  finally { loading.value = false }
})

const demoProjects = [
  { title: 'Boutique Bio en ligne', description: 'E-commerce Vue.js + Django avec paiement Stripe. +40% de ventes dès le premier mois.', bg: 'bg-green-100', emoji: '🌿', stack: ['Vue.js', 'Django', 'Stripe', 'PostgreSQL'] },
  { title: 'CRM Immobilier', description: 'Application web métier pour agence immobilière. Gestion des biens, clients et rendez-vous.', bg: 'bg-blue-100', emoji: '🏠', stack: ['Vue.js 3', 'Django REST', 'Redis', 'Docker'] },
  { title: 'SaaS RH', description: 'Plateforme de gestion des ressources humaines avec tableaux de bord et automatisations.', bg: 'bg-purple-100', emoji: '👥', stack: ['Nuxt.js', 'Django', 'PostgreSQL', 'Celery'] },
]
</script>
