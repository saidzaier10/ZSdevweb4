<template>
  <div id="app">
    <AppHeader />
    <main>
      <RouterView />
    </main>
    <AppFooter />
    <ToastContainer />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ToastContainer from '@/components/ui/ToastContainer.vue'
</script>
