/**
 * Utilitaires de formatage partagés entre tous les composants.
 * DRY : une seule définition au lieu de 5+ copies.
 */

const priceFormatter = new Intl.NumberFormat('fr-FR', {
  style: 'currency',
  currency: 'EUR',
  minimumFractionDigits: 0,
  maximumFractionDigits: 0,
})

/**
 * Formate un nombre en prix euros (ex: 1 500 €)
 */
export function formatPrice(value) {
  return priceFormatter.format(value)
}

/**
 * Formate un pourcentage (ex: 20 %)
 */
export function formatPercent(value, decimals = 1) {
  return `${parseFloat(value).toFixed(decimals)} %`
}
