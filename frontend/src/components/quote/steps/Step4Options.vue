<template>
  <div class="animate-fade-in">
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Options supplémentaires</h2>
    <p class="text-gray-500 mb-8">Enrichissez votre projet avec ces fonctionnalités (toutes facultatives).</p>

    <div class="grid grid-cols-1 gap-3">
      <button
        v-for="option in catalogStore.supplementaryOptions"
        :key="option.id"
        @click="quoteStore.toggleOption(option.id)"
        :class="[
          'p-4 rounded-xl border-2 text-left transition-all duration-200',
          isSelected(option.id)
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-200 hover:border-gray-300'
        ]"
      >
        <div class="flex items-center gap-4">
          <div :class="[
            'w-6 h-6 rounded-md flex items-center justify-center flex-shrink-0 border-2 transition-colors',
            isSelected(option.id) ? 'bg-primary-600 border-primary-600' : 'border-gray-300'
          ]" aria-hidden="true">
            <svg v-if="isSelected(option.id)" class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="flex-1">
            <div class="font-semibold text-gray-900 text-sm">{{ option.name }}</div>
            <div class="text-gray-500 text-xs mt-0.5">{{ option.description }}</div>
          </div>
          <div class="text-right flex-shrink-0">
            <span class="font-bold text-sm text-primary-600">
              +{{ formatPrice(option.price) }}
            </span>
            <span v-if="option.is_recurring" class="text-xs text-gray-400 block">/mois</span>
          </div>
        </div>
      </button>
    </div>

    <p class="text-sm text-gray-400 mt-4 text-center">Vous pouvez passer cette étape si vous n'avez pas de besoins spécifiques.</p>
  </div>
</template>

<script setup>
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'
import { formatPrice } from '@/utils/formatters.js'

defineEmits(['next'])
const quoteStore = useQuoteStore()
const catalogStore = useCatalogStore()

function isSelected(id) {
  return quoteStore.formData.optionIds.includes(id)
}
</script>
