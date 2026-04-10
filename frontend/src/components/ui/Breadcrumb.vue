<template>
  <nav aria-label="Fil d'Ariane" class="mb-6">
    <ol class="flex items-center gap-1 text-sm text-gray-500 flex-wrap">
      <li v-for="(crumb, idx) in crumbs" :key="idx" class="flex items-center gap-1">
        <span v-if="idx > 0" class="text-gray-300" aria-hidden="true">/</span>
        <RouterLink
          v-if="crumb.to && idx < crumbs.length - 1"
          :to="crumb.to"
          class="hover:text-primary-600 transition-colors"
        >
          {{ crumb.label }}
        </RouterLink>
        <span v-else class="font-medium text-gray-900" :aria-current="idx === crumbs.length - 1 ? 'page' : undefined">
          {{ crumb.label }}
        </span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  crumbs: {
    type: Array, // [{ label: String, to?: String }]
    required: true,
  },
})
</script>
