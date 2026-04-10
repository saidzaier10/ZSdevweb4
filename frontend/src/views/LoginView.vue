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
            class="input w-full"
            placeholder="votre@email.fr"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            class="input w-full"
            placeholder="••••••••"
          />
        </div>

        <p v-if="errorMsg" class="text-sm text-red-600">{{ errorMsg }}</p>

        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? 'Connexion…' : 'Se connecter' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useHead } from '@unhead/vue'

useHead({ title: 'Connexion — Zsdevweb' })

const router = useRouter()
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
    router.push('/espace-client')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Identifiants incorrects.'
  } finally {
    loading.value = false
  }
}
</script>
