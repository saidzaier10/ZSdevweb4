import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { quotesApi } from '@/api/quotes.js'

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

  // Prix calculés localement (mis à jour par usePricing)
  const pricing = ref({
    base_price: 0,
    design_supplement: 0,
    complexity_factor: 1,
    options_total: 0,
    subtotal_ht: 0,
    discount_percent: 0,
    discount_amount: 0,
    vat_rate: 20,
    vat_amount: 0,
    total_ttc: 0,
    installment_1: 0,
    installment_2: 0,
    installment_3: 0,
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

  function updatePricing(newPricing) {
    Object.assign(pricing.value, newPricing)
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
    pricing.value = {
      base_price: 0, design_supplement: 0, complexity_factor: 1,
      options_total: 0, subtotal_ht: 0, discount_percent: 0,
      discount_amount: 0, vat_rate: 20, vat_amount: 0,
      total_ttc: 0, installment_1: 0, installment_2: 0, installment_3: 0,
    }
  }

  return {
    currentStep, formData, pricing, progress, submitting, submitted,
    submittedQuote, error, leadId, canGoNext, isLastStep,
    nextStep, prevStep, goToStep, updateFormData, toggleOption,
    updatePricing, submitQuote, reset, TOTAL_STEPS,
  }
})
