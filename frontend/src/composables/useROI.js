/**
 * useROI — Calculateur ROI (JS pur, pas d'API).
 *
 * Aide le prospect à visualiser le retour sur investissement
 * d'un nouveau site web.
 */
import { computed, ref } from 'vue'
import { formatPrice } from '@/utils/formatters.js'

export function useROI() {
  const inputs = ref({
    monthlyVisitors: 1000,      // visiteurs/mois actuels
    currentConversionRate: 1,   // taux de conversion actuel (%)
    averageOrderValue: 150,     // valeur moyenne d'une commande (€)
    expectedTrafficIncrease: 50, // augmentation trafic attendue (%)
    newConversionRate: 2.5,     // nouveau taux de conversion avec le site (%)
    projectCost: 3000,          // coût du projet (€)
  })

  const results = computed(() => {
    const {
      monthlyVisitors,
      currentConversionRate,
      averageOrderValue,
      expectedTrafficIncrease,
      newConversionRate,
      projectCost,
    } = inputs.value

    // Revenus actuels
    const currentMonthlyLeads = monthlyVisitors * (currentConversionRate / 100)
    const currentMonthlyRevenue = currentMonthlyLeads * averageOrderValue

    // Revenus avec le nouveau site
    const newMonthlyVisitors = monthlyVisitors * (1 + expectedTrafficIncrease / 100)
    const newMonthlyLeads = newMonthlyVisitors * (newConversionRate / 100)
    const newMonthlyRevenue = newMonthlyLeads * averageOrderValue

    // Gain mensuel
    const monthlyGain = newMonthlyRevenue - currentMonthlyRevenue

    // Retour sur investissement
    const monthsToROI = projectCost > 0 ? Math.ceil(projectCost / monthlyGain) : null
    const roi12Months = monthlyGain * 12 - projectCost
    const roiPercent = projectCost > 0 ? Math.round((roi12Months / projectCost) * 100) : 0

    return {
      currentMonthlyRevenue: Math.round(currentMonthlyRevenue),
      newMonthlyRevenue: Math.round(newMonthlyRevenue),
      monthlyGain: Math.round(monthlyGain),
      annualGain: Math.round(monthlyGain * 12),
      roi12Months: Math.round(roi12Months),
      roiPercent,
      monthsToROI,
      currentMonthlyLeads: Math.round(currentMonthlyLeads),
      newMonthlyLeads: Math.round(newMonthlyLeads),
      additionalLeads: Math.round(newMonthlyLeads - currentMonthlyLeads),
    }
  })

  const formatCurrency = formatPrice

  function updateInput(key, value) {
    inputs.value[key] = parseFloat(value) || 0
  }

  return { inputs, results, formatCurrency, updateInput }
}
