import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth.js'
import { registerAuthCallbacks } from '@/api/axios.js'
import { clearApiCache } from '@/composables/useApiCache.js'

export const useAuthStore = defineStore('auth', () => {
  // access_token uniquement en mémoire (jamais dans localStorage)
  // refresh_token dans cookie HttpOnly côté serveur
  const accessToken = ref(null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  // Expose les callbacks à axios pour éviter la dépendance circulaire
  registerAuthCallbacks({
    getAccessToken: () => accessToken.value,
    setAccessToken: (token) => { accessToken.value = token },
    onLogout: logout,
  })

  async function login(email, password) {
    const { data } = await authApi.login(email, password)
    accessToken.value = data.access
    // data.refresh n'existe plus — il est dans le cookie HttpOnly
    await fetchMe()
  }

  async function fetchMe() {
    try {
      const { data } = await authApi.me()
      user.value = data
    } catch {
      logout()
    }
  }

  function setAccessToken(token) {
    accessToken.value = token
  }

  function updateUser(patch) {
    if (user.value) {
      user.value = { ...user.value, ...patch }
    }
  }

  function logout() {
    accessToken.value = null
    user.value = null
    clearApiCache()
    // Demande au backend de supprimer le cookie refresh_token
    authApi.logout().catch(() => {})
  }

  // Au démarrage de l'app, tenter un refresh silencieux pour restaurer la session
  // si un cookie refresh_token valide existe (ex : retour sur l'app après fermeture)
  async function tryRestoreSession() {
    if (accessToken.value) return
    try {
      const { data } = await authApi.refresh()
      accessToken.value = data.access
      await fetchMe()
    } catch {
      // Pas de session active — état anonyme, rien à faire
    }
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    login,
    fetchMe,
    logout,
    setAccessToken,
    updateUser,
    tryRestoreSession,
  }
})
