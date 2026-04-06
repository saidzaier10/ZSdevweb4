<template>
  <header class="sticky top-0 z-50 bg-white/90 backdrop-blur-sm border-b border-gray-100">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 font-display font-bold text-xl text-gray-900">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white text-sm font-bold">ZS</span>
          </div>
          <span>Zsdevweb</span>
        </RouterLink>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
            active-class="text-primary-600 bg-primary-50"
          >
            {{ link.label }}
          </RouterLink>
        </div>

        <!-- CTAs -->
        <div class="hidden md:flex items-center gap-3">
          <RouterLink to="/audit-gratuit" class="btn-ghost text-sm">
            Audit gratuit
          </RouterLink>
          <RouterLink to="/devis" class="btn-primary text-sm py-2">
            Obtenir un devis
          </RouterLink>
        </div>

        <!-- Mobile burger -->
        <button
          @click="uiStore.toggleMobileMenu()"
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Menu"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!uiStore.mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
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
        <div v-if="uiStore.mobileMenuOpen" class="md:hidden py-4 border-t border-gray-100">
          <div class="flex flex-col gap-1">
            <RouterLink
              v-for="link in navLinks"
              :key="link.to"
              :to="link.to"
              @click="uiStore.closeMobileMenu()"
              class="px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
            >
              {{ link.label }}
            </RouterLink>
            <div class="pt-3 flex flex-col gap-2">
              <RouterLink to="/audit-gratuit" @click="uiStore.closeMobileMenu()" class="btn-secondary text-sm justify-center">
                Audit gratuit
              </RouterLink>
              <RouterLink to="/devis" @click="uiStore.closeMobileMenu()" class="btn-primary text-sm justify-center">
                Obtenir un devis
              </RouterLink>
            </div>
          </div>
        </div>
      </Transition>
    </nav>
  </header>
</template>

<script setup>
import { useUIStore } from '@/stores/ui.js'

const uiStore = useUIStore()

const navLinks = [
  { to: '/services', label: 'Services' },
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/a-propos', label: 'À propos' },
  { to: '/contact', label: 'Contact' },
]
</script>
