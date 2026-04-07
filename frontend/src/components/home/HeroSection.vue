<template>
  <section class="relative overflow-hidden bg-gradient-to-br from-gray-900 via-primary-950 to-gray-900 text-white">
    <!-- Background pattern -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.3) 1px, transparent 0); background-size: 40px 40px;" />
    </div>

    <!-- Glow effect -->
    <div class="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-primary-500 rounded-full filter blur-3xl opacity-10" />

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-36">
      <div class="max-w-3xl">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm font-medium mb-8">
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse-slow" />
          Disponible pour de nouveaux projets
        </div>

        <h1 class="text-5xl md:text-6xl font-display font-bold leading-tight mb-6">
          Je conçois des sites web qui
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-accent-400">
            digitalisent les TPE/PME
          </span>
        </h1>

        <p class="text-gray-300 text-xl leading-relaxed mb-10 max-w-2xl">
          Développeur web freelance basé à Mouvaux. J'accompagne les entreprises
          de la métropole lilloise (Hem, Roubaix, Tourcoing) avec des sites web modernes et orientés résultat.
        </p>

        <!-- Stats rapides -->
        <div class="flex flex-wrap gap-8 mb-10">
          <div v-for="stat in stats" :key="stat.label">
            <div class="text-3xl font-bold text-white">{{ stat.value }}</div>
            <div class="text-gray-400 text-sm">{{ stat.label }}</div>
          </div>
        </div>

        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row gap-4">
          <RouterLink to="/devis" class="btn-primary text-base py-4 px-8">
            Obtenir un devis gratuit →
          </RouterLink>
          <RouterLink to="/portfolio" class="inline-flex items-center gap-2 text-white border border-white/30 hover:border-white/60 px-8 py-4 rounded-xl transition-all font-medium">
            Voir mes réalisations
          </RouterLink>
        </div>

        <!-- Social proof -->
        <div class="mt-10 flex items-center gap-3">
          <div class="flex -space-x-2">
            <div
              v-for="i in 4"
              :key="i"
              class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-accent-500 border-2 border-gray-900"
            />
          </div>
          <div class="text-sm text-gray-400">
            <span class="text-white font-semibold">+30 clients</span> font confiance à Zsdevweb
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom wave -->
    <div class="absolute bottom-0 left-0 right-0">
      <svg viewBox="0 0 1440 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 60L1440 60L1440 0C1440 0 1080 60 720 60C360 60 0 0 0 0V60Z" fill="white"/>
      </svg>
    </div>
  </section>
</template>

<script setup>
const stats = [
  { value: '30+', label: 'projets livrés' },
  { value: '100%', label: 'clients satisfaits' },
  { value: '5 ans', label: "d'expérience" },
]
</script>
