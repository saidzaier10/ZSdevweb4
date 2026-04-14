<template>
  <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold', colorClass]">
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { QUOTE_STATUS_COLORS } from './statusColors.js'

const props = defineProps({
  status:   { type: String, required: true },
  label:    { type: String, default: null },
  colorMap: { type: Object, default: null },
})

const colorClass = computed(() => {
  const map = props.colorMap ?? QUOTE_STATUS_COLORS
  return map[props.status] ?? 'bg-gray-100 text-gray-600'
})
</script>
