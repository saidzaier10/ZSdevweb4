<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="card w-full max-w-md">

      <!-- Succès -->
      <div v-if="sent" class="text-center py-4">
        <div class="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Email envoyé</h1>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Si cet email est enregistré, vous recevrez un lien de réinitialisation dans quelques minutes.
          Pensez à vérifier vos spams.
        </p>
        <RouterLink to="/connexion" class="btn-primary inline-flex">Retour à la connexion</RouterLink>
      </div>

      <!-- Formulaire -->
      <template v-else>
        <div class="mb-6">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Mot de passe oublié</h1>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Entrez votre email, nous vous enverrons un lien de réinitialisation.
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              class="input-field w-full"
              placeholder="votre@email.fr"
            />
          </div>

          <p v-if="errorMsg" class="text-sm text-red-600" role="alert">{{ errorMsg }}</p>

          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? 'Envoi…' : 'Envoyer le lien' }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-600 dark:text-gray-400 mt-5">
          <RouterLink to="/connexion" class="text-primary-600 hover:underline">
            Retour à la connexion
          </RouterLink>
        </p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authApi } from '@/api/auth.js'
import { useHead } from '@unhead/vue'

useHead({ title: 'Mot de passe oublié — Zsdevweb' })

const email   = ref('')
const loading = ref(false)
const sent    = ref(false)
const errorMsg = ref('')

async function handleSubmit() {
  loading.value = true
  errorMsg.value = ''
  try {
    await authApi.passwordResetRequest(email.value)
    sent.value = true
  } catch {
    errorMsg.value = 'Une erreur est survenue. Veuillez réessayer.'
  } finally {
    loading.value = false
  }
}
</script>
