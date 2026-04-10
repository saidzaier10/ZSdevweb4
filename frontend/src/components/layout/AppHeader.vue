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

        <!-- CTAs + Dark toggle -->
        <div class="hidden md:flex items-center gap-3">
          <!-- Toggle dark mode -->
          <button
            @click="toggleTheme"
            class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :aria-label="isDark ? 'Passer en mode clair' : 'Passer en mode sombre'"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <RouterLink to="/audit-gratuit" class="btn-ghost text-sm">Audit gratuit</RouterLink>
          <RouterLink to="/devis" class="btn-primary text-sm py-2">Obtenir un devis</RouterLink>
        </div>

        <!-- Mobile: dark toggle + burger -->
        <div class="md:hidden flex items-center gap-2">
          <button
            @click="toggleTheme"
            class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :aria-label="isDark ? 'Mode clair' : 'Mode sombre'"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

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
              <RouterLink to="/audit-gratuit" class="btn-secondary text-sm justify-center">Audit gratuit</RouterLink>
              <RouterLink to="/devis" class="btn-primary text-sm justify-center">Obtenir un devis</RouterLink>
            </div>
          </div>
        </div>
      </Transition>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui.js'
import { useTheme } from '@/composables/useTheme.js'

const uiStore = useUIStore()
const router = useRouter()
const { isDark, toggle: toggleTheme } = useTheme()

router.afterEach(() => uiStore.closeMobileMenu())

const navLinks = [
  { to: '/services', label: 'Services' },
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/a-propos', label: 'À propos' },
  { to: '/contact', label: 'Contact' },
]
</script>
