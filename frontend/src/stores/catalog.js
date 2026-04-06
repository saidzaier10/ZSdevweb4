import { defineStore } from 'pinia'
import { ref } from 'vue'
import { catalogApi } from '@/api/catalog.js'

export const useCatalogStore = defineStore('catalog', () => {
  const categories = ref([])
  const designOptions = ref([])
  const complexityLevels = ref([])
  const supplementaryOptions = ref([])
  const loading = ref(false)
  const loaded = ref(false)

  async function fetchAll() {
    if (loaded.value) return
    loading.value = true
    try {
      const [cat, design, complexity, options] = await Promise.all([
        catalogApi.getCategories(),
        catalogApi.getDesignOptions(),
        catalogApi.getComplexityLevels(),
        catalogApi.getSupplementaryOptions(),
      ])
      categories.value = cat.data.results ?? cat.data
      designOptions.value = design.data.results ?? design.data
      complexityLevels.value = complexity.data.results ?? complexity.data
      supplementaryOptions.value = options.data.results ?? options.data
      loaded.value = true
    } finally {
      loading.value = false
    }
  }

  function getProjectTypeById(id) {
    for (const cat of categories.value) {
      const found = cat.project_types?.find((t) => t.id === id)
      if (found) return found
    }
    return null
  }

  function getDesignOptionById(id) {
    return designOptions.value.find((d) => d.id === id) || null
  }

  function getComplexityById(id) {
    return complexityLevels.value.find((c) => c.id === id) || null
  }

  function getOptionsByIds(ids) {
    return supplementaryOptions.value.filter((o) => ids.includes(o.id))
  }

  return {
    categories,
    designOptions,
    complexityLevels,
    supplementaryOptions,
    loading,
    loaded,
    fetchAll,
    getProjectTypeById,
    getDesignOptionById,
    getComplexityById,
    getOptionsByIds,
  }
})
