<template>
  <div class="card">
    <h2 class="font-bold text-gray-900 dark:text-white mb-4">Devis récents</h2>

    <template v-if="loading">
      <div v-for="i in 5" :key="i" class="flex gap-4 py-3 border-b border-gray-100 dark:border-gray-700 last:border-0">
        <div class="h-4 w-28 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 flex-1 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 w-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </div>
    </template>

    <template v-else-if="quotes.length">
      <div class="overflow-x-auto -mx-5">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-xs font-medium text-gray-500 uppercase tracking-wide border-b border-gray-100 dark:border-gray-700">
              <th class="pb-3 pl-5 pr-4">Numéro</th>
              <th class="pb-3 pr-4">Client</th>
              <th class="pb-3 pr-4 text-right">Montant TTC</th>
              <th class="pb-3 pr-4">Statut</th>
              <th class="pb-3 pr-5">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="q in quotes"
              :key="q.uuid"
              class="border-b border-gray-50 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
              @click="$router.push(`/devis/${q.uuid}`)"
            >
              <td class="py-3 pl-5 pr-4 font-mono text-xs text-gray-600 dark:text-gray-300">{{ q.quote_number }}</td>
              <td class="py-3 pr-4">
                <p class="font-medium text-gray-900 dark:text-white">{{ q.client_name }}</p>
                <p v-if="q.client_company" class="text-xs text-gray-500">{{ q.client_company }}</p>
              </td>
              <td class="py-3 pr-4 text-right font-semibold text-gray-900 dark:text-white whitespace-nowrap">
                {{ formatPrice(q.total_ttc) }}
              </td>
              <td class="py-3 pr-4">
                <StatusBadge :status="q.status" :label="q.status_display" :color-map="QUOTE_STATUS_COLORS" />
              </td>
              <td class="py-3 pr-5 text-gray-500 whitespace-nowrap">{{ formatDateShort(q.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <p v-else class="text-sm text-gray-500 py-4 text-center">Aucun devis pour le moment.</p>
  </div>
</template>

<script setup>
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { QUOTE_STATUS_COLORS } from '@/components/ui/statusColors.js'
import { useFormatters } from '@/composables/useFormatters.js'

defineProps({
  loading: { type: Boolean, default: false },
  quotes:  { type: Array,   default: () => [] },
})

const { formatPrice, formatDateShort } = useFormatters()
</script>
