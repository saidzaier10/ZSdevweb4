<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-24">
      <LoadingSpinner />
    </div>

    <template v-else-if="project">
      <!-- En-tête projet -->
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
              <a
                v-if="project.site_url"
                :href="project.site_url"
                target="_blank"
                class="btn-secondary text-sm inline-flex items-center gap-1.5"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                Voir le site
              </a>
              <RouterLink
                v-if="project.quote_uuid"
                :to="`/devis/${project.quote_uuid}`"
                class="text-sm text-primary-600 hover:underline"
              >
                Devis {{ project.quote_number }}
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <div class="max-w-4xl mx-auto px-4 py-8 space-y-8">

        <!-- Progression globale -->
        <div class="card">
          <h2 class="font-bold text-gray-900 mb-5">Avancement du projet</h2>

          <!-- Étapes -->
          <div class="flex items-center gap-0 mb-6 overflow-x-auto pb-2">
            <template v-for="(step, i) in steps" :key="step.key">
              <div class="flex flex-col items-center flex-shrink-0 min-w-[80px]">
                <div
                  class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all"
                  :class="stepClass(step.key)"
                >
                  <svg v-if="isStepDone(step.key)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                  <span v-else>{{ i + 1 }}</span>
                </div>
                <span class="text-xs text-center mt-1.5 text-gray-500 leading-tight">{{ step.label }}</span>
              </div>
              <div
                v-if="i < steps.length - 1"
                class="flex-1 h-0.5 min-w-[20px] transition-all"
                :class="isStepDone(steps[i + 1].key) || project.status === steps[i + 1].key ? 'bg-primary-500' : 'bg-gray-200'"
              />
            </template>
          </div>

          <!-- Barre % -->
          <div class="flex justify-between text-sm text-gray-500 mb-2">
            <span>Progression globale</span>
            <span class="font-bold text-gray-900">{{ project.progress_percent }}%</span>
          </div>
          <div class="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-3 bg-gradient-to-r from-primary-500 to-primary-400 rounded-full transition-all duration-700"
              :style="{ width: `${project.progress_percent}%` }"
            />
          </div>

          <!-- Dates -->
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-100">
            <div v-if="project.started_at">
              <div class="text-xs text-gray-400 uppercase tracking-wide mb-1">Démarrage</div>
              <div class="font-semibold text-gray-900">{{ formatDate(project.started_at) }}</div>
            </div>
            <div v-if="project.estimated_delivery">
              <div class="text-xs text-gray-400 uppercase tracking-wide mb-1">Livraison prévue</div>
              <div class="font-semibold text-gray-900">{{ formatDate(project.estimated_delivery) }}</div>
            </div>
            <div v-if="project.delivered_at">
              <div class="text-xs text-gray-400 uppercase tracking-wide mb-1">Livré le</div>
              <div class="font-semibold text-green-600">{{ formatDate(project.delivered_at) }}</div>
            </div>
          </div>
        </div>

        <!-- Timeline des mises à jour -->
        <div v-if="project.updates?.length">
          <h2 class="font-bold text-gray-900 mb-4">Journal de bord</h2>
          <div class="relative">
            <!-- Ligne verticale -->
            <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200" />

            <div class="space-y-4">
              <div
                v-for="update in project.updates"
                :key="update.id"
                class="relative pl-12"
              >
                <!-- Icône -->
                <div
                  class="absolute left-0 w-8 h-8 rounded-full flex items-center justify-center"
                  :class="updateIconClass(update.update_type)"
                  aria-hidden="true"
                >
                  <component :is="updateIconSvg(update.update_type)" class="w-4 h-4" />
                </div>
                <!-- Contenu -->
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

        <!-- Documents -->
        <div v-if="project.documents?.length">
          <h2 class="font-bold text-gray-900 mb-4">Documents</h2>
          <div class="grid gap-3 sm:grid-cols-2">
            <a
              v-for="doc in project.documents"
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
                <div class="text-xs text-gray-400">{{ docTypeLabel(doc.doc_type) }} · {{ formatDate(doc.uploaded_at) }}</div>
              </div>
              <svg class="w-4 h-4 text-gray-300 ml-auto flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </a>
          </div>
        </div>

        <!-- Contact -->
        <div class="card bg-primary-50 border-primary-100">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { clientApi } from '@/api/client.js'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const route = useRoute()
const project = ref(null)
const loading = ref(true)

const steps = [
  { key: 'briefing',    label: 'Briefing' },
  { key: 'design',      label: 'Design' },
  { key: 'development', label: 'Dév.' },
  { key: 'review',      label: 'Révision' },
  { key: 'delivered',   label: 'Livré' },
]

const stepOrder = steps.map(s => s.key)

function isStepDone(key) {
  if (!project.value) return false
  const current = stepOrder.indexOf(project.value.status)
  const target = stepOrder.indexOf(key)
  return current > target
}

function stepClass(key) {
  if (!project.value) return 'bg-gray-100 text-gray-400'
  if (project.value.status === key) return 'bg-primary-600 text-white ring-4 ring-primary-100'
  if (isStepDone(key)) return 'bg-primary-500 text-white'
  return 'bg-gray-100 text-gray-400'
}

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

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

// SVG icons pour les types de mises à jour (remplace les emojis)
const UPDATE_ICONS = {
  progress: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-blue-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>`,
  },
  milestone: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-green-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3l14 9-14 9V3z" /></svg>`,
  },
  delivery: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-purple-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`,
  },
  feedback: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-amber-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>`,
  },
  info: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-500"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`,
  },
  default: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-400"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>`,
  },
}

const DOC_ICONS = {
  contract: { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-blue-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>` },
  mockup: { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-purple-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>` },
  deliverable: { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-green-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>` },
  invoice: { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-amber-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2zM10 8.5a.5.5 0 11-1 0 .5.5 0 011 0zm5 5a.5.5 0 11-1 0 .5.5 0 011 0z" /></svg>` },
  other: { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-500"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>` },
}

function updateIconSvg(type) { return UPDATE_ICONS[type] ?? UPDATE_ICONS.default }
function docIconSvg(type) { return DOC_ICONS[type] ?? DOC_ICONS.other }

function updateIconClass(type) {
  return {
    progress:  'bg-blue-50',
    milestone: 'bg-green-50',
    delivery:  'bg-purple-50',
    feedback:  'bg-amber-50',
    info:      'bg-gray-50',
  }[type] ?? 'bg-gray-50'
}

function docColor(type) {
  return {
    contract:    'bg-blue-50',
    mockup:      'bg-purple-50',
    deliverable: 'bg-green-50',
    invoice:     'bg-amber-50',
    other:       'bg-gray-50',
  }[type] ?? 'bg-gray-50'
}

function docTypeLabel(type) {
  return { contract: 'Contrat', mockup: 'Maquette', deliverable: 'Livrable', invoice: 'Facture', other: 'Document' }[type] ?? 'Document'
}
</script>
