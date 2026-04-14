<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">

    <!-- En-tête -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Tableau de bord</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Vue d'ensemble de l'activité</p>
        </div>
        <button @click="refresh" class="btn-ghost text-sm flex items-center gap-2" :disabled="loading">
          <svg class="w-4 h-4" :class="{ 'animate-spin': loading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Actualiser
        </button>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

      <!-- Erreur -->
      <div v-if="error" class="card border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-sm" role="alert">
        {{ error }}
      </div>

      <!-- KPI cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="kpi in kpiCards" :key="kpi.label" class="card">
          <!-- Skeleton -->
          <template v-if="loading">
            <div class="h-3 w-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-3"></div>
            <div class="h-7 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
          </template>
          <template v-else>
            <p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">{{ kpi.label }}</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ kpi.value }}</p>
            <p v-if="kpi.sub" class="text-xs text-gray-400 mt-1">{{ kpi.sub }}</p>
          </template>
        </div>
      </div>

      <!-- Devis récents -->
      <div class="card">
        <h2 class="font-bold text-gray-900 dark:text-white mb-4">Devis récents</h2>

        <!-- Skeleton table -->
        <template v-if="loading">
          <div v-for="i in 5" :key="i" class="flex gap-4 py-3 border-b border-gray-100 dark:border-gray-700 last:border-0">
            <div class="h-4 w-28 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
            <div class="h-4 flex-1 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
            <div class="h-4 w-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
            <div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
          </div>
        </template>

        <template v-else-if="stats?.recent_quotes?.length">
          <div class="overflow-x-auto -mx-5">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-left text-xs font-medium text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-700">
                  <th class="pb-3 pl-5 pr-4">Numéro</th>
                  <th class="pb-3 pr-4">Client</th>
                  <th class="pb-3 pr-4 text-right">Montant TTC</th>
                  <th class="pb-3 pr-4">Statut</th>
                  <th class="pb-3 pr-5">Date</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="q in stats.recent_quotes"
                  :key="q.uuid"
                  class="border-b border-gray-50 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
                  @click="$router.push(`/devis/${q.uuid}`)"
                >
                  <td class="py-3 pl-5 pr-4 font-mono text-xs text-gray-600 dark:text-gray-300">{{ q.quote_number }}</td>
                  <td class="py-3 pr-4">
                    <p class="font-medium text-gray-900 dark:text-white">{{ q.client_name }}</p>
                    <p v-if="q.client_company" class="text-xs text-gray-400">{{ q.client_company }}</p>
                  </td>
                  <td class="py-3 pr-4 text-right font-semibold text-gray-900 dark:text-white whitespace-nowrap">
                    {{ formatPrice(q.total_ttc) }}
                  </td>
                  <td class="py-3 pr-4">
                    <StatusBadge :status="q.status" :label="q.status_display" :color-map="QUOTE_STATUS_COLORS" />
                  </td>
                  <td class="py-3 pr-5 text-gray-400 whitespace-nowrap">{{ formatDate(q.created_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>

        <p v-else class="text-sm text-gray-400 py-4 text-center">Aucun devis pour le moment.</p>
      </div>

      <!-- Projets actifs -->
      <div class="card">
        <h2 class="font-bold text-gray-900 dark:text-white mb-4">Projets actifs</h2>

        <!-- Skeleton -->
        <template v-if="loading">
          <div v-for="i in 3" :key="i" class="flex gap-4 py-3 border-b border-gray-100 dark:border-gray-700 last:border-0">
            <div class="h-4 flex-1 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
            <div class="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
            <div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
          </div>
        </template>

        <template v-else-if="stats?.active_projects?.length">
          <div class="space-y-3">
            <RouterLink
              v-for="p in stats.active_projects"
              :key="p.uuid"
              :to="`/espace-client/projets/${p.uuid}`"
              class="flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors group"
            >
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-900 dark:text-white truncate group-hover:text-primary-600 transition-colors">
                  {{ p.title }}
                </p>
                <p class="text-xs text-gray-400 truncate">{{ p.client_email }}</p>
              </div>

              <StatusBadge :status="p.status" :label="p.status_display" :color-map="PROJECT_STATUS_COLORS" />

              <div class="w-32 shrink-0">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-xs text-gray-400">{{ p.progress_percent }}%</span>
                </div>
                <div class="h-1.5 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    class="h-full bg-primary-500 rounded-full transition-all duration-500"
                    :style="{ width: `${p.progress_percent}%` }"
                  ></div>
                </div>
              </div>
            </RouterLink>
          </div>
        </template>

        <p v-else class="text-sm text-gray-400 py-4 text-center">Aucun projet actif.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import { dashboardApi } from '@/api/dashboard.js'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { QUOTE_STATUS_COLORS, PROJECT_STATUS_COLORS } from '@/components/ui/statusColors.js'

useHead({
  title: 'Tableau de bord | Zsdevweb',
  meta: [{ name: 'robots', content: 'noindex, nofollow' }],
})

const stats   = ref(null)
const loading = ref(false)
const error   = ref('')

const kpiCards = computed(() => {
  const k = stats.value?.kpis
  return [
    {
      label: 'CA total accepté',
      value: k ? formatPrice(k.revenue_total) : '—',
      sub:   k ? `${formatPrice(k.revenue_this_month)} ce mois` : null,
    },
    {
      label: 'Devis ce mois',
      value: k?.quotes_this_month ?? '—',
      sub:   k ? `${k.quotes_total} au total` : null,
    },
    {
      label: 'Taux de conversion',
      value: k ? `${k.conversion_rate} %` : '—',
      sub:   k ? `${k.quotes_accepted} acceptés` : null,
    },
    {
      label: 'Projets actifs',
      value: k?.projects_active ?? '—',
      sub:   k ? `${k.quotes_pending} devis en attente` : null,
    },
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

function formatPrice(value) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(Number(value))
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

onMounted(refresh)
</script>
