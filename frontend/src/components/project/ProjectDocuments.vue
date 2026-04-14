<template>
  <div>
    <h2 class="font-bold text-gray-900 mb-4">Documents</h2>
    <div class="grid gap-3 sm:grid-cols-2">
      <a
        v-for="doc in documents"
        :key="doc.id"
        :href="doc.file_url"
        target="_blank"
        class="card flex items-center gap-4 hover:shadow-md transition-all hover:-translate-y-0.5 cursor-pointer"
      >
        <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" :class="docColor(doc.doc_type)" aria-hidden="true">
          <component :is="docIconSvg(doc.doc_type)" class="w-5 h-5" />
        </div>
        <div class="min-w-0">
          <div class="font-semibold text-gray-900 truncate">{{ doc.name }}</div>
          <div class="text-xs text-gray-500">{{ docTypeLabel(doc.doc_type) }} · {{ formatDate(doc.uploaded_at) }}</div>
        </div>
        <svg class="w-4 h-4 text-gray-300 ml-auto flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
      </a>
    </div>
  </div>
</template>

<script setup>
import { useProjectIcons } from '@/composables/useProjectIcons.js'

defineProps({
  documents: { type: Array, required: true },
})

const { docIconSvg, docColor, docTypeLabel } = useProjectIcons()

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
