<template>
  <div class="animate-fade-in">
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Niveau de complexité</h2>
    <p class="text-gray-500 mb-8">Estimez le niveau de fonctionnalités dont vous avez besoin.</p>

    <div class="grid grid-cols-1 gap-4">
      <button
        v-for="level in catalogStore.complexityLevels"
        :key="level.id"
        @click="quoteStore.updateFormData({ complexityId: level.id })"
        :class="[
          'p-5 rounded-xl border-2 text-left transition-all duration-200',
          quoteStore.formData.complexityId === level.id
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-200 hover:border-gray-300'
        ]"
      >
        <div class="flex items-center justify-between">
          <div>
            <div class="font-semibold text-gray-900">{{ level.name }}</div>
            <div class="text-gray-500 text-sm mt-1">{{ level.description }}</div>
          </div>
          <div class="text-right ml-4">
            <span class="text-sm font-semibold text-gray-600">×{{ level.multiplier }}</span>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'

defineEmits(['next'])
const quoteStore = useQuoteStore()
const catalogStore = useCatalogStore()
</script>
