/**
 * usePricing — Prix en temps réel via l'API /price-preview/.
 *
 * ARCHITECTURE: Le calcul est fait EXCLUSIVEMENT côté backend (Python/Decimal).
 * Ce composable appelle l'endpoint avec debounce 300ms.
 * Avantage: une seule logique de calcul, zéro risque de divergence float/Decimal.
 */
import { ref, watch } from 'vue'
import { quotesApi } from '@/api/quotes.js'
import { useQuoteStore } from '@/stores/quote.js'
import { formatPrice } from '@/utils/formatters.js'

export function usePricing() {
  const quoteStore = useQuoteStore()
  const pricing = ref(null)
  const loading = ref(false)
  let debounceTimer = null

  async function fetchPreview() {
    const { projectTypeId, designOptionId, complexityId, optionIds } = quoteStore.formData

    if (!projectTypeId) {
      pricing.value = null
      return
    }

    loading.value = true
    try {
      const { data } = await quotesApi.pricePreview({
        project_type_id: projectTypeId,
        design_option_id: designOptionId || null,
        complexity_id: complexityId || null,
        option_ids: optionIds || [],
      })
      pricing.value = data
    } catch (e) {
      console.warn('Price preview failed (non-blocking):', e.message)
      pricing.value = null
    } finally {
      loading.value = false
    }
  }

  // Déclenche un appel debouncé à chaque changement des sélections
  watch(
    () => [
      quoteStore.formData.projectTypeId,
      quoteStore.formData.designOptionId,
      quoteStore.formData.complexityId,
      // JSON.stringify pour détecter les changements dans le tableau
      JSON.stringify(quoteStore.formData.optionIds),
    ],
    () => {
      clearTimeout(debounceTimer)
      debounceTimer = setTimeout(fetchPreview, 300)
    },
    { immediate: true },
  )

  return { pricing, loading, formatPrice }
}
