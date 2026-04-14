<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="card w-full max-w-md">
      <h1 class="text-2xl font-bold text-gray-900 mb-6 text-center">Connexion</h1>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
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

        <div>
          <PasswordInput
            v-model="password"
            label="Mot de passe"
            input-id="password"
            required
            autocomplete="current-password"
          />
        </div>

        <div class="flex items-center justify-between">
          <p v-if="errorMsg" class="text-sm text-red-600" role="alert">{{ errorMsg }}</p>
          <RouterLink to="/mot-de-passe-oublie" class="text-sm text-primary-600 hover:underline ml-auto">
            Mot de passe oublié ?
          </RouterLink>
        </div>

        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? 'Connexion…' : 'Se connecter' }}
        </button>
      </form>

      <p class="text-sm text-center text-gray-500 dark:text-gray-400 mt-6">
        Pas encore de compte ?
        <RouterLink to="/inscription" class="text-primary-600 hover:underline font-medium">Créer un compte</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useHead } from '@unhead/vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'

useHead({ title: 'Connexion — Zsdevweb' })

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''
  try {
    await authStore.login(email.value, password.value)
    const redirect = route.query.redirect
    if (redirect && redirect.startsWith('/')) {
      router.push(redirect)
    } else if (authStore.user?.is_staff) {
      router.push('/tableau-de-bord')
    } else {
      router.push('/espace-client')
    }
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Identifiants incorrects.'
  } finally {
    loading.value = false
  }
}
</script>
