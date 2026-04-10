import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Sitemap from 'vite-plugin-sitemap'
import WebfontDownload from 'vite-plugin-webfont-dl'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/composables/**', 'src/stores/**'],
    },
  },
  plugins: [
    vue(),
    Sitemap({ hostname: 'https://zsdevweb.fr' }),
    // Télécharge les Google Fonts au build et les sert en local → plus de dépendance CDN
    WebfontDownload(),
  ],
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
