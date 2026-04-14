<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4 py-12">
    <div class="card w-full max-w-md">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2 text-center">Créer un compte</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 text-center mb-6">
        Suivez l'avancement de votre projet en temps réel.
      </p>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Prénom</label>
            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              autocomplete="given-name"
              class="input-field w-full"
              placeholder="Jean"
            />
          </div>
          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Nom</label>
            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              autocomplete="family-name"
              class="input-field w-full"
              placeholder="Dupont"
            />
          </div>
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            autocomplete="email"
            class="input-field w-full"
            :class="{ 'border-red-400': errors.email }"
            placeholder="votre@email.fr"
          />
          <p v-if="errors.email" class="text-xs text-red-600 mt-1">{{ errors.email }}</p>
        </div>

        <PasswordInput
          v-model="form.password"
          label="Mot de passe"
          input-id="password"
          required
          minlength="8"
          autocomplete="new-password"
          placeholder="8 caractères minimum"
          :error="errors.password"
        />

        <PasswordInput
          v-model="form.password2"
          label="Confirmer le mot de passe"
          input-id="password2"
          required
          minlength="8"
          autocomplete="new-password"
          :error="errors.password2"
        />

        <p v-if="errors.non_field" class="text-sm text-red-600" role="alert">{{ errors.non_field }}</p>

        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? 'Création du compte…' : 'Créer mon compte' }}
        </button>
      </form>

      <p class="text-sm text-center text-gray-500 dark:text-gray-400 mt-6">
        Déjà un compte ?
        <RouterLink to="/connexion" class="text-primary-600 hover:underline font-medium">Se connecter</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { authApi } from '@/api/auth.js'
import { useHead } from '@unhead/vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'

useHead({
  title: 'Créer un compte | Zsdevweb',
  meta: [{ name: 'robots', content: 'noindex, nofollow' }],
})

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ email: '', password: '', password2: '', first_name: '', last_name: '' })
const errors = reactive({ email: '', password: '', password2: '', non_field: '' })
const loading = ref(false)

function clearErrors() {
  errors.email = ''
  errors.password = ''
  errors.password2 = ''
  errors.non_field = ''
}

async function handleRegister() {
  clearErrors()
  loading.value = true
  try {
    await authApi.register(form)
    // Connexion automatique après inscription
    await authStore.login(form.email, form.password)
    router.push(authStore.user?.is_staff ? '/tableau-de-bord' : '/espace-client')
  } catch (e) {
    const data = e.response?.data
    if (data) {
      errors.email    = data.email?.[0]    || ''
      errors.password = data.password?.[0] || ''
      errors.password2 = data.password2?.[0] || ''
      errors.non_field = data.detail || data.non_field_errors?.[0] || ''
    } else {
      errors.non_field = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    loading.value = false
  }
}
</script>
