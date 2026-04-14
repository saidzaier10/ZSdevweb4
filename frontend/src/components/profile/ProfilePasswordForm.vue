<template>
  <div class="card">
    <h2 class="font-bold text-gray-900 dark:text-white mb-5">Changer le mot de passe</h2>

    <form @submit.prevent="change" class="space-y-4">
      <PasswordInput v-model="form.current" label="Mot de passe actuel" required autocomplete="current-password" />
      <PasswordInput v-model="form.newPw"   label="Nouveau mot de passe" required minlength="8" autocomplete="new-password" placeholder="8 caractères minimum" />
      <PasswordInput v-model="form.confirm" label="Confirmer"            required minlength="8" autocomplete="new-password" />

      <div v-if="msg" class="flex items-center gap-2 text-sm" :class="success ? 'text-green-600' : 'text-red-600'" role="alert">
        <svg v-if="success" class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ msg }}
      </div>

      <div class="flex justify-end">
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Modification…' : 'Modifier le mot de passe' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { authApi } from '@/api/auth.js'
import PasswordInput from '@/components/ui/PasswordInput.vue'

const form    = reactive({ current: '', newPw: '', confirm: '' })
const loading = ref(false)
const msg     = ref('')
const success = ref(false)

async function change() {
  msg.value = ''
  if (form.newPw !== form.confirm) {
    success.value = false
    msg.value = 'Les mots de passe ne correspondent pas.'
    return
  }
  loading.value = true
  try {
    await authApi.changePassword({ current_password: form.current, new_password: form.newPw })
    success.value = true
    msg.value = 'Mot de passe modifié avec succès.'
    form.current = form.newPw = form.confirm = ''
  } catch (e) {
    success.value = false
    const d = e.response?.data
    msg.value = d?.current_password?.[0] || d?.new_password?.[0] || d?.detail || 'Erreur lors de la modification.'
  } finally {
    loading.value = false
  }
}
</script>
