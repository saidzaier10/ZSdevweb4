<template>
  <div class="card">
    <h2 class="font-bold text-gray-900 dark:text-white mb-4">Demandes d'audit</h2>

    <template v-if="loading">
      <div v-for="i in 4" :key="i" class="flex gap-4 py-3 border-b border-gray-100 dark:border-gray-700 last:border-0">
        <div class="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 flex-1 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </div>
    </template>

    <template v-else-if="audits.length">
      <div class="overflow-x-auto -mx-5">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-xs font-medium text-gray-500 uppercase tracking-wide border-b border-gray-100 dark:border-gray-700">
              <th class="pb-3 pl-5 pr-4">Contact</th>
              <th class="pb-3 pr-4">Site</th>
              <th class="pb-3 pr-4">Objectifs</th>
              <th class="pb-3 pr-4">Statut</th>
              <th class="pb-3 pr-5">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="a in audits"
              :key="a.id"
              class="border-b border-gray-50 dark:border-gray-800 last:border-0"
            >
              <td class="py-3 pl-5 pr-4">
                <p class="font-medium text-gray-900 dark:text-white">{{ a.name }}</p>
                <a :href="`mailto:${a.email}`" class="text-xs text-primary-600 hover:underline">{{ a.email }}</a>
                <p v-if="a.company" class="text-xs text-gray-500 dark:text-gray-400">{{ a.company }}</p>
              </td>
              <td class="py-3 pr-4">
                <a :href="a.site_url" target="_blank" rel="noopener noreferrer"
                   class="text-xs text-primary-600 hover:underline break-all">
                  {{ a.site_url }}
                </a>
              </td>
              <td class="py-3 pr-4">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="obj in a.objectives"
                    :key="obj"
                    class="inline-block px-1.5 py-0.5 text-xs rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
                  >{{ OBJECTIVE_LABELS[obj] ?? obj }}</span>
                  <span v-if="!a.objectives?.length" class="text-xs text-gray-400">—</span>
                </div>
              </td>
              <td class="py-3 pr-4">
                <span
                  :class="a.is_processed
                    ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                    : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'"
                  class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap"
                >
                  <span v-if="a.is_processed">Traité</span>
                  <span v-else>En attente</span>
                </span>
              </td>
              <td class="py-3 pr-5 text-gray-500 dark:text-gray-400 whitespace-nowrap text-xs">
                {{ formatDateShort(a.created_at) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <p v-else class="text-sm text-gray-500 py-4 text-center">Aucune demande d'audit pour le moment.</p>
  </div>
</template>

<script setup>
import { useFormatters } from '@/composables/useFormatters.js'

defineProps({
  loading: { type: Boolean, default: false },
  audits:  { type: Array,   default: () => [] },
})

const OBJECTIVE_LABELS = {
  more_traffic: 'Trafic',
  more_leads:   'Leads',
  better_ux:    'UX',
  faster_site:  'Vitesse',
  seo:          'SEO',
  mobile:       'Mobile',
  other:        'Autre',
}

const { formatDateShort } = useFormatters()
</script>
