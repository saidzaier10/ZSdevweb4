<template>
  <div class="min-h-screen bg-gray-50 py-16 px-4">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-4xl font-bold text-gray-900 mb-3">Contactez-moi</h1>
      <p class="text-gray-500 mb-10">Une question, un projet ? Je réponds sous 24h.</p>

      <div v-if="sent" class="card text-center py-12">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Message envoyé !</h2>
        <p class="text-gray-500">Je vous répondrai dans les 24h. À bientôt !</p>
      </div>

      <div v-if="errorMsg" class="flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm" role="alert">
        <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        {{ errorMsg }}
      </div>

      <form v-else @submit.prevent="submit" class="card space-y-5">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <BaseInput v-model="form.name" label="Nom complet" required />
          <BaseInput v-model="form.email" label="Email" type="email" required />
        </div>
        <BaseInput v-model="form.phone" label="Téléphone" type="tel" />
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Sujet</label>
          <select v-model="form.subject" class="input-field">
            <option value="project">Nouveau projet</option>
            <option value="quote">Demande de devis</option>
            <option value="partnership">Partenariat</option>
            <option value="other">Autre</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Message *</label>
          <textarea v-model="form.message" rows="5" required class="input-field resize-none" placeholder="Décrivez votre projet ou votre demande..." />
        </div>
        <BaseButton type="submit" :loading="loading" class="w-full justify-center">
          Envoyer le message
        </BaseButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { contactApi } from '@/api/contact.js'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const form = reactive({ name: '', email: '', phone: '', company: '', subject: 'project', message: '' })
const loading = ref(false)
const sent = ref(false)
const errorMsg = ref('')

async function submit() {
  loading.value = true
  errorMsg.value = ''
  try {
    await contactApi.send(form)
    sent.value = true
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Une erreur est survenue. Veuillez réessayer.'
  } finally {
    loading.value = false
  }
}

import { useHead } from '@unhead/vue'

useHead({
  title: 'Contactez Zsdevweb — Devis et Création Web à Mouvaux / Lille',
  meta: [
    { name: 'description', content: 'Un projet de création de site internet ou d\'application sur la métropole lilloise (Mouvaux, Roubaix, Tourcoing) ? Contactez-moi pour en discuter.' },
    { property: 'og:title', content: 'Contactez Zsdevweb' },
    { property: 'og:description', content: 'Un projet sur la métropole lilloise ? Contactez-moi pour en discuter.' }
  ]
})
</script>
