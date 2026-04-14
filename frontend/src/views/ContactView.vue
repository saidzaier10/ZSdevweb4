<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-16 px-4">
    <div class="max-w-6xl mx-auto">

      <!-- En-tête -->
      <div class="mb-10">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-3">Contactez-moi</h1>
        <p class="text-gray-600 dark:text-gray-400">Une question, un projet ? Je réponds sous 24h.</p>
      </div>

      <!-- Succès -->
      <div v-if="sent" class="card dark:bg-gray-800 text-center py-12 max-w-2xl">
        <div class="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Message envoyé !</h2>
        <p class="text-gray-600 dark:text-gray-400">Je vous répondrai dans les 24h. À bientôt !</p>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

        <!-- Formulaire -->
        <div>
          <div v-if="errorMsg" class="flex items-center gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-700 dark:text-red-400 text-sm mb-5" role="alert">
            <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            {{ errorMsg }}
          </div>

          <form @submit.prevent="submit" class="card dark:bg-gray-800 dark:border-gray-700 space-y-5">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <BaseInput v-model="form.name" label="Nom complet" required />
              <BaseInput v-model="form.email" label="Email" type="email" required />
            </div>
            <BaseInput v-model="form.phone" label="Téléphone" type="tel" />
            <div>
              <label for="subject" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Sujet</label>
              <select id="subject" v-model="form.subject" class="input-field">
                <option value="project">Nouveau projet</option>
                <option value="quote">Demande de devis</option>
                <option value="partnership">Partenariat</option>
                <option value="other">Autre</option>
              </select>
            </div>
            <div>
              <label for="message" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Message *</label>
              <textarea id="message" v-model="form.message" rows="5" required class="input-field resize-none" placeholder="Décrivez votre projet ou votre demande..." />
            </div>
            <BaseButton type="submit" :loading="loading" class="w-full justify-center">
              Envoyer le message
            </BaseButton>
          </form>
        </div>

        <!-- Carte + infos -->
        <div class="space-y-5">

          <!-- Carte Google Maps — La Plaine Image, Tourcoing -->
          <div class="card dark:bg-gray-800 dark:border-gray-700 p-0 overflow-hidden">
            <iframe
              title="Localisation — La Plaine Image, Tourcoing"
              src="https://maps.google.com/maps?q=Plaine+Images+165+Boulevard+de+l%27Egalite+59200+Tourcoing&t=&z=15&ie=UTF8&iwloc=&output=embed&hl=fr"
              width="100%"
              height="300"
              style="border:0; display:block;"
              allowfullscreen
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
              aria-label="Carte Google Maps — La Plaine Image, Tourcoing"
            />
          </div>

          <!-- Infos de contact -->
          <div class="card dark:bg-gray-800 dark:border-gray-700 space-y-4">
            <h2 class="font-bold text-gray-900 dark:text-white">Informations</h2>

            <div class="flex items-start gap-3">
              <div class="w-9 h-9 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">La Plaine Image</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">165 Bd de l'Égalité, 59200 Tourcoing</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Métropole lilloise</p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="w-9 h-9 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Email</p>
                <a href="mailto:contact@zsdevweb.fr" class="text-sm text-primary-600 hover:underline">contact@zsdevweb.fr</a>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="w-9 h-9 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Disponibilité</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Lun – Ven, 9h – 18h</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Réponse sous 24h</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { contactApi } from '@/api/contact.js'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useHead } from '@unhead/vue'

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

useHead({
  title: 'Contactez Zsdevweb — Devis et Création Web à Tourcoing / Lille',
  meta: [
    { name: 'description', content: 'Développeur web freelance basé à La Plaine Image, Tourcoing. Un projet de création de site ou d\'application sur la métropole lilloise ? Contactez-moi sous 24h.' },
    { property: 'og:title', content: 'Contactez Zsdevweb — La Plaine Image, Tourcoing' },
    { property: 'og:description', content: 'Développeur web freelance basé à La Plaine Image, Tourcoing. Contactez-moi pour votre projet.' },
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'LocalBusiness',
        name: 'Zsdevweb',
        url: 'https://zsdevweb.fr',
        email: 'contact@zsdevweb.fr',
        description: 'Développeur web freelance spécialisé dans la création de sites et applications sur-mesure pour TPE et PME de la métropole lilloise.',
        address: {
          '@type': 'PostalAddress',
          streetAddress: '165 Boulevard de l\'Égalité',
          addressLocality: 'Tourcoing',
          addressRegion: 'Hauts-de-France',
          postalCode: '59200',
          addressCountry: 'FR',
        },
        geo: {
          '@type': 'GeoCoordinates',
          latitude: 50.7186,
          longitude: 3.1747,
        },
        hasMap: 'https://maps.google.com/maps?q=Plaine+Images+Tourcoing',
        areaServed: [
          { '@type': 'City', name: 'Tourcoing' },
          { '@type': 'City', name: 'Roubaix' },
          { '@type': 'City', name: 'Mouvaux' },
          { '@type': 'City', name: 'Lille' },
        ],
        openingHoursSpecification: [
          {
            '@type': 'OpeningHoursSpecification',
            dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            opens: '09:00',
            closes: '18:00',
          },
        ],
      }),
    },
  ],
})
</script>
