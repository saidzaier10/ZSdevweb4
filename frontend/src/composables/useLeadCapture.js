/**
 * useLeadCapture — Capture de lead anticipée.
 * SRP : une seule méthode générique `capture()`, les contextes passent leurs données.
 */
import { ref } from 'vue'
import { leadsApi } from '@/api/leads.js'
import { useQuoteStore } from '@/stores/quote.js'

export function useLeadCapture() {
  const quoteStore = useQuoteStore()
  const capturing = ref(false)
  const captureError = ref(null)

  let captureTimeout = null

  /**
   * Méthode générique de capture — tous les contextes l'utilisent.
   * Non-bloquante : ne lève jamais d'erreur vers l'appelant.
   */
  async function capture(payload) {
    if (!payload.email) return
    try {
      const { data } = await leadsApi.capture(payload)
      return data
    } catch (err) {
      console.warn(`Lead capture failed [${payload.source}] (non-blocking):`, err.message)
    }
  }

  /**
   * Capture depuis l'étape 5 du wizard — debouncée 800ms.
   */
  async function captureFromStep5() {
    const { clientEmail, clientName, clientPhone, clientCompany, projectTypeId, budgetRange } =
      quoteStore.formData

    if (!clientEmail || !clientName) return

    if (captureTimeout) clearTimeout(captureTimeout)

    captureTimeout = setTimeout(async () => {
      if (capturing.value) return
      capturing.value = true
      captureError.value = null

      try {
        const data = await capture({
          email: clientEmail,
          name: clientName,
          phone: clientPhone,
          company: clientCompany,
          source: 'quote_wizard',
          budget_range: budgetRange,
          project_type_id: projectTypeId,
        })
        if (data?.id) quoteStore.leadId = data.id
      } catch (err) {
        captureError.value = err.message
      } finally {
        capturing.value = false
      }
    }, 800)
  }

  /**
   * Capture depuis le calculateur ROI.
   */
  function captureFromROI(email, name, source = 'roi_calculator') {
    return capture({ email, name: name || '', source })
  }

  /**
   * Capture depuis l'estimateur rapide.
   */
  function captureFromEstimator(email, projectTypeId) {
    return capture({ email, source: 'quick_estimate', project_type_id: projectTypeId })
  }

  return { capturing, captureError, capture, captureFromStep5, captureFromROI, captureFromEstimator }
}
