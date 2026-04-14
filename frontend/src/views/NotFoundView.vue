<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4">
    <div class="text-center max-w-lg">
      <div class="mb-8">
        <span class="text-8xl font-display font-bold bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
          404
        </span>
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
        Page introuvable
      </h1>
      <p class="text-gray-600 dark:text-gray-400 mb-8">
        La page que vous recherchez n'existe pas ou a été déplacée.
      </p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <RouterLink to="/" class="btn-primary text-sm justify-center">
          ← Retour à l'accueil
        </RouterLink>
        <RouterLink to="/contact" class="btn-ghost text-sm justify-center">
          Contactez-moi
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useHead } from '@unhead/vue'

useHead({
  title: 'Page introuvable — Zsdevweb',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' },
  ],
})
</script>
