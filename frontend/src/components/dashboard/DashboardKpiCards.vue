<template>
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
    <div v-for="kpi in kpiCards" :key="kpi.label" class="card">
      <template v-if="loading">
        <div class="h-3 w-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-3"></div>
        <div class="h-7 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </template>
      <template v-else>
        <p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">{{ kpi.label }}</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ kpi.value }}</p>
        <p v-if="kpi.sub" class="text-xs text-gray-400 mt-1">{{ kpi.sub }}</p>
      </template>
    </div>
  </div>
</template>

<script setup>
defineProps({
  loading:  { type: Boolean, default: false },
  kpiCards: { type: Array,   default: () => [] },
})
</script>
