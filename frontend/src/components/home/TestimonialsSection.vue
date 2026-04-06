<template>
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="section-title">Ce que disent mes clients</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="t in testimonials" :key="t.name" class="card">
          <div class="flex gap-1 mb-4">
            <svg v-for="i in 5" :key="i" class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
          <p class="text-gray-600 text-sm leading-relaxed mb-4">"{{ t.content }}"</p>
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
              <span class="text-primary-700 font-bold text-sm">{{ t.name[0] }}</span>
            </div>
            <div>
              <div class="font-semibold text-gray-900 text-sm">{{ t.name }}</div>
              <div class="text-gray-500 text-xs">{{ t.company }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const testimonials = [
  { name: 'Marie L.', company: 'Boutique Bio Paris', content: 'Site e-commerce livré en 5 semaines, exactement comme prévu. Les ventes ont augmenté de 40% dès le premier mois.' },
  { name: 'Thomas R.', company: 'Cabinet RH Conseil', content: 'Excellent travail sur notre application de gestion. Interface intuitive, code propre et accompagnement professionnel.' },
  { name: 'Sophie M.', company: 'Agence immobilière', content: 'Refonte complète de notre site. Résultat bluffant, trafic doublé en 3 mois. Je recommande sans hésiter.' },
]
</script>
