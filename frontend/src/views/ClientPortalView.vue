<template>
  <div class="min-h-screen bg-gray-50">

    <!-- En-tête -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-5xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold text-gray-900">Espace client</h1>
        <p class="text-gray-500 mt-1">Suivez l'avancement de vos projets en temps réel.</p>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 py-8">

      <!-- Skeleton loading -->
      <div v-if="loading" class="grid gap-4 md:grid-cols-2" aria-label="Chargement des projets" aria-busy="true">
        <div v-for="i in 4" :key="i" class="card space-y-4">
          <div class="flex items-start justify-between">
            <div class="space-y-2 flex-1">
              <SkeletonLoader height="h-5" width="w-40" />
              <SkeletonLoader height="h-3" width="w-28" />
            </div>
            <SkeletonLoader height="h-5" width="w-20" rounded="rounded-full" />
          </div>
          <div class="space-y-1.5">
            <div class="flex justify-between">
              <SkeletonLoader height="h-3" width="w-20" />
              <SkeletonLoader height="h-3" width="w-10" />
            </div>
            <SkeletonLoader height="h-2" rounded="rounded-full" />
          </div>
          <SkeletonLoader height="h-4" width="w-48" />
        </div>
      </div>

      <!-- Non connecté -->
      <div v-else-if="!authStore.isAuthenticated" class="card text-center py-16 max-w-md mx-auto">
        <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Connexion requise</h2>
        <p class="text-gray-500 mb-6">Connectez-vous pour accéder à vos projets.</p>
        <RouterLink to="/connexion" class="btn-primary inline-flex">Se connecter</RouterLink>
      </div>

      <!-- Aucun projet -->
      <div v-else-if="projects.length === 0" class="card text-center py-16 max-w-md mx-auto">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Aucun projet en cours</h2>
        <p class="text-gray-500 mb-6">Démarrez votre premier projet en demandant un devis.</p>
        <RouterLink to="/devis" class="btn-primary inline-flex">Demander un devis</RouterLink>
      </div>

      <!-- Filtres + recherche -->
      <div v-else>
        <div class="flex flex-col sm:flex-row gap-3 mb-6">
          <!-- Recherche -->
          <div class="relative flex-1">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="search"
              type="search"
              placeholder="Rechercher un projet..."
              class="input-field pl-9 py-2.5 text-sm"
              aria-label="Rechercher un projet"
            />
          </div>
          <!-- Filtre statut -->
          <select v-model="filterStatus" class="input-field py-2.5 text-sm sm:w-48" aria-label="Filtrer par statut">
            <option value="">Tous les statuts</option>
            <option v-for="(label, key) in STATUS_LABELS" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>

        <!-- Résultat filtré vide -->
        <div v-if="filteredProjects.length === 0" class="text-center py-12 text-gray-400 dark:text-gray-600">
          <svg class="w-10 h-10 mx-auto mb-3 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Aucun projet ne correspond à votre recherche.
          <button @click="search = ''; filterStatus = ''" class="block mx-auto mt-2 text-sm text-primary-600 hover:underline">
            Effacer les filtres
          </button>
        </div>

        <div class="grid gap-4 md:grid-cols-2">
          <div
            v-for="project in filteredProjects"
            :key="project.uuid"
            @click="$router.push(`/espace-client/projets/${project.uuid}`)"
            class="card cursor-pointer hover:shadow-md transition-all hover:-translate-y-0.5"
          >
            <!-- Statut -->
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="font-bold text-gray-900 text-lg">{{ project.title }}</h3>
                <p class="text-sm text-gray-400 mt-0.5">Mis à jour {{ formatDate(project.updated_at) }}</p>
              </div>
              <StatusBadge :status="project.status" :label="project.status_display" :color-map="PROJECT_STATUS_COLORS" />
            </div>

            <!-- Barre de progression -->
            <div class="mb-3">
              <div class="flex justify-between text-xs text-gray-500 mb-1.5">
                <span>Progression</span>
                <span class="font-semibold">{{ project.progress_percent }}%</span>
              </div>
              <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  class="h-2 rounded-full transition-all duration-500"
                  :class="progressColor(project.progress_percent)"
                  :style="{ width: `${project.progress_percent}%` }"
                />
              </div>
            </div>

            <!-- Livraison estimée -->
            <div v-if="project.estimated_delivery" class="flex items-center gap-2 text-sm text-gray-500">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Livraison prévue le <strong class="text-gray-700">{{ formatDate(project.estimated_delivery) }}</strong>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { clientApi } from '@/api/client.js'
import { useHead } from '@unhead/vue'
import StatusBadge, { PROJECT_STATUS_COLORS } from '@/components/ui/StatusBadge.vue'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'

useHead({
  title: 'Espace client | Zsdevweb',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})

const authStore = useAuthStore()
const projects = ref([])
const loading = ref(true)
const search = ref('')
const filterStatus = ref('')

const STATUS_LABELS = {
  briefing:    'Briefing',
  design:      'Design',
  development: 'Développement',
  review:      'Révision',
  delivered:   'Livré',
  maintenance: 'Maintenance',
}

const filteredProjects = computed(() => {
  return projects.value.filter(p => {
    const matchSearch = !search.value || p.title.toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = !filterStatus.value || p.status === filterStatus.value
    return matchSearch && matchStatus
  })
})

onMounted(async () => {
  if (!authStore.isAuthenticated) { loading.value = false; return }
  try {
    const { data } = await clientApi.getProjects()
    projects.value = data.results ?? data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

function progressColor(pct) {
  if (pct >= 80) return 'bg-green-500'
  if (pct >= 40) return 'bg-blue-500'
  return 'bg-amber-400'
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
