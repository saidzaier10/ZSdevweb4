<template>
  <section class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="section-title">Comment ça marche ?</h2>
        <p class="section-subtitle mx-auto">Un processus simple et transparent, de la demande à la livraison.</p>
      </div>

      <div class="relative">
        <!-- Ligne de connexion desktop -->
        <div class="hidden lg:block absolute top-8 left-1/2 -translate-x-1/2 w-3/4 h-0.5 bg-gray-200" />

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div v-for="(step, idx) in steps" :key="step.title" class="relative text-center">
            <div class="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-white font-bold text-xl">{{ idx + 1 }}</span>
            </div>
            <h3 class="font-bold text-gray-900 mb-2">{{ step.title }}</h3>
            <p class="text-gray-500 text-sm">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  { title: 'Devis en ligne', description: 'Remplissez le formulaire en 5 minutes. Recevez un devis personnalisé sous 24h.' },
  { title: 'Validation', description: 'On discute de votre projet, j\'affine le devis selon vos besoins.' },
  { title: 'Développement', description: 'Je code votre projet avec des points d\'avancement réguliers.' },
  { title: 'Livraison', description: 'Mise en ligne, tests complets, formation et support inclus.' },
]
</script>
