import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        // En Docker, le backend est accessible via le nom du service, pas localhost
        target: process.env.VITE_BACKEND_INTERNAL_URL || 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
})
