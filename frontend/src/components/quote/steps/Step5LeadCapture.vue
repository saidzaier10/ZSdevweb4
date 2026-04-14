<template>
  <div class="animate-fade-in">
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Vos coordonnées</h2>
    <p class="text-gray-600 mb-8">Pour recevoir votre devis personnalisé par email.</p>

    <form @submit.prevent class="space-y-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <BaseInput
          v-model="form.clientName"
          label="Prénom et nom"
          placeholder="Jean Dupont"
          required
          :error="errors.clientName"
          @blur="validateField('clientName')"
        />
        <BaseInput
          v-model="form.clientEmail"
          label="Email"
          type="email"
          placeholder="jean@exemple.fr"
          required
          :error="errors.clientEmail"
          @blur="validateField('clientEmail')"
        />
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <BaseInput
          v-model="form.clientPhone"
          label="Téléphone"
          type="tel"
          placeholder="+33 6 XX XX XX XX"
        />
        <BaseInput
          v-model="form.clientCompany"
          label="Entreprise"
          placeholder="Ma Société"
        />
      </div>

      <div>
        <label for="budget_range" class="block text-sm font-medium text-gray-700 mb-1">Budget estimé</label>
        <select id="budget_range" v-model="form.budgetRange" class="input-field">
          <option value="">Je ne sais pas encore</option>
          <option value="< 1000">Moins de 1 000 €</option>
          <option value="1000-3000">1 000 € — 3 000 €</option>
          <option value="3000-6000">3 000 € — 6 000 €</option>
          <option value="6000-15000">6 000 € — 15 000 €</option>
          <option value="> 15000">Plus de 15 000 €</option>
        </select>
      </div>
    </form>

    <!-- Confiance -->
    <div class="mt-6 flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
      <svg class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
        <path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <div class="text-sm text-gray-600">
        <strong>Vos données sont protégées.</strong> Elles ne seront jamais vendues ni partagées.
        Vous recevrez uniquement votre devis.
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import { useLeadCapture } from '@/composables/useLeadCapture.js'
import BaseInput from '@/components/ui/BaseInput.vue'

defineEmits(['next'])

const quoteStore = useQuoteStore()
const { captureFromStep5 } = useLeadCapture()

const form = reactive({
  clientName: quoteStore.formData.clientName,
  clientEmail: quoteStore.formData.clientEmail,
  clientPhone: quoteStore.formData.clientPhone,
  clientCompany: quoteStore.formData.clientCompany,
  budgetRange: quoteStore.formData.budgetRange,
})

const errors = reactive({
  clientName: '',
  clientEmail: '',
})

function validateField(field) {
  if (field === 'clientName') {
    errors.clientName = form.clientName.trim() ? '' : 'Le prénom et nom sont requis.'
  }
  if (field === 'clientEmail') {
    if (!form.clientEmail.trim()) {
      errors.clientEmail = 'L\'email est requis.'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.clientEmail)) {
      errors.clientEmail = 'Adresse email invalide.'
    } else {
      errors.clientEmail = ''
    }
  }
}

// Sync vers le store à chaque changement + capture lead dès que l'email est valide
watch(form, (val) => {
  quoteStore.updateFormData({ ...val })
  if (val.clientEmail && val.clientName && !errors.clientEmail) {
    captureFromStep5()
  }
}, { deep: true })
</script>
