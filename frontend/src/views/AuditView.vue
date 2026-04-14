<template>
  <div class="min-h-screen bg-gray-50 py-16 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-10">
        <div class="inline-flex items-center gap-2 bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
          100% Gratuit — Sans engagement
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-3">Audit gratuit de votre site web</h1>
        <p class="text-gray-500">Je vous remets un rapport d'audit complet sous 48h : performance, SEO, UX, conversions.</p>
      </div>

      <div v-if="sent" class="card text-center py-12">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Demande reçue !</h2>
        <p class="text-gray-500">Je vous enverrai votre rapport d'audit dans les 48h.</p>
      </div>

      <form v-else @submit.prevent="submit" class="card space-y-5">
        <BaseInput v-model="form.site_url" label="URL de votre site" type="url" placeholder="https://monsite.fr" required />
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <BaseInput v-model="form.name" label="Votre nom" required />
          <BaseInput v-model="form.email" label="Email" type="email" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Vos objectifs principaux</label>
          <div class="grid grid-cols-2 gap-2">
            <label v-for="obj in objectives" :key="obj.value" class="flex items-center gap-2 p-3 rounded-lg border border-gray-200 cursor-pointer hover:bg-gray-50">
              <input type="checkbox" :value="obj.value" v-model="form.objectives" class="rounded border-gray-300 text-primary-600" />
              <span class="text-sm text-gray-700">{{ obj.label }}</span>
            </label>
          </div>
        </div>
        <div>
          <label for="current_issues" class="block text-sm font-medium text-gray-700 mb-1">Problèmes actuels identifiés</label>
          <textarea id="current_issues" v-model="form.current_issues" rows="3" class="input-field resize-none" placeholder="Ex: Mon site est lent, je ne génère pas de leads..." />
        </div>
        <BaseButton type="submit" :loading="loading" class="w-full justify-center">
          Demander mon audit gratuit →
        </BaseButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { auditApi } from '@/api/audit.js'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useHead } from '@unhead/vue'

const form = reactive({ site_url: '', name: '', email: '', phone: '', company: '', current_issues: '', objectives: [], budget_range: '' })
const loading = ref(false)
const sent = ref(false)
const objectives = [
  { value: 'more_traffic', label: 'Plus de trafic' },
  { value: 'more_leads', label: 'Plus de leads' },
  { value: 'better_ux', label: 'Meilleure UX' },
  { value: 'faster_site', label: 'Site plus rapide' },
  { value: 'seo', label: 'Meilleur SEO' },
  { value: 'mobile', label: 'Optimisation mobile' },
]

async function submit() {
  loading.value = true
  try {
    await auditApi.request(form)
    sent.value = true
  } catch {
    alert('Une erreur est survenue.')
  } finally {
    loading.value = false
  }
}

useHead({
  title: 'Audit SEO et Performance Gratuit pour votre TPE/PME | Zsdevweb',
  meta: [
    { name: 'description', content: 'Obtenez un audit SEO et technique gratuit à 100% pour votre entreprise. Zsdevweb analyse gratuitement la performance de votre site local.' },
    { property: 'og:title', content: 'Audit SEO Gratuit par Zsdevweb' },
    { property: 'og:description', content: 'Obtenez un audit SEO complet gratuit pour votre site internet.' }
  ]
})
</script>
