<template>
  <div :class="['animate-pulse bg-gray-200 rounded-lg', sizeClass, props.class]" aria-hidden="true" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  width: { type: String, default: 'w-full' },
  height: { type: String, default: 'h-4' },
  rounded: { type: String, default: 'rounded-lg' },
  class: { type: String, default: '' },
})

const sizeClass = computed(() => `${props.width} ${props.height} ${props.rounded}`)
</script>
