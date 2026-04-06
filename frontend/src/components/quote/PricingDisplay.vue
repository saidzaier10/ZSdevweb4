<template>
  <div class="sticky top-24">
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <svg class="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 19h16a2 2 0 002-2V7a2 2 0 00-2-2H4a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        Estimation en direct
      </h3>

      <div v-if="loading" class="flex justify-center py-6">
        <LoadingSpinner />
      </div>

      <div v-else-if="pricing" class="space-y-3">
        <!-- Lignes de détail -->
        <div class="space-y-2 text-sm">
          <div class="flex justify-between text-gray-600">
            <span>Prix de base</span>
            <span>{{ format(pricing.base_price) }}</span>
          </div>
          <div v-if="pricing.design_supplement > 0" class="flex justify-between text-gray-600">
            <span>Design</span>
            <span>+{{ format(pricing.design_supplement) }}</span>
          </div>
          <div v-if="pricing.complexity_factor > 1" class="flex justify-between text-gray-600">
            <span>Complexité ×{{ pricing.complexity_factor }}</span>
            <span class="text-orange-600">×{{ pricing.complexity_factor }}</span>
          </div>
          <div v-if="pricing.options_total > 0" class="flex justify-between text-gray-600">
            <span>Options</span>
            <span>+{{ format(pricing.options_total) }}</span>
          </div>
        </div>

        <div class="border-t border-gray-100 pt-3 space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">Sous-total HT</span>
            <span class="font-medium">{{ format(pricing.subtotal_ht) }}</span>
          </div>
          <div class="flex justify-between text-sm text-gray-500">
            <span>TVA 20%</span>
            <span>+{{ format(pricing.vat_amount) }}</span>
          </div>
        </div>

        <!-- Total TTC -->
        <div class="bg-primary-50 rounded-xl p-3 mt-2">
          <div class="flex justify-between items-center">
            <span class="font-semibold text-gray-900">Total TTC</span>
            <span class="text-xl font-bold text-primary-600">{{ format(pricing.total_ttc) }}</span>
          </div>
        </div>

        <!-- Plan 3× -->
        <InstallmentPlan :pricing="pricing" compact />
      </div>

      <div v-else-if="!loading" class="text-center py-8 text-gray-400 text-sm">
        <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        Sélectionnez un type de projet pour voir l'estimation
      </div>
    </div>
  </div>
</template>

<script setup>
import { usePricing } from '@/composables/usePricing.js'
import InstallmentPlan from './InstallmentPlan.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const { pricing, loading, formatPrice } = usePricing()

function format(value) {
  return formatPrice(value)
}
</script>
