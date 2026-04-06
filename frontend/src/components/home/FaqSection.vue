<template>
  <section class="py-20 bg-white">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="section-title">Questions fréquentes</h2>
      </div>
      <div class="space-y-4">
        <div
          v-for="(item, idx) in faqs"
          :key="idx"
          class="border border-gray-200 rounded-xl overflow-hidden"
        >
          <button
            @click="toggle(idx)"
            class="w-full flex items-center justify-between p-5 text-left hover:bg-gray-50 transition-colors"
          >
            <span class="font-medium text-gray-900">{{ item.q }}</span>
            <svg :class="['w-5 h-5 text-gray-400 transition-transform', open === idx ? 'rotate-180' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-if="open === idx" class="px-5 pb-5 text-gray-600 text-sm leading-relaxed">
            {{ item.a }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const open = ref(null)

function toggle(idx) {
  open.value = open.value === idx ? null : idx
}

const faqs = [
  { q: 'Quel est le délai pour un projet ?', a: 'Un site vitrine est livré en 2 à 4 semaines. Un e-commerce en 4 à 8 semaines. Une application web en 6 à 16 semaines selon la complexité.' },
  { q: 'Comment se déroule le paiement ?', a: '30% à la signature du devis, 40% à mi-projet, 30% à la livraison. Paiement par virement ou carte bancaire.' },
  { q: 'Proposez-vous un suivi après livraison ?', a: 'Oui, une période de garantie de 30 jours est incluse. Des contrats de maintenance mensuelle sont disponibles à partir de 150€/mois.' },
  { q: 'Puis-je modifier le devis après signature ?', a: 'Des modifications mineures sont incluses. Pour des évolutions majeures, un avenant est établi en accord avec vous.' },
  { q: 'Travaillez-vous à distance ?', a: 'Oui, je travaille en 100% remote avec des clients dans toute la France et à l\'international. Des visioconférences régulières assurent le suivi.' },
]
</script>
