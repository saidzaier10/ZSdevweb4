<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">

    <!-- En-tête -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-2xl mx-auto px-4 py-8">
        <div class="flex items-center gap-2 text-sm text-gray-400 mb-3">
          <RouterLink to="/espace-client" class="hover:text-primary-600">Espace client</RouterLink>
          <span>/</span>
          <span class="text-gray-600 dark:text-gray-300">Mon profil</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Mon profil</h1>
      </div>
    </div>

    <div class="max-w-2xl mx-auto px-4 py-8 space-y-6">

      <!-- Infos personnelles -->
      <div class="card">
        <h2 class="font-bold text-gray-900 dark:text-white mb-5">Informations personnelles</h2>

        <form @submit.prevent="saveProfile" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Prénom</label>
              <input v-model="profile.first_name" type="text" class="input-field w-full" placeholder="Prénom" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Nom</label>
              <input v-model="profile.last_name" type="text" class="input-field w-full" placeholder="Nom" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input :value="authStore.user?.email" type="email" class="input-field w-full opacity-60" disabled />
            <p class="text-xs text-gray-400 mt-1">L'email ne peut pas être modifié.</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Téléphone</label>
              <input v-model="profile.phone" type="tel" class="input-field w-full" placeholder="+33 6 12 34 56 78" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Entreprise</label>
              <input v-model="profile.company" type="text" class="input-field w-full" placeholder="Nom de l'entreprise" />
            </div>
          </div>

          <div v-if="profileMsg" class="flex items-center gap-2 text-sm" :class="profileSuccess ? 'text-green-600' : 'text-red-600'" role="alert">
            <svg v-if="profileSuccess" class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ profileMsg }}
          </div>

          <div class="flex justify-end">
            <button type="submit" class="btn-primary" :disabled="profileLoading">
              {{ profileLoading ? 'Enregistrement…' : 'Enregistrer' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Changement de mot de passe -->
      <div class="card">
        <h2 class="font-bold text-gray-900 dark:text-white mb-5">Changer le mot de passe</h2>

        <form @submit.prevent="changePassword" class="space-y-4">
          <PasswordInput
            v-model="pwForm.current"
            label="Mot de passe actuel"
            required
            autocomplete="current-password"
          />
          <PasswordInput
            v-model="pwForm.newPw"
            label="Nouveau mot de passe"
            required
            minlength="8"
            autocomplete="new-password"
            placeholder="8 caractères minimum"
          />
          <PasswordInput
            v-model="pwForm.confirm"
            label="Confirmer"
            required
            minlength="8"
            autocomplete="new-password"
          />

          <div v-if="pwMsg" class="flex items-center gap-2 text-sm" :class="pwSuccess ? 'text-green-600' : 'text-red-600'" role="alert">
            <svg v-if="pwSuccess" class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ pwMsg }}
          </div>

          <div class="flex justify-end">
            <button type="submit" class="btn-primary" :disabled="pwLoading">
              {{ pwLoading ? 'Modification…' : 'Modifier le mot de passe' }}
            </button>
          </div>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { authApi } from '@/api/auth.js'
import { useHead } from '@unhead/vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'

useHead({
  title: 'Mon profil | Zsdevweb',
  meta: [{ name: 'robots', content: 'noindex, nofollow' }],
})

const authStore = useAuthStore()

// --- Profil ---
const profile = reactive({ first_name: '', last_name: '', phone: '', company: '' })
const profileLoading = ref(false)
const profileMsg     = ref('')
const profileSuccess = ref(false)

onMounted(() => {
  const u = authStore.user
  if (u) {
    profile.first_name = u.first_name || ''
    profile.last_name  = u.last_name  || ''
    profile.phone      = u.phone      || ''
    profile.company    = u.company    || ''
  }
})

async function saveProfile() {
  profileLoading.value = true
  profileMsg.value = ''
  try {
    const { data } = await authApi.updateMe(profile)
    authStore.updateUser(data)
    profileSuccess.value = true
    profileMsg.value = 'Profil mis à jour.'
  } catch {
    profileSuccess.value = false
    profileMsg.value = 'Erreur lors de la mise à jour.'
  } finally {
    profileLoading.value = false
  }
}

// --- Mot de passe ---
const pwForm = reactive({ current: '', newPw: '', confirm: '' })
const pwLoading = ref(false)
const pwMsg     = ref('')
const pwSuccess = ref(false)

async function changePassword() {
  pwMsg.value = ''
  if (pwForm.newPw !== pwForm.confirm) {
    pwSuccess.value = false
    pwMsg.value = 'Les mots de passe ne correspondent pas.'
    return
  }
  pwLoading.value = true
  try {
    await authApi.changePassword({ current_password: pwForm.current, new_password: pwForm.newPw })
    pwSuccess.value = true
    pwMsg.value = 'Mot de passe modifié avec succès.'
    pwForm.current = ''
    pwForm.newPw   = ''
    pwForm.confirm = ''
  } catch (e) {
    pwSuccess.value = false
    const data = e.response?.data
    pwMsg.value = data?.current_password?.[0] || data?.new_password?.[0] || data?.detail || 'Erreur lors de la modification.'
  } finally {
    pwLoading.value = false
  }
}
</script>
