<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div v-if="!quoteStore.submitted" class="max-w-5xl mx-auto">
      <!-- En-tête -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-3">Obtenir un devis gratuit</h1>
        <p class="text-gray-500 text-lg">Répondez à quelques questions et recevez votre devis personnalisé en quelques minutes.</p>
      </div>

      <QuoteWizard @submitted="onSubmitted" />
    </div>

    <!-- Confirmation -->
    <div v-else class="max-w-2xl mx-auto text-center py-20">
      <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h2 class="text-3xl font-bold text-gray-900 mb-3">Demande reçue !</h2>
      <p class="text-gray-500 text-lg mb-2">
        Votre devis <strong>{{ quoteStore.submittedQuote?.quote_number }}</strong> a été créé.
      </p>
      <p class="text-gray-500 mb-8">
        Vous recevrez votre devis détaillé à <strong>{{ quoteStore.submittedQuote?.client_email }}</strong> sous 24h.
      </p>

      <!-- Récapitulatif prix -->
      <div v-if="quoteStore.submittedQuote" class="card max-w-sm mx-auto mb-8 text-left">
        <div class="flex justify-between items-center mb-3">
          <span class="text-gray-500">Total TTC</span>
          <span class="text-2xl font-bold text-primary-600">
            {{ formatPrice(quoteStore.submittedQuote.total_ttc) }}
          </span>
        </div>
        <div class="text-sm text-gray-500">
          Valide jusqu'au {{ formatDate(quoteStore.submittedQuote.valid_until) }}
        </div>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <RouterLink to="/" class="btn-secondary">
          Retour à l'accueil
        </RouterLink>
        <button @click="quoteStore.reset()" class="btn-primary">
          Nouveau devis
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeRouteLeave } from 'vue-router'
import { useQuoteStore } from '@/stores/quote.js'
import QuoteWizard from '@/components/quote/QuoteWizard.vue'
import { formatPrice } from '@/utils/formatters.js'
import { useHead } from '@unhead/vue'

const quoteStore = useQuoteStore()

function onSubmitted(quote) {
  // Le store gère déjà l'état submitted
}

onBeforeRouteLeave(() => {
  const hasProgress = quoteStore.currentStep > 1 && !quoteStore.submitted
  if (!hasProgress) return true
  return window.confirm('Vous avez un devis en cours. Quitter cette page effacera votre progression. Continuer ?')
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

useHead({
  title: 'Demande de devis création de site internet | Zsdevweb',
  meta: [
    { name: 'description', content: 'Demandez un devis gratuit pour la création de votre site vitrine, e-commerce ou application web sur la métropole lilloise (Mouvaux, Roubaix, Tourcoing).' },
    { property: 'og:title', content: 'Devis Création Site Web' },
    { property: 'og:description', content: 'Demandez un devis gratuit pour votre projet digital.' }
  ]
})
</script>
