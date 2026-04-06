<template>
  <section class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="section-title">Mes réalisations</h2>
        <p class="section-subtitle mx-auto">Des projets concrets, des résultats mesurables.</p>
      </div>

      <div v-if="loading" class="flex justify-center py-12">
        <LoadingSpinner />
      </div>

      <div v-else-if="projects.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="project in projects" :key="project.id" class="card group hover:shadow-xl transition-shadow">
          <div class="bg-gray-100 rounded-xl aspect-video mb-4 flex items-center justify-center overflow-hidden">
            <img v-if="project.image" :src="project.image" :alt="project.title" class="w-full h-full object-cover" />
            <div v-else class="text-gray-400 text-center p-4">
              <svg class="w-8 h-8 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              {{ project.title }}
            </div>
          </div>
          <h3 class="font-bold text-gray-900 mb-1">{{ project.title }}</h3>
          <p class="text-gray-500 text-sm mb-3">{{ project.tagline }}</p>
          <div class="flex flex-wrap gap-1">
            <span v-for="tech in (project.tech_stack || []).slice(0, 3)" :key="tech" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-md">
              {{ tech }}
            </span>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-16">
        <p class="text-gray-400">Portfolio en cours de mise à jour...</p>
      </div>

      <div class="text-center mt-10">
        <RouterLink to="/portfolio" class="btn-secondary">
          Voir tout le portfolio →
        </RouterLink>
      </div>
    </div>
  </section>
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
  } catch {
    projects.value = []
  } finally {
    loading.value = false
  }
})
</script>
