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
                >
                  <span class="text-sm">{{ updateIcon(update.update_type) }}</span>
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
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" :class="docColor(doc.doc_type)">
                <span class="text-lg">{{ docIcon(doc.doc_type) }}</span>
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
    <div v-else class="text-center py-24 text-gray-400">Projet introuvable.</div>

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

function updateIcon(type) {
  return { progress: '📊', milestone: '🏁', delivery: '🚀', feedback: '💬', info: 'ℹ️' }[type] ?? '📌'
}

function updateIconClass(type) {
  return {
    progress:  'bg-blue-50',
    milestone: 'bg-green-50',
    delivery:  'bg-purple-50',
    feedback:  'bg-amber-50',
    info:      'bg-gray-50',
  }[type] ?? 'bg-gray-50'
}

function docIcon(type) {
  return { contract: '📄', mockup: '🎨', deliverable: '📦', invoice: '🧾', other: '📎' }[type] ?? '📎'
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
