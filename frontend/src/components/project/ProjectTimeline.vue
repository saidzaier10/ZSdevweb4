<template>
  <div>
    <h2 class="font-bold text-gray-900 mb-4">Journal de bord</h2>
    <div class="relative">
      <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200" />
      <div class="space-y-4">
        <div v-for="update in updates" :key="update.id" class="relative pl-12">
          <div
            class="absolute left-0 w-8 h-8 rounded-full flex items-center justify-center"
            :class="updateIconClass(update.update_type)"
            aria-hidden="true"
          >
            <component :is="updateIconSvg(update.update_type)" class="w-4 h-4" />
          </div>
          <div class="card py-4 px-5">
            <div class="flex items-start justify-between gap-2">
              <h3 class="font-semibold text-gray-900">{{ update.title }}</h3>
              <span class="text-xs text-gray-400 flex-shrink-0">{{ formatDate(update.created_at) }}</span>
            </div>
            <p class="text-sm text-gray-600 mt-1.5 leading-relaxed">{{ update.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProjectIcons } from '@/composables/useProjectIcons.js'

defineProps({
  updates: { type: Array, required: true },
})

const { updateIconSvg, updateIconClass } = useProjectIcons()

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
