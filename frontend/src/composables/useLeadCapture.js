/**
 * useLeadCapture — Capture de lead anticipée à l'étape 5 du wizard.
 */
import { ref } from 'vue'
import { leadsApi } from '@/api/leads.js'
import { useQuoteStore } from '@/stores/quote.js'

export function useLeadCapture() {
  const quoteStore = useQuoteStore()
  const capturing = ref(false)
  const captureError = ref(null)

  let captureTimeout = null

  async function captureFromStep5() {
    const { clientEmail, clientName, clientPhone, clientCompany, projectTypeId, budgetRange } =
      quoteStore.formData

    if (!clientEmail || !clientName) return

    // Debouncé pour éviter les doubles appels
    if (captureTimeout) clearTimeout(captureTimeout)

    captureTimeout = setTimeout(async () => {
      if (capturing.value) return
      capturing.value = true
      captureError.value = null

      try {
        const { data } = await leadsApi.capture({
          email: clientEmail,
          name: clientName,
          phone: clientPhone,
          company: clientCompany,
          source: 'quote_wizard',
          budget_range: budgetRange,
          project_type_id: projectTypeId,
        })
        quoteStore.leadId = data.id
      } catch (err) {
        // La capture de lead ne doit pas bloquer le wizard
        captureError.value = err.message
        console.warn('Lead capture failed (non-blocking):', err.message)
      } finally {
        capturing.value = false
      }
    }, 800)
  }

  async function captureFromROI(email, name, source = 'roi_calculator') {
    if (!email) return
    try {
      await leadsApi.capture({ email, name: name || '', source })
    } catch {
      // Silently fail
    }
  }

  async function captureFromEstimator(email, projectTypeId) {
    if (!email) return
    try {
      await leadsApi.capture({
        email,
        source: 'quick_estimate',
        project_type_id: projectTypeId,
      })
    } catch {
      // Silently fail
    }
  }

  return { capturing, captureError, captureFromStep5, captureFromROI, captureFromEstimator }
}
