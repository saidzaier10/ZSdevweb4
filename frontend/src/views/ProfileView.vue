<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
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
      <ProfileInfoForm />
      <ProfilePasswordForm />
    </div>
  </div>
</template>

<script setup>
import { useHead } from '@unhead/vue'
import ProfileInfoForm from '@/components/profile/ProfileInfoForm.vue'
import ProfilePasswordForm from '@/components/profile/ProfilePasswordForm.vue'

useHead({
  title: 'Mon profil | Zsdevweb',
  meta: [{ name: 'robots', content: 'noindex, nofollow' }],
})
</script>
