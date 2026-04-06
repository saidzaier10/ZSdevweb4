<template>
  <section class="py-20 bg-primary-600">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">
        Prêt à lancer votre projet ?
      </h2>
      <p class="text-primary-100 text-lg mb-8 max-w-2xl mx-auto">
        Obtenez votre devis personnalisé en 5 minutes. Réponse garantie sous 24h.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <RouterLink to="/devis" class="bg-white text-primary-600 font-semibold px-8 py-4 rounded-xl hover:bg-gray-50 transition-colors inline-flex items-center justify-center">
          Obtenir mon devis gratuit →
        </RouterLink>
        <RouterLink to="/audit-gratuit" class="text-white border-2 border-white/50 hover:border-white font-semibold px-8 py-4 rounded-xl transition-colors inline-flex items-center justify-center">
          Demander un audit
        </RouterLink>
      </div>
    </div>
  </section>
</template>
