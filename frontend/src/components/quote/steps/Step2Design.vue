<template>
  <div class="animate-fade-in">
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Quel niveau de design ?</h2>
    <p class="text-gray-500 mb-8">Le design impacte directement l'image de votre entreprise et les conversions.</p>

    <div class="grid grid-cols-1 gap-4">
      <button
        v-for="option in catalogStore.designOptions"
        :key="option.id"
        @click="quoteStore.updateFormData({ designOptionId: option.id })"
        :class="[
          'p-5 rounded-xl border-2 text-left transition-all duration-200',
          quoteStore.formData.designOptionId === option.id
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-200 hover:border-gray-300'
        ]"
      >
        <div class="flex items-center justify-between">
          <div>
            <div class="font-semibold text-gray-900">{{ option.name }}</div>
            <div class="text-gray-500 text-sm mt-1">{{ option.description }}</div>
          </div>
          <div class="text-right ml-4 flex-shrink-0">
            <span v-if="parseFloat(option.price_supplement) === 0" class="text-green-600 font-bold">Inclus</span>
            <span v-else class="text-primary-600 font-bold">+{{ formatPrice(option.price_supplement) }}</span>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'
import { formatPrice } from '@/utils/formatters.js'

defineEmits(['next'])

const quoteStore = useQuoteStore()
const catalogStore = useCatalogStore()
</script>
