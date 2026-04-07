<template>
  <div class="min-h-screen bg-gray-50 py-16 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-3">Estimez votre projet en 30 secondes</h1>
        <p class="text-gray-500 text-lg">Obtenez une fourchette de prix immédiate, sans inscription.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Sélecteur -->
        <div class="card space-y-6">
          <div v-if="catalogStore.loading" class="flex justify-center py-8">
            <LoadingSpinner />
          </div>
          <template v-else>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">Type de projet</label>
              <div class="space-y-4">
                <div v-for="cat in catalogStore.categories" :key="cat.id">
                  <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">{{ cat.name }}</p>
                  <div class="grid grid-cols-1 gap-2">
                    <button
                      v-for="type in cat.project_types"
                      :key="type.id"
                      @click="selectedTypeId = type.id"
                      :class="[
                        'p-3 text-sm rounded-xl border-2 text-left transition-all',
                        selectedTypeId === type.id
                          ? 'border-primary-500 bg-primary-50 font-semibold text-primary-900'
                          : 'border-gray-200 hover:border-gray-300 text-gray-700'
                      ]"
                    >
                      <span class="block">{{ type.name }}</span>
                      <span class="text-xs text-gray-400">à partir de {{ formatPrice(type.base_price) }}</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="selectedType">
              <label class="block text-sm font-medium text-gray-700 mb-2">Complexité estimée</label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="level in catalogStore.complexityLevels"
                  :key="level.id"
                  @click="selectedComplexityId = level.id"
                  :class="[
                    'p-3 text-sm rounded-xl border-2 text-center transition-all',
                    selectedComplexityId === level.id
                      ? 'border-primary-500 bg-primary-50 font-semibold'
                      : 'border-gray-200 hover:border-gray-300'
                  ]"
                >
                  {{ level.name }}
                </button>
              </div>
            </div>
          </template>
        </div>

        <!-- Résultat -->
        <div>
          <div v-if="estimate" class="card text-center space-y-4 animate-fade-in">
            <h3 class="font-semibold text-gray-700">Estimation de votre projet</h3>

            <div>
              <div class="text-5xl font-bold text-primary-600">{{ formatPrice(estimate.total_ttc) }}</div>
              <div class="text-sm text-gray-400 mt-1">TTC — TVA 20% incluse</div>
            </div>

            <div class="bg-gray-50 rounded-xl p-4 text-sm space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-500">HT</span>
                <span class="font-medium">{{ formatPrice(estimate.subtotal_ht) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">TVA 20%</span>
                <span class="font-medium">{{ formatPrice(estimate.vat) }}</span>
              </div>
              <div class="flex justify-between font-semibold border-t border-gray-200 pt-2">
                <span>Total TTC</span>
                <span class="text-primary-600">{{ formatPrice(estimate.total_ttc) }}</span>
              </div>
            </div>

            <div class="text-sm text-gray-500">
              Délai estimé : <strong>{{ selectedType?.min_days }}–{{ selectedType?.max_days }} jours</strong>
            </div>

            <!-- Plan 3× -->
            <div class="bg-primary-50 rounded-xl p-4 text-sm">
              <p class="font-semibold text-gray-700 mb-2">Paiement en 3 fois</p>
              <div class="space-y-1">
                <div class="flex justify-between text-gray-600">
                  <span>Acompte (30%)</span><span class="font-semibold">{{ formatPrice(estimate.i1) }}</span>
                </div>
                <div class="flex justify-between text-gray-600">
                  <span>Mi-projet (40%)</span><span class="font-semibold">{{ formatPrice(estimate.i2) }}</span>
                </div>
                <div class="flex justify-between text-gray-600">
                  <span>Livraison (30%)</span><span class="font-semibold">{{ formatPrice(estimate.i3) }}</span>
                </div>
              </div>
            </div>

            <RouterLink to="/devis" class="btn-primary w-full justify-center">
              Obtenir un devis précis et gratuit →
            </RouterLink>
            <p class="text-xs text-gray-400">
              Cette estimation est indicative. Le devis final est gratuit et sans engagement.
            </p>
          </div>

          <div v-else class="card text-center py-16">
            <div class="text-gray-300 mb-4">
              <svg class="w-16 h-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 19h16a2 2 0 002-2V7a2 2 0 00-2-2H4a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <p class="text-gray-400">Sélectionnez un type de projet<br>pour voir l'estimation</p>
          </div>
        </div>
      </div>

      <!-- CTA bas -->
      <div class="mt-12 text-center p-8 bg-white rounded-2xl border border-gray-100">
        <p class="text-gray-600 mb-4">Cette estimation vous convient ? Obtenez un devis détaillé et personnalisé.</p>
        <RouterLink to="/devis" class="btn-primary inline-flex">
          Démarrer ma demande de devis →
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCatalogStore } from '@/stores/catalog.js'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { useHead } from '@unhead/vue'

const catalogStore = useCatalogStore()
const selectedTypeId = ref(null)
const selectedComplexityId = ref(null)

onMounted(() => catalogStore.fetchAll())

const selectedType = computed(() => catalogStore.getProjectTypeById(selectedTypeId.value))
const selectedComplexity = computed(() => catalogStore.getComplexityById(selectedComplexityId.value))

const estimate = computed(() => {
  if (!selectedType.value) return null
  const base = parseFloat(selectedType.value.base_price)
  const mult = selectedComplexity.value ? parseFloat(selectedComplexity.value.multiplier) : 1
  const ht = Math.round(base * mult)
  const vat = Math.round(ht * 0.2)
  const ttc = ht + vat
  return {
    subtotal_ht: ht,
    vat,
    total_ttc: ttc,
    i1: Math.round(ttc * 0.30),
    i2: Math.round(ttc * 0.40),
    i3: ttc - Math.round(ttc * 0.30) - Math.round(ttc * 0.40),
  }
})

function formatPrice(value) {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency', currency: 'EUR', maximumFractionDigits: 0,
  }).format(value)
}

useHead({
  title: 'Estimer le prix d\'un site web | Simulateur en ligne - Zsdevweb',
  meta: [
    { name: 'description', content: 'Estimez gratuitement et en 30 secondes le prix de votre site web, e-commerce ou application SaaS avec notre simulateur.' },
    { property: 'og:title', content: 'Estimer le prix d\'un site web' },
    { property: 'og:description', content: 'Estimez le coût de votre projet en ligne.' }
  ]
})
</script>
