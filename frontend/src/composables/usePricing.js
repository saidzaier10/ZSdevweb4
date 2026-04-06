/**
 * usePricing — Calcul de prix en temps réel (JS pur, sans API).
 * Miroir client-side de PricingService Python.
 */
import { computed } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'

export function usePricing() {
  const quoteStore = useQuoteStore()
  const catalogStore = useCatalogStore()

  const VAT_RATE = 20

  function round2(n) {
    return Math.round(n * 100) / 100
  }

  const pricing = computed(() => {
    const { projectTypeId, designOptionId, complexityId, optionIds } = quoteStore.formData

    // 1. Prix de base
    const projectType = catalogStore.getProjectTypeById(projectTypeId)
    if (!projectType) return null

    const basePrice = parseFloat(projectType.base_price)

    // 2. Supplément design
    const designOption = catalogStore.getDesignOptionById(designOptionId)
    const designSupplement = designOption ? parseFloat(designOption.price_supplement) : 0

    const afterDesign = basePrice + designSupplement

    // 3. Multiplicateur complexité
    const complexity = catalogStore.getComplexityById(complexityId)
    const complexityFactor = complexity ? parseFloat(complexity.multiplier) : 1
    const afterComplexity = round2(afterDesign * complexityFactor)

    // 4. Options supplémentaires
    const options = catalogStore.getOptionsByIds(optionIds)
    const optionsTotal = options.reduce((sum, o) => sum + parseFloat(o.price), 0)

    // 5. Sous-total
    const subtotalHt = round2(afterComplexity + optionsTotal)

    // 6. TVA
    const vatAmount = round2(subtotalHt * VAT_RATE / 100)
    const totalTtc = round2(subtotalHt + vatAmount)

    // 7. Plan de paiement
    const i1 = round2(totalTtc * 0.30)
    const i2 = round2(totalTtc * 0.40)
    const i3 = round2(totalTtc - i1 - i2)

    return {
      base_price: basePrice,
      design_supplement: designSupplement,
      complexity_factor: complexityFactor,
      options_total: optionsTotal,
      subtotal_ht: subtotalHt,
      vat_rate: VAT_RATE,
      vat_amount: vatAmount,
      total_ttc: totalTtc,
      installment_1: i1,
      installment_2: i2,
      installment_3: i3,
    }
  })

  function formatPrice(value) {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  return { pricing, formatPrice }
}
