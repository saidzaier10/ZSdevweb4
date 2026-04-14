<template>
  <div class="card">
    <h2 class="font-bold text-gray-900 dark:text-white mb-4">Projets actifs</h2>

    <template v-if="loading">
      <div v-for="i in 3" :key="i" class="flex gap-4 py-3 border-b border-gray-100 dark:border-gray-700 last:border-0">
        <div class="h-4 flex-1 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </div>
    </template>

    <template v-else-if="projects.length">
      <div class="space-y-3">
        <RouterLink
          v-for="p in projects"
          :key="p.uuid"
          :to="`/espace-client/projets/${p.uuid}`"
          class="flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors group"
        >
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-900 dark:text-white truncate group-hover:text-primary-600 transition-colors">
              {{ p.title }}
            </p>
            <p class="text-xs text-gray-500 truncate">{{ p.client_email }}</p>
          </div>
          <StatusBadge :status="p.status" :label="p.status_display" :color-map="PROJECT_STATUS_COLORS" />
          <div class="w-32 shrink-0">
            <div class="flex justify-between mb-1">
              <span class="text-xs text-gray-500">{{ p.progress_percent }}%</span>
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

    <p v-else class="text-sm text-gray-500 py-4 text-center">Aucun projet actif.</p>
  </div>
</template>

<script setup>
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { PROJECT_STATUS_COLORS } from '@/components/ui/statusColors.js'

defineProps({
  loading:  { type: Boolean, default: false },
  projects: { type: Array,   default: () => [] },
})
</script>
