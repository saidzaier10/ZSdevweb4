import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const mobileMenuOpen = ref(false)
  const toast = ref(null)

  function showToast(message, type = 'success', duration = 4000) {
    toast.value = { message, type, id: Date.now() }
    setTimeout(() => {
      toast.value = null
    }, duration)
  }

  function toggleMobileMenu() {
    mobileMenuOpen.value = !mobileMenuOpen.value
  }

  function closeMobileMenu() {
    mobileMenuOpen.value = false
  }

  return { mobileMenuOpen, toast, showToast, toggleMobileMenu, closeMobileMenu }
})
