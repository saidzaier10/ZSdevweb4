<template>
  <div>
    <!-- Header -->
    <section class="bg-gradient-to-br from-gray-900 to-primary-950 text-white py-20 px-4">
      <div class="max-w-4xl mx-auto">
        <Breadcrumb :items="breadcrumbs" class="mb-8" />
        <div v-if="loading" class="animate-pulse">
          <div class="h-10 bg-gray-700 rounded w-2/3 mb-4"></div>
          <div class="h-6 bg-gray-700 rounded w-1/2"></div>
        </div>
        <div v-else-if="project">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">{{ project.title }}</h1>
          <p v-if="project.tagline" class="text-gray-300 text-lg">{{ project.tagline }}</p>
        </div>
      </div>
    </section>

    <!-- Content -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Loading -->
        <div v-if="loading" class="space-y-8">
          <SkeletonLoader class="h-80 rounded-2xl" />
          <SkeletonLoader class="h-40 rounded-xl" />
        </div>

        <!-- Error -->
        <div v-else-if="error" class="text-center py-20">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.268 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Projet non trouvé</h2>
          <p class="text-gray-500 mb-6">Ce projet n'existe pas ou a été retiré.</p>
          <RouterLink to="/portfolio" class="btn-primary text-sm">← Retour au portfolio</RouterLink>
        </div>

        <!-- Project detail -->
        <div v-else-if="project" class="space-y-12">
          <!-- Image principale -->
          <div class="rounded-2xl overflow-hidden bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-700">
            <picture v-if="project.image">
              <source v-if="project.image_webp" :srcset="project.image_webp" type="image/webp" />
              <img
                :src="project.image"
                :alt="`Capture d'écran du projet ${project.title}`"
                class="w-full h-auto object-cover"
                loading="lazy"
                width="1200"
                height="675"
              />
            </picture>
            <div v-else class="aspect-video flex items-center justify-center">
              <span class="text-6xl">💻</span>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
            <!-- Description -->
            <div class="lg:col-span-2 space-y-6">
              <div>
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">À propos du projet</h2>
                <div class="prose prose-gray dark:prose-invert max-w-none text-gray-600 dark:text-gray-300 leading-relaxed">
                  {{ project.description }}
                </div>
              </div>

              <!-- Image secondaire -->
              <div v-if="project.image_secondary" class="rounded-xl overflow-hidden">
                <picture>
                  <source v-if="project.image_secondary_webp" :srcset="project.image_secondary_webp" type="image/webp" />
                  <img
                    :src="project.image_secondary"
                    :alt="`Vue supplémentaire du projet ${project.title}`"
                    class="w-full h-auto object-cover"
                    loading="lazy"
                  />
                </picture>
              </div>
            </div>

            <!-- Sidebar infos -->
            <div class="space-y-6">
              <!-- Stack technique -->
              <div class="card">
                <h3 class="font-bold text-gray-900 dark:text-white text-sm uppercase tracking-wider mb-3">Stack technique</h3>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="tech in (project.tech_stack || [])"
                    :key="tech"
                    class="text-xs bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 px-3 py-1.5 rounded-lg font-medium"
                  >
                    {{ tech }}
                  </span>
                </div>
              </div>

              <!-- Client -->
              <div v-if="project.client_name" class="card">
                <h3 class="font-bold text-gray-900 dark:text-white text-sm uppercase tracking-wider mb-3">Client</h3>
                <p class="text-gray-600 dark:text-gray-300">{{ project.client_name }}</p>
              </div>

              <!-- Liens -->
              <div class="card space-y-3">
                <h3 class="font-bold text-gray-900 dark:text-white text-sm uppercase tracking-wider mb-3">Liens</h3>
                <a
                  v-if="project.url"
                  :href="project.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="flex items-center gap-2 text-primary-600 dark:text-primary-400 hover:underline text-sm font-medium"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Voir le site en ligne
                </a>
                <a
                  v-if="project.github_url"
                  :href="project.github_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white text-sm font-medium"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                  </svg>
                  Code source GitHub
                </a>
                <p v-if="!project.url && !project.github_url" class="text-gray-400 dark:text-gray-500 text-sm italic">
                  Projet confidentiel
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-primary-600 text-white text-center px-4">
      <h2 class="text-2xl font-bold mb-4">Un projet similaire en tête ?</h2>
      <p class="text-primary-100 mb-8 max-w-lg mx-auto">Discutons de votre projet et obtenez un devis personnalisé sous 24h.</p>
      <RouterLink to="/devis" class="bg-white text-primary-600 font-semibold px-8 py-4 rounded-xl hover:bg-gray-50 transition-colors inline-flex">
        Démarrer mon projet →
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { portfolioApi } from '@/api/portfolio.js'
import Breadcrumb from '@/components/ui/Breadcrumb.vue'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'
import { useHead } from '@unhead/vue'

const route = useRoute()
const project = ref(null)
const loading = ref(true)
const error = ref(false)

const breadcrumbs = computed(() => [
  { label: 'Accueil', to: '/' },
  { label: 'Portfolio', to: '/portfolio' },
  ...(project.value ? [{ label: project.value.title }] : []),
])

onMounted(async () => {
  try {
    const { data } = await portfolioApi.getProject(route.params.slug)
    project.value = data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})

// SEO dynamique basé sur le projet chargé
useHead(computed(() => {
  if (!project.value) {
    return {
      title: 'Projet — Portfolio | Zsdevweb',
    }
  }
  const p = project.value
  const techList = (p.tech_stack || []).join(', ')
  return {
    title: `${p.title} — Réalisation Web | Zsdevweb`,
    meta: [
      {
        name: 'description',
        content: p.tagline || `Découvrez le projet ${p.title}${p.client_name ? ` réalisé pour ${p.client_name}` : ''}. Technologies : ${techList}. Développement web sur-mesure à Mouvaux / Lille.`,
      },
      { property: 'og:title', content: `${p.title} — Portfolio Zsdevweb` },
      { property: 'og:description', content: p.tagline || p.description?.substring(0, 160) },
      { property: 'og:type', content: 'article' },
      { property: 'og:url', content: `https://zsdevweb.fr/portfolio/${route.params.slug}` },
      ...(p.image ? [{ property: 'og:image', content: p.image }] : []),
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
    link: [
      { rel: 'canonical', href: `https://zsdevweb.fr/portfolio/${route.params.slug}` },
    ],
  }
}))
</script>
