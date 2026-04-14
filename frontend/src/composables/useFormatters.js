export function useFormatters() {
  function formatPrice(value) {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      maximumFractionDigits: 0,
    }).format(Number(value))
  }

  function formatDate(d, opts = { day: 'numeric', month: 'long', year: 'numeric' }) {
    if (!d) return '—'
    return new Date(d).toLocaleDateString('fr-FR', opts)
  }

  function formatDateShort(d) {
    return formatDate(d, { day: '2-digit', month: '2-digit', year: 'numeric' })
  }

  return { formatPrice, formatDate, formatDateShort }
}
