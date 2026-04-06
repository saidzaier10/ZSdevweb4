import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { quotesApi } from '@/api/quotes.js'

// NOTE ARCHITECTURE: Le pricing n'est PAS dans ce store.
// usePricing() composable gère les prix via l'API /price-preview/.
// Ce store gère uniquement l'état du wizard (steps + formData + submit).

export const useQuoteStore = defineStore('quote', () => {
  const TOTAL_STEPS = 6

  const currentStep = ref(1)
  const submitting = ref(false)
  const submitted = ref(false)
  const submittedQuote = ref(null)
  const error = ref(null)
  const leadId = ref(null)

  const formData = ref({
    // Étape 1 — Catégorie / Type
    projectTypeId: null,
    categoryId: null,

    // Étape 2 — Design
    designOptionId: null,

    // Étape 3 — Complexité
    complexityId: null,

    // Étape 4 — Options
    optionIds: [],

    // Étape 5 — Lead
    clientName: '',
    clientEmail: '',
    clientPhone: '',
    clientCompany: '',
    budgetRange: '',

    // Étape 6 — Description / Délai
    projectDescription: '',
    desiredDeadline: null,
  })

  const progress = computed(() => Math.round((currentStep.value / TOTAL_STEPS) * 100))
  const canGoNext = computed(() => {
    return validateStep(currentStep.value)
  })
  const isLastStep = computed(() => currentStep.value === TOTAL_STEPS)

  function validateStep(step) {
    switch (step) {
      case 1: return !!formData.value.projectTypeId
      case 2: return !!formData.value.designOptionId
      case 3: return !!formData.value.complexityId
      case 4: return true // Options facultatives
      case 5: return !!formData.value.clientEmail && !!formData.value.clientName
      case 6: return true
      default: return true
    }
  }

  function nextStep() {
    if (currentStep.value < TOTAL_STEPS && canGoNext.value) {
      currentStep.value++
    }
  }

  function prevStep() {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  function goToStep(step) {
    if (step >= 1 && step <= TOTAL_STEPS) {
      currentStep.value = step
    }
  }

  function updateFormData(data) {
    Object.assign(formData.value, data)
  }

  function toggleOption(optionId) {
    const idx = formData.value.optionIds.indexOf(optionId)
    if (idx === -1) {
      formData.value.optionIds.push(optionId)
    } else {
      formData.value.optionIds.splice(idx, 1)
    }
  }

  async function submitQuote() {
    if (submitting.value) return

    submitting.value = true
    error.value = null

    try {
      const payload = {
        project_type_id: formData.value.projectTypeId,
        design_option_id: formData.value.designOptionId,
        complexity_id: formData.value.complexityId,
        option_ids: formData.value.optionIds,
        client_name: formData.value.clientName,
        client_email: formData.value.clientEmail,
        client_phone: formData.value.clientPhone,
        client_company: formData.value.clientCompany,
        project_description: formData.value.projectDescription,
        desired_deadline: formData.value.desiredDeadline || null,
      }

      const { data } = await quotesApi.create(payload)
      submittedQuote.value = data
      submitted.value = true
      return data
    } catch (err) {
      error.value = err.response?.data || { detail: 'Une erreur est survenue.' }
      throw err
    } finally {
      submitting.value = false
    }
  }

  function reset() {
    currentStep.value = 1
    submitted.value = false
    submittedQuote.value = null
    error.value = null
    leadId.value = null
    formData.value = {
      projectTypeId: null,
      categoryId: null,
      designOptionId: null,
      complexityId: null,
      optionIds: [],
      clientName: '',
      clientEmail: '',
      clientPhone: '',
      clientCompany: '',
      budgetRange: '',
      projectDescription: '',
      desiredDeadline: null,
    }
  }

  return {
    currentStep, formData, progress, submitting, submitted,
    submittedQuote, error, leadId, canGoNext, isLastStep,
    nextStep, prevStep, goToStep, updateFormData, toggleOption,
    submitQuote, reset, TOTAL_STEPS,
  }
})
