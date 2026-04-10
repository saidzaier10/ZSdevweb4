import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 15000,
  withCredentials: true, // Envoie le cookie refresh_token HttpOnly automatiquement
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

/**
 * Accesseurs injectés par le store auth après initialisation de Pinia.
 * Pattern callback pour éviter la dépendance circulaire store ↔ axios.
 */
let _getAccessToken = () => null
let _setAccessToken = () => {}
let _handleLogout = () => {}

export function registerAuthCallbacks({ getAccessToken, setAccessToken, onLogout }) {
  _getAccessToken = getAccessToken
  _setAccessToken = setAccessToken
  _handleLogout = onLogout
}

// Request interceptor — injecte l'access token depuis la mémoire Pinia
instance.interceptors.request.use(
  (config) => {
    const token = _getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — refresh JWT automatique via cookie HttpOnly
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  failedQueue = []
}

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      // Éviter la boucle infinie sur l'endpoint de refresh
      if (originalRequest.url?.includes('/auth/token/refresh/')) {
        _handleLogout()
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return instance(originalRequest)
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // Pas de body — le cookie refresh_token est envoyé automatiquement
        const { data } = await instance.post('/api/v1/auth/token/refresh/')
        const newToken = data.access

        // Met à jour le store Pinia via le callback enregistré
        _setAccessToken(newToken)

        instance.defaults.headers.common.Authorization = `Bearer ${newToken}`
        processQueue(null, newToken)
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return instance(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        _handleLogout()
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default instance
