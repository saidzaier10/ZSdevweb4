<template>
  <div class="w-full bg-gray-200 rounded-full overflow-hidden" :class="heightClass">
    <div
      class="bg-primary-600 rounded-full transition-all duration-500 ease-out"
      :class="heightClass"
      :style="{ width: `${Math.min(100, Math.max(0, value))}%` }"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, default: 0 },
  height: { type: String, default: 'md' },
})

const heightClass = computed(() => ({
  sm: 'h-1',
  md: 'h-2',
  lg: 'h-3',
}[props.height]))
</script>
