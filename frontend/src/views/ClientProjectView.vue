<template>
  <div class="min-h-screen bg-gray-50">

    <div v-if="loading" class="flex justify-center py-24">
      <LoadingSpinner />
    </div>

    <template v-else-if="project">
      <!-- En-tête -->
      <div class="bg-white border-b border-gray-200">
        <div class="max-w-4xl mx-auto px-4 py-6">
          <div class="flex items-center gap-2 text-sm text-gray-400 mb-3">
            <RouterLink to="/espace-client" class="hover:text-primary-600">Espace client</RouterLink>
            <span>/</span>
            <span class="text-gray-600">{{ project.title }}</span>
          </div>
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ project.title }}</h1>
              <p v-if="project.description" class="text-gray-500 mt-1">{{ project.description }}</p>
            </div>
            <div class="flex items-center gap-3">
              <a v-if="project.site_url" :href="project.site_url" target="_blank" class="btn-secondary text-sm inline-flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                Voir le site
              </a>
              <RouterLink v-if="project.quote_uuid" :to="`/devis/${project.quote_uuid}`" class="text-sm text-primary-600 hover:underline">
                Devis {{ project.quote_number }}
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <div class="max-w-4xl mx-auto px-4 py-8 space-y-8">
        <ProjectProgress
          :status="project.status"
          :progress="project.progress_percent"
          :started-at="project.started_at"
          :estimated-delivery="project.estimated_delivery"
          :delivered-at="project.delivered_at"
        />
        <ProjectTimeline v-if="project.updates?.length" :updates="project.updates" />
        <ProjectDocuments v-if="project.documents?.length" :documents="project.documents" />

        <!-- Contact -->
        <div class="card bg-primary-50 border-primary-100">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-primary-900">Une question sur votre projet ?</h3>
              <p class="text-sm text-primary-700 mt-0.5 mb-3">Je réponds sous 24h en jours ouvrés.</p>
              <RouterLink to="/contact" class="btn-primary text-sm inline-flex">Nous contacter</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Erreur -->
    <div v-else class="max-w-md mx-auto px-4 py-24 text-center">
      <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      </div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Projet introuvable</h2>
      <p class="text-gray-500 mb-6">Ce projet n'existe pas ou vous n'y avez pas accès.</p>
      <RouterLink to="/espace-client" class="btn-primary inline-flex">Retour à l'espace client</RouterLink>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { clientApi } from '@/api/client.js'
import { useHead } from '@unhead/vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import ProjectProgress from '@/components/project/ProjectProgress.vue'
import ProjectTimeline from '@/components/project/ProjectTimeline.vue'
import ProjectDocuments from '@/components/project/ProjectDocuments.vue'

useHead({
  title: 'Mon projet | Zsdevweb',
  meta: [{ name: 'robots', content: 'noindex, nofollow' }],
})

const route = useRoute()
const project = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await clientApi.getProject(route.params.uuid)
    project.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>
