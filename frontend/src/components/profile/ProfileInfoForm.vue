<template>
  <div class="card">
    <h2 class="font-bold text-gray-900 dark:text-white mb-5">Informations personnelles</h2>

    <form @submit.prevent="save" class="space-y-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label for="first_name" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Prénom</label>
          <input id="first_name" v-model="form.first_name" type="text" class="input-field w-full" placeholder="Prénom" />
        </div>
        <div>
          <label for="last_name" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Nom</label>
          <input id="last_name" v-model="form.last_name" type="text" class="input-field w-full" placeholder="Nom" />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Email</label>
        <input :value="user?.email" type="email" class="input-field w-full opacity-60" disabled />
        <p class="text-xs text-gray-400 mt-1">L'email ne peut pas être modifié.</p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Téléphone</label>
          <input id="phone" v-model="form.phone" type="tel" class="input-field w-full" placeholder="+33 6 12 34 56 78" />
        </div>
        <div>
          <label for="company" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Entreprise</label>
          <input id="company" v-model="form.company" type="text" class="input-field w-full" placeholder="Nom de l'entreprise" />
        </div>
      </div>

      <div v-if="msg" class="flex items-center gap-2 text-sm" :class="success ? 'text-green-600' : 'text-red-600'" role="alert">
        <svg v-if="success" class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ msg }}
      </div>

      <div class="flex justify-end">
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Enregistrement…' : 'Enregistrer' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { authApi } from '@/api/auth.js'

const authStore = useAuthStore()
const user = authStore.user

const form = reactive({
  first_name: user?.first_name || '',
  last_name:  user?.last_name  || '',
  phone:      user?.phone      || '',
  company:    user?.company    || '',
})

const loading = ref(false)
const msg     = ref('')
const success = ref(false)

async function save() {
  loading.value = true
  msg.value = ''
  try {
    const { data } = await authApi.updateMe(form)
    authStore.updateUser(data)
    success.value = true
    msg.value = 'Profil mis à jour.'
  } catch {
    success.value = false
    msg.value = 'Erreur lors de la mise à jour.'
  } finally {
    loading.value = false
  }
}
</script>
