import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

export function useToast() {
  function show({ message, type = 'info', duration = 4000 }) {
    const id = ++nextId
    toasts.value.push({ id, message, type })
    setTimeout(() => dismiss(id), duration)
  }

  function dismiss(id) {
    const idx = toasts.value.findIndex(t => t.id === id)
    if (idx !== -1) toasts.value.splice(idx, 1)
  }

  return {
    toasts,
    success: (message, duration) => show({ message, type: 'success', duration }),
    error: (message, duration) => show({ message, type: 'error', duration }),
    info: (message, duration) => show({ message, type: 'info', duration }),
    dismiss,
  }
}
