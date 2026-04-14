<template>
  <!-- Visible uniquement sur mobile/tablet, caché sur lg+ (où la sidebar est visible) -->
  <Transition name="slide-up">
    <div
      v-if="quoteStore.formData.projectTypeId"
      class="lg:hidden fixed bottom-0 inset-x-0 z-40 bg-white border-t border-gray-200 shadow-lg"
    >
      <div class="px-4 py-3 flex items-center justify-between gap-4">
        <div class="flex items-center gap-2 min-w-0">
          <svg class="w-4 h-4 text-primary-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 19h16a2 2 0 002-2V7a2 2 0 00-2-2H4a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <span class="text-xs text-gray-500 truncate">Estimation</span>
        </div>

        <div v-if="loading" class="flex items-center gap-2">
          <LoadingSpinner size="sm" />
          <span class="text-xs text-gray-400">Calcul...</span>
        </div>

        <div v-else-if="pricing" class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs text-gray-500">HT</div>
            <div class="text-sm font-semibold text-gray-700">{{ formatPrice(pricing.subtotal_ht) }}</div>
          </div>
          <div class="w-px h-8 bg-gray-200" />
          <div class="text-right">
            <div class="text-xs text-gray-500">TTC</div>
            <div class="text-base font-bold text-primary-600">{{ formatPrice(pricing.total_ttc) }}</div>
          </div>
          <button
            @click="expanded = !expanded"
            class="p-1 text-gray-400 hover:text-gray-600"
            :aria-label="expanded ? 'Masquer le détail' : 'Voir le détail'"
          >
            <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': expanded }" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Détail expandable -->
      <Transition name="expand">
        <div v-if="expanded && pricing" class="px-4 pb-4 space-y-2 border-t border-gray-100 pt-3">
          <div class="flex justify-between text-sm text-gray-600">
            <span>Prix de base</span><span>{{ formatPrice(pricing.base_price) }}</span>
          </div>
          <div v-if="pricing.design_supplement > 0" class="flex justify-between text-sm text-gray-600">
            <span>Design</span><span>+{{ formatPrice(pricing.design_supplement) }}</span>
          </div>
          <div v-if="pricing.complexity_factor > 1" class="flex justify-between text-sm text-gray-600">
            <span>Complexité</span><span class="text-orange-600">×{{ pricing.complexity_factor }}</span>
          </div>
          <div v-if="pricing.options_total > 0" class="flex justify-between text-sm text-gray-600">
            <span>Options</span><span>+{{ formatPrice(pricing.options_total) }}</span>
          </div>
          <div class="border-t border-gray-100 pt-2 flex justify-between text-sm text-gray-500">
            <span>TVA 20%</span><span>+{{ formatPrice(pricing.vat_amount) }}</span>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import { usePricing } from '@/composables/usePricing.js'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const quoteStore = useQuoteStore()
const { pricing, loading, formatPrice } = usePricing()
const expanded = ref(false)
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.25s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}
.expand-enter-to,
.expand-leave-from {
  max-height: 200px;
  opacity: 1;
}
</style>
