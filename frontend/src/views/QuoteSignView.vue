<template>
  <div class="min-h-screen bg-gray-50 py-16 px-4">
    <div class="max-w-xl mx-auto">

      <!-- Loading -->
      <div v-if="loading" class="card text-center py-16">
        <LoadingSpinner />
        <p class="text-gray-500 mt-4">Vérification du lien...</p>
      </div>

      <!-- Erreur de token -->
      <div v-else-if="tokenError" class="card text-center py-12">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Lien invalide</h2>
        <p class="text-gray-600">{{ tokenError }}</p>
        <RouterLink to="/contact" class="btn-primary mt-6 inline-flex">Nous contacter</RouterLink>
      </div>

      <!-- Déjà signé -->
      <div v-else-if="alreadySigned" class="card text-center py-12">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-500" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Devis {{ alreadySignedStatus }}</h2>
        <p class="text-gray-600">Ce devis a déjà été traité.</p>
      </div>

      <!-- Formulaire de signature -->
      <div v-else-if="quoteInfo && !signed && !rejected">
        <!-- Breadcrumb -->
        <Breadcrumb :crumbs="[{ label: 'Accueil', to: '/' }, { label: 'Signature du devis' }]" />

        <!-- En-tête -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-900">Signature du devis</h1>
          <p class="text-gray-600 mt-1">{{ quoteInfo.quote_number }}</p>
        </div>

        <!-- Récapitulatif -->
        <div class="card mb-6">
          <h3 class="font-semibold text-gray-900 mb-4">Récapitulatif</h3>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">Client</span>
              <span class="font-medium">{{ quoteInfo.client_name }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Montant TTC</span>
              <span class="font-bold text-xl text-primary-600">{{ formatPrice(quoteInfo.total_ttc) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Valable jusqu'au</span>
              <span class="font-medium">{{ formatDate(quoteInfo.valid_until) }}</span>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-100">
            <RouterLink :to="`/devis/${uuid}`" class="text-sm text-primary-600 hover:underline">
              → Consulter le devis complet
            </RouterLink>
          </div>
        </div>

        <!-- Champ signature -->
        <div class="card mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Votre nom complet (pour valider la signature)
          </label>
          <input
            v-model="signatureName"
            type="text"
            :placeholder="quoteInfo.client_name"
            class="w-full border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <p class="text-xs text-gray-500 mt-2">
            En signant, vous acceptez les conditions générales de vente disponibles sur zsdevweb.fr/cgv.
          </p>
        </div>

        <!-- Boutons d'action -->
        <div class="space-y-3">
          <button
            @click="sign('accept')"
            :disabled="submitting || !signatureName.trim()"
            class="btn-primary w-full justify-center py-4 text-base disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="submitting">Signature en cours...</span>
            <span v-else>✅ Accepter et signer le devis</span>
          </button>

          <button
            @click="showRejectForm = !showRejectForm"
            class="w-full text-center text-sm text-gray-500 hover:text-red-500 transition-colors py-2"
          >
            Je souhaite refuser ce devis
          </button>

          <!-- Erreur de signature -->
          <div v-if="signError" class="flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm" role="alert">
            <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            {{ signError }}
          </div>

          <!-- Formulaire de refus -->
          <div v-if="showRejectForm" class="card border-red-100 bg-red-50">
            <label for="reject_reason" class="block text-sm font-medium text-red-700 mb-3">Motif du refus (optionnel)</label>
            <textarea
              id="reject_reason"
              v-model="rejectReason"
              rows="3"
              placeholder="Budget, délai, changement de projet..."
              class="w-full border border-red-200 rounded-xl px-4 py-3 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-red-400"
            />
            <button
              @click="sign('reject')"
              :disabled="submitting"
              class="mt-3 w-full py-3 rounded-xl border-2 border-red-400 text-red-600 font-semibold text-sm hover:bg-red-50 transition-all disabled:opacity-50"
            >
              Confirmer le refus
            </button>
          </div>
        </div>
      </div>

      <!-- Succès — Accepté -->
      <div v-else-if="signed" class="card text-center py-12 animate-fade-in">
        <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-green-500" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Devis accepté !</h2>
        <p class="text-gray-600 mb-6">
          Merci {{ quoteInfo?.client_name }}. Votre devis a été signé avec succès.<br>
          Nous vous contacterons dans les 24h pour démarrer votre projet.
        </p>
        <div class="bg-green-50 rounded-xl p-4 text-sm text-green-800 mb-6">
          Un acompte de <strong>{{ formatPrice(Number(quoteInfo?.total_ttc) * 0.3) }}</strong> (30%) sera demandé à la signature du contrat.
        </div>
        <RouterLink to="/contact" class="btn-primary inline-flex">
          Nous envoyer un message →
        </RouterLink>
      </div>

      <!-- Succès — Refusé -->
      <div v-else-if="rejected" class="card text-center py-12">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Devis refusé</h2>
        <p class="text-gray-600 mb-6">Merci pour votre retour. N'hésitez pas à nous recontacter si vous changez d'avis.</p>
        <RouterLink to="/contact" class="btn-secondary inline-flex">Nous contacter</RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios.js'
import { useHead } from '@unhead/vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import Breadcrumb from '@/components/ui/Breadcrumb.vue'
import { formatPrice } from '@/utils/formatters.js'

useHead({
  title: 'Signer votre devis | Zsdevweb',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})

const route = useRoute()
const uuid = route.params.uuid
const token = route.query.token || ''

const loading = ref(true)
const tokenError = ref('')
const alreadySigned = ref(false)
const alreadySignedStatus = ref('')
const quoteInfo = ref(null)
const signatureName = ref('')
const rejectReason = ref('')
const showRejectForm = ref(false)
const submitting = ref(false)
const signed = ref(false)
const rejected = ref(false)
const signError = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get(`/api/v1/quotes/${uuid}/sign/?token=${token}`)
    if (data.valid) {
      quoteInfo.value = data
    } else {
      if (data.status && ['accepted', 'rejected', 'expired'].includes(data.status)) {
        alreadySigned.value = true
        alreadySignedStatus.value = data.detail
      } else {
        tokenError.value = data.detail || 'Lien de signature invalide.'
      }
    }
  } catch (e) {
    const msg = e.response?.data?.detail
    if (e.response?.status === 400 && msg) {
      alreadySigned.value = true
      alreadySignedStatus.value = msg
    } else {
      tokenError.value = 'Lien de signature invalide ou expiré.'
    }
  } finally {
    loading.value = false
  }
})

async function sign(action) {
  submitting.value = true
  try {
    await api.post(`/api/v1/quotes/${uuid}/sign/`, {
      token,
      action,
      signature_name: signatureName.value,
      reason: rejectReason.value,
    })
    if (action === 'accept') {
      signed.value = true
    } else {
      rejected.value = true
    }
  } catch (e) {
    signError.value = e.response?.data?.detail || 'Une erreur est survenue. Veuillez réessayer.'
  } finally {
    submitting.value = false
  }
}



function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' })
}
</script>
