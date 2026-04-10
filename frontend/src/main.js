import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@unhead/vue/client'
import * as Sentry from '@sentry/vue'
import App from './App.vue'
import router from './router/index.js'
import './assets/main.css'

const app = createApp(App)
const head = createHead()

// Sentry — activé uniquement si VITE_SENTRY_DSN est défini
const sentryDsn = import.meta.env.VITE_SENTRY_DSN
if (sentryDsn) {
  Sentry.init({
    app,
    dsn: sentryDsn,
    integrations: [
      Sentry.browserTracingIntegration({ router }),
    ],
    tracesSampleRate: 0.1,
    environment: import.meta.env.MODE,
    ignoreErrors: [
      // Erreurs réseau normales (offline, annulation)
      'Network Error',
      'Request aborted',
      /^ResizeObserver loop/,
    ],
  })
}

app.use(createPinia())
app.use(router)
app.use(head)

// Restauration silencieuse de session via cookie refresh_token HttpOnly
import('@/stores/auth.js').then(({ useAuthStore }) => {
  useAuthStore().tryRestoreSession()
})

// Gestionnaire d'erreurs global — capture les erreurs non gérées dans les composants
app.config.errorHandler = (err, instance, info) => {
  console.error('[Zsdevweb] Erreur globale :', err)
  console.error('[Zsdevweb] Composant :', instance?.$options?.name || 'Anonyme')
  console.error('[Zsdevweb] Info :', info)
  if (sentryDsn) {
    Sentry.captureException(err, { extra: { info, component: instance?.$options?.name } })
  }
}

app.mount('#app')
