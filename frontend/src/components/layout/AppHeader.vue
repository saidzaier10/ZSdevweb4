<template>
  <header class="sticky top-0 z-50 bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm border-b border-gray-100 dark:border-gray-800">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 font-display font-bold text-xl text-gray-900 dark:text-white">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white text-sm font-bold">ZS</span>
          </div>
          <span>Zsdevweb</span>
        </RouterLink>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-1" role="navigation" aria-label="Navigation principale">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors"
            active-class="text-primary-600 bg-primary-50 dark:bg-primary-900/30"
          >
            {{ link.label }}
          </RouterLink>
        </div>

        <!-- Desktop : actions -->
        <div class="hidden md:flex items-center gap-3">
          <DarkModeToggle :is-dark="isDark" @toggle="toggleTheme" />

          <UserMenuDropdown
            v-if="authStore.isAuthenticated"
            ref="userMenuRef"
            :user="authStore.user"
            @logout="handleLogout"
          />
          <template v-else>
            <RouterLink to="/connexion" class="btn-ghost text-sm">Connexion</RouterLink>
            <RouterLink to="/audit-gratuit" class="btn-ghost text-sm">Audit gratuit</RouterLink>
            <RouterLink to="/devis" class="btn-primary text-sm py-2">Obtenir un devis</RouterLink>
          </template>
        </div>

        <!-- Mobile : dark toggle + burger -->
        <div class="md:hidden flex items-center gap-2">
          <DarkModeToggle :is-dark="isDark" @toggle="toggleTheme" :compact="true" />
          <button
            @click="uiStore.toggleMobileMenu()"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :aria-label="uiStore.mobileMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
            :aria-expanded="uiStore.mobileMenuOpen"
            aria-controls="mobile-menu"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path v-if="!uiStore.mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div v-if="uiStore.mobileMenuOpen" id="mobile-menu" class="md:hidden py-4 border-t border-gray-100 dark:border-gray-800" role="navigation" aria-label="Menu mobile">
          <div class="flex flex-col gap-1">
            <RouterLink
              v-for="link in navLinks"
              :key="link.to"
              :to="link.to"
              class="px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              {{ link.label }}
            </RouterLink>

            <div class="pt-3 flex flex-col gap-2">
              <template v-if="authStore.isAuthenticated">
                <div class="px-4 py-2 border border-gray-100 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                  <p class="text-xs text-gray-500">Connecté</p>
                  <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ authStore.user?.email }}</p>
                </div>
                <RouterLink v-if="authStore.user?.is_staff" to="/tableau-de-bord" class="btn-secondary text-sm justify-center text-primary-600">Tableau de bord</RouterLink>
                <RouterLink to="/espace-client" class="btn-secondary text-sm justify-center">Mes projets</RouterLink>
                <RouterLink to="/espace-client/profil" class="btn-ghost text-sm justify-center">Mon profil</RouterLink>
                <button @click="handleLogout" class="btn-ghost text-sm justify-center text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20">
                  Se déconnecter
                </button>
              </template>
              <template v-else>
                <RouterLink to="/connexion" class="btn-secondary text-sm justify-center">Connexion</RouterLink>
                <RouterLink to="/inscription" class="btn-ghost text-sm justify-center">Créer un compte</RouterLink>
                <RouterLink to="/audit-gratuit" class="btn-ghost text-sm justify-center">Audit gratuit</RouterLink>
                <RouterLink to="/devis" class="btn-primary text-sm justify-center">Obtenir un devis</RouterLink>
              </template>
            </div>
          </div>
        </div>
      </Transition>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui.js'
import { useAuthStore } from '@/stores/auth.js'
import { useTheme } from '@/composables/useTheme.js'
import UserMenuDropdown from './UserMenuDropdown.vue'
import DarkModeToggle from './DarkModeToggle.vue'

const uiStore = useUIStore()
const authStore = useAuthStore()
const router = useRouter()
const { isDark, toggle: toggleTheme } = useTheme()
const userMenuRef = ref(null)

router.afterEach(() => {
  uiStore.closeMobileMenu()
  userMenuRef.value?.close()
})

async function handleLogout() {
  authStore.logout()
  router.push('/')
}

const navLinks = [
  { to: '/services', label: 'Services' },
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/a-propos', label: 'À propos' },
  { to: '/contact', label: 'Contact' },
]
</script>
