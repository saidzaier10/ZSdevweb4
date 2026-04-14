<template>
  <div
    class="card cursor-pointer hover:shadow-md transition-all hover:-translate-y-0.5"
    @click="$router.push(`/espace-client/projets/${project.uuid}`)"
  >
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="font-bold text-gray-900 text-lg">{{ project.title }}</h3>
        <p class="text-sm text-gray-400 mt-0.5">Mis à jour {{ formatDate(project.updated_at) }}</p>
      </div>
      <StatusBadge :status="project.status" :label="project.status_display" :color-map="PROJECT_STATUS_COLORS" />
    </div>

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

    <div v-if="project.estimated_delivery" class="flex items-center gap-2 text-sm text-gray-500">
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      Livraison prévue le <strong class="text-gray-700">{{ formatDate(project.estimated_delivery) }}</strong>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { PROJECT_STATUS_COLORS } from '@/components/ui/statusColors.js'
import { useFormatters } from '@/composables/useFormatters.js'

defineProps({
  project: { type: Object, required: true },
})

const { formatDate } = useFormatters()

function progressColor(pct) {
  if (pct >= 80) return 'bg-green-500'
  if (pct >= 40) return 'bg-blue-500'
  return 'bg-amber-400'
}
</script>
