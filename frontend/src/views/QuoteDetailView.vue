<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-3xl mx-auto">
      <div v-if="loading" class="space-y-6" aria-busy="true">
        <!-- Skeleton header -->
        <div class="card space-y-4">
          <div class="flex justify-between items-start">
            <div class="space-y-2">
              <SkeletonLoader height="h-3" width="w-16" />
              <SkeletonLoader height="h-7" width="w-48" />
            </div>
            <SkeletonLoader height="h-6" width="w-20" rounded="rounded-full" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="i in 4" :key="i" class="space-y-1">
              <SkeletonLoader height="h-3" width="w-16" />
              <SkeletonLoader height="h-4" width="w-32" />
            </div>
          </div>
        </div>
        <!-- Skeleton prix -->
        <div class="card space-y-3">
          <SkeletonLoader height="h-5" width="w-36" />
          <div v-for="i in 4" :key="i" class="flex justify-between">
            <SkeletonLoader height="h-4" width="w-40" />
            <SkeletonLoader height="h-4" width="w-20" />
          </div>
          <SkeletonLoader height="h-16" rounded="rounded-xl" />
        </div>
      </div>

      <div v-else-if="error" class="card text-center py-16">
        <p class="text-red-600 mb-4">Devis introuvable ou expiré.</p>
        <RouterLink to="/devis" class="btn-primary">Faire une nouvelle demande</RouterLink>
      </div>

      <template v-else-if="quote">
        <!-- Breadcrumb -->
        <Breadcrumb :crumbs="[{ label: 'Accueil', to: '/' }, { label: 'Devis', to: '/devis' }, { label: quote.quote_number }]" />

        <!-- Header devis -->
        <div class="card mb-6">
          <div class="flex items-start justify-between mb-6">
            <div>
              <div class="text-sm text-gray-400 mb-1">Devis n°</div>
              <div class="flex items-center gap-2">
                <div class="text-2xl font-bold text-gray-900">{{ quote.quote_number }}</div>
                <button
                  @click="copyQuoteNumber"
                  :title="copied ? 'Copié !' : 'Copier le numéro'"
                  class="p-1.5 rounded-lg text-gray-400 hover:text-primary-600 hover:bg-primary-50 transition-colors"
                  :aria-label="copied ? 'Numéro copié' : 'Copier le numéro de devis'"
                >
                  <svg v-if="!copied" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <svg v-else class="w-4 h-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </div>
            <StatusBadge :status="quote.status" :label="quote.status_display" />
          </div>

          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div class="text-gray-400">Client</div>
              <div class="font-medium">{{ quote.client_name }}</div>
            </div>
            <div>
              <div class="text-gray-400">Email</div>
              <div class="font-medium">{{ quote.client_email }}</div>
            </div>
            <div>
              <div class="text-gray-400">Projet</div>
              <div class="font-medium">{{ quote.project_type?.name }}</div>
            </div>
            <div>
              <div class="text-gray-400">Valable jusqu'au</div>
              <div class="font-medium" :class="{ 'text-red-500': quote.is_expired }">
                {{ formatDate(quote.valid_until) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Détail des prix -->
        <div class="card mb-6">
          <h2 class="font-bold text-gray-900 mb-4">Détail du devis</h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between text-gray-600">
              <span>Prix de base ({{ quote.project_type?.name }})</span>
              <span>{{ formatPrice(quote.base_price) }}</span>
            </div>
            <div v-if="parseFloat(quote.design_supplement) > 0" class="flex justify-between text-gray-600">
              <span>Design ({{ quote.design_option?.name }})</span>
              <span>+{{ formatPrice(quote.design_supplement) }}</span>
            </div>
            <div v-if="parseFloat(quote.complexity_factor) > 1" class="flex justify-between text-gray-600">
              <span>Complexité ({{ quote.complexity?.name }})</span>
              <span>×{{ quote.complexity_factor }}</span>
            </div>
            <div v-if="parseFloat(quote.options_total) > 0" class="flex justify-between text-gray-600">
              <span>Options supplémentaires</span>
              <span>+{{ formatPrice(quote.options_total) }}</span>
            </div>
            <div v-if="quote.options?.length > 0" class="pl-4 space-y-1">
              <div v-for="opt in quote.options" :key="opt.id" class="flex justify-between text-gray-400 text-xs">
                <span>↳ {{ opt.name }}</span>
                <span>{{ formatPrice(opt.price) }}</span>
              </div>
            </div>
            <div class="border-t border-gray-100 pt-2 flex justify-between">
              <span class="text-gray-600">Sous-total HT</span>
              <span class="font-medium">{{ formatPrice(quote.subtotal_ht) }}</span>
            </div>
            <div v-if="parseFloat(quote.discount_amount) > 0" class="flex justify-between text-green-600">
              <span>Remise ({{ quote.discount_percent }}%)</span>
              <span>-{{ formatPrice(quote.discount_amount) }}</span>
            </div>
            <div class="flex justify-between text-gray-500">
              <span>TVA {{ quote.vat_rate }}%</span>
              <span>+{{ formatPrice(quote.vat_amount) }}</span>
            </div>
          </div>

          <div class="bg-primary-50 rounded-xl p-4 mt-4">
            <div class="flex justify-between items-center">
              <span class="font-bold text-gray-900 text-lg">Total TTC</span>
              <span class="text-3xl font-bold text-primary-600">{{ formatPrice(quote.total_ttc) }}</span>
            </div>
          </div>
        </div>

        <!-- Plan de paiement -->
        <div class="card mb-6">
          <h2 class="font-bold text-gray-900 mb-4">Plan de paiement en 3 fois</h2>
          <div class="space-y-3">
            <div v-for="(item, idx) in installments" :key="idx" class="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-bold">{{ idx + 1 }}</div>
                <div>
                  <div class="font-medium text-sm text-gray-900">{{ item.label }}</div>
                  <div class="text-xs text-gray-400">{{ item.timing }}</div>
                </div>
              </div>
              <span class="font-bold text-gray-900">{{ formatPrice(item.amount) }}</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row gap-3">
          <a :href="pdfUrl" target="_blank" class="btn-secondary flex-1 justify-center">
            Télécharger le PDF
          </a>
          <RouterLink to="/contact" class="btn-primary flex-1 justify-center">
            Accepter le devis →
          </RouterLink>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { quotesApi } from '@/api/quotes.js'
import { useHead } from '@unhead/vue'
import Breadcrumb from '@/components/ui/Breadcrumb.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'
import { formatPrice } from '@/utils/formatters.js'

useHead({
  title: 'Votre devis | Zsdevweb',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})

const route = useRoute()
const quote = ref(null)
const loading = ref(true)
const error = ref(false)
const copied = ref(false)

async function copyQuoteNumber() {
  if (!quote.value) return
  await navigator.clipboard.writeText(quote.value.quote_number)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

onMounted(async () => {
  try {
    const { data } = await quotesApi.getByUuid(route.params.uuid)
    quote.value = data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})

const pdfUrl = computed(() => quote.value ? quotesApi.getPdfUrl(quote.value.uuid) : '#')

const installments = computed(() => {
  if (!quote.value) return []
  return [
    { label: 'Acompte à la signature', timing: '30% — due immédiatement', amount: quote.value.installment_1 },
    { label: 'Mi-projet', timing: '40% — à mi-parcours', amount: quote.value.installment_2 },
    { label: 'Livraison', timing: '30% — à la remise des livrables', amount: quote.value.installment_3 },
  ]
})

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
