<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="card w-full max-w-md">

      <!-- Lien invalide -->
      <div v-if="invalidLink" class="text-center py-4">
        <div class="w-14 h-14 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Lien invalide</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Ce lien de réinitialisation est invalide ou a expiré.
        </p>
        <RouterLink to="/mot-de-passe-oublie" class="btn-primary inline-flex">Faire une nouvelle demande</RouterLink>
      </div>

      <!-- Succès -->
      <div v-else-if="done" class="text-center py-4">
        <div class="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Mot de passe mis à jour</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.
        </p>
        <RouterLink to="/connexion" class="btn-primary inline-flex">Se connecter</RouterLink>
      </div>

      <!-- Formulaire -->
      <template v-else>
        <div class="mb-6">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Nouveau mot de passe</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Choisissez un mot de passe d'au moins 8 caractères.</p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <PasswordInput
            v-model="password"
            label="Nouveau mot de passe"
            input-id="password"
            required
            minlength="8"
            autocomplete="new-password"
          />
          <PasswordInput
            v-model="password2"
            label="Confirmer"
            input-id="password2"
            required
            minlength="8"
            autocomplete="new-password"
          />

          <p v-if="errorMsg" class="text-sm text-red-600" role="alert">{{ errorMsg }}</p>

          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? 'Enregistrement…' : 'Enregistrer le mot de passe' }}
          </button>
        </form>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { authApi } from '@/api/auth.js'
import { useHead } from '@unhead/vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'

useHead({ title: 'Nouveau mot de passe — Zsdevweb' })

const route = useRoute()
const uid   = route.query.uid   || ''
const token = route.query.token || ''

const password  = ref('')
const password2 = ref('')
const loading   = ref(false)
const done      = ref(false)
const errorMsg  = ref('')
const invalidLink = ref(!uid || !token)

async function handleSubmit() {
  errorMsg.value = ''
  if (password.value !== password2.value) {
    errorMsg.value = 'Les mots de passe ne correspondent pas.'
    return
  }
  loading.value = true
  try {
    await authApi.passwordResetConfirm({ uid, token, password: password.value })
    done.value = true
  } catch (e) {
    const detail = e.response?.data
    if (detail?.uid || detail?.token) {
      invalidLink.value = true
    } else {
      errorMsg.value = detail?.password?.[0] || detail?.detail || 'Une erreur est survenue.'
    }
  } finally {
    loading.value = false
  }
}
</script>
