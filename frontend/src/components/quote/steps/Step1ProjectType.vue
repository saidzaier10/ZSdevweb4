<template>
  <div class="animate-fade-in">
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Quel type de projet ?</h2>
    <p class="text-gray-600 mb-8">Sélectionnez la catégorie qui correspond le mieux à votre besoin.</p>

    <div v-if="catalogStore.loading" class="flex justify-center py-12">
      <LoadingSpinner />
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="category in catalogStore.categories"
        :key="category.id"
        class="space-y-3"
      >
        <h3 class="text-sm font-semibold text-gray-600 uppercase tracking-wide">
          {{ category.name }}
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button
            v-for="type in category.project_types"
            :key="type.id"
            @click="selectType(type)"
            :class="[
              'p-4 rounded-xl border-2 text-left transition-all duration-200',
              quoteStore.formData.projectTypeId === type.id
                ? 'border-primary-500 bg-primary-50 shadow-sm'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            ]"
          >
            <div class="font-semibold text-gray-900 text-sm">{{ type.name }}</div>
            <div class="text-gray-600 text-xs mt-1">{{ type.description }}</div>
            <div class="mt-3 flex items-center justify-between">
              <span class="text-primary-600 font-bold text-sm">
                À partir de {{ formatPrice(type.base_price) }}
              </span>
              <span class="text-gray-500 text-xs">{{ type.min_days }}–{{ type.max_days }}j</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { formatPrice } from '@/utils/formatters.js'

defineEmits(['next'])

const quoteStore = useQuoteStore()
const catalogStore = useCatalogStore()

onMounted(() => catalogStore.fetchAll())

function selectType(type) {
  quoteStore.updateFormData({ projectTypeId: type.id })
}
</script>
