<template>
  <div :class="compact ? 'mt-2' : 'card mt-6'">
    <h4 :class="compact ? 'text-xs font-semibold text-gray-600 mb-2' : 'font-semibold text-gray-900 mb-4'">
      Paiement en 3 fois
    </h4>
    <div class="space-y-2">
      <div
        v-for="(installment, idx) in installments"
        :key="idx"
        class="flex items-center justify-between"
        :class="compact ? 'text-xs' : 'text-sm'"
      >
        <div class="flex items-center gap-2">
          <div class="w-5 h-5 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xs font-bold flex-shrink-0">
            {{ idx + 1 }}
          </div>
          <span class="text-gray-600">{{ installment.label }}</span>
        </div>
        <span class="font-semibold text-gray-900">{{ formatPrice(installment.amount) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatPrice } from '@/utils/formatters.js'

const props = defineProps({
  pricing: { type: Object, required: true },
  compact: { type: Boolean, default: false },
})

const installments = computed(() => [
  { label: 'Acompte à la signature (30%)', amount: props.pricing.installment_1 },
  { label: 'Mi-projet (40%)', amount: props.pricing.installment_2 },
  { label: 'Livraison (30%)', amount: props.pricing.installment_3 },
])

</script>
