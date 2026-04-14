<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">

    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Tableau de bord</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Vue d'ensemble de l'activité</p>
        </div>
        <button @click="refresh" class="btn-ghost text-sm flex items-center gap-2" :disabled="loading">
          <svg class="w-4 h-4" :class="{ 'animate-spin': loading }" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Actualiser
        </button>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div v-if="error" class="card border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-sm" role="alert">
        {{ error }}
      </div>
      <DashboardKpiCards :loading="loading" :kpi-cards="kpiCards" />
      <DashboardQuotesTable :loading="loading" :quotes="stats?.recent_quotes ?? []" />
      <DashboardProjectsList :loading="loading" :projects="stats?.active_projects ?? []" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import { dashboardApi } from '@/api/dashboard.js'
import { useFormatters } from '@/composables/useFormatters.js'
import DashboardKpiCards from '@/components/dashboard/DashboardKpiCards.vue'
import DashboardQuotesTable from '@/components/dashboard/DashboardQuotesTable.vue'
import DashboardProjectsList from '@/components/dashboard/DashboardProjectsList.vue'

useHead({
  title: 'Tableau de bord | Zsdevweb',
  meta: [{ name: 'robots', content: 'noindex, nofollow' }],
})

const { formatPrice } = useFormatters()
const stats   = ref(null)
const loading = ref(false)
const error   = ref('')

const kpiCards = computed(() => {
  const k = stats.value?.kpis
  return [
    { label: 'CA total accepté',   value: k ? formatPrice(k.revenue_total)    : '—', sub: k ? `${formatPrice(k.revenue_this_month)} ce mois` : null },
    { label: 'Devis ce mois',      value: k?.quotes_this_month ?? '—',               sub: k ? `${k.quotes_total} au total` : null },
    { label: 'Taux de conversion', value: k ? `${k.conversion_rate} %`         : '—', sub: k ? `${k.quotes_accepted} acceptés` : null },
    { label: 'Projets actifs',     value: k?.projects_active ?? '—',                 sub: k ? `${k.quotes_pending} devis en attente` : null },
  ]
})

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await dashboardApi.getStats()
    stats.value = data
  } catch {
    error.value = 'Impossible de charger les données. Vérifiez votre connexion.'
  } finally {
    loading.value = false
  }
}

onMounted(refresh)
</script>
