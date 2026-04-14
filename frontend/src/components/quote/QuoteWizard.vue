<template>
  <div class="max-w-4xl mx-auto pb-24 lg:pb-0">
    <!-- Navigation par étapes cliquable -->
    <nav class="mb-8" aria-label="Étapes du devis">
      <ol class="flex items-center gap-0">
        <template v-for="(step, idx) in steps" :key="step.key">
          <li class="flex items-center flex-shrink-0">
            <button
              @click="navigateTo(idx + 1)"
              :disabled="!canNavigateTo(idx + 1)"
              :aria-current="store.currentStep === idx + 1 ? 'step' : undefined"
              :aria-label="`Étape ${idx + 1} : ${step.label}`"
              class="flex flex-col items-center gap-1.5 group disabled:cursor-default"
            >
              <!-- Cercle -->
              <span
                class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all"
                :class="stepCircleClass(idx + 1)"
              >
                <!-- Étape complétée -->
                <svg v-if="isCompleted(idx + 1)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-else>{{ idx + 1 }}</span>
              </span>
              <!-- Label (desktop uniquement) -->
              <span
                class="hidden sm:block text-xs font-medium transition-colors"
                :class="stepLabelClass(idx + 1)"
              >{{ step.label }}</span>
            </button>
          </li>
          <!-- Connecteur -->
          <li v-if="idx < steps.length - 1" class="flex-1 h-0.5 mx-1 transition-all" :class="isCompleted(idx + 2) || store.currentStep === idx + 2 ? 'bg-primary-400' : 'bg-gray-200 dark:bg-gray-700'" aria-hidden="true" />
        </template>
      </ol>
      <!-- Progression % sous les étapes sur mobile -->
      <div class="flex items-center justify-between mt-3 sm:hidden">
        <span class="text-xs text-gray-600 dark:text-gray-400">Étape {{ store.currentStep }} / {{ store.TOTAL_STEPS }}</span>
        <span class="text-xs font-semibold text-primary-600">{{ store.progress }}%</span>
      </div>
    </nav>

    <!-- Étapes -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Formulaire principal -->
      <div class="lg:col-span-2">
        <Transition :name="transitionName" mode="out-in">
          <component
            :is="currentStepComponent"
            :key="store.currentStep"
            @next="handleNext"
          />
        </Transition>

        <!-- Navigation bas -->
        <div class="flex items-center justify-between mt-8">
          <BaseButton
            v-if="store.currentStep > 1"
            variant="ghost"
            @click="handleBack"
          >
            ← Retour
          </BaseButton>
          <div v-else />

          <BaseButton
            v-if="!store.isLastStep"
            variant="primary"
            :disabled="!store.canGoNext"
            @click="handleNext"
          >
            Continuer →
          </BaseButton>
          <BaseButton
            v-else
            variant="primary"
            :loading="store.submitting"
            @click="handleSubmit"
          >
            {{ store.submitting ? 'Envoi en cours...' : 'Envoyer ma demande' }}
          </BaseButton>
        </div>
      </div>

      <!-- Sidebar prix (desktop) -->
      <div class="hidden lg:block">
        <PricingDisplay />
      </div>
    </div>

    <!-- Barre de prix sticky (mobile) -->
    <MobilePricingBar />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import BaseButton from '@/components/ui/BaseButton.vue'
import PricingDisplay from './PricingDisplay.vue'
import MobilePricingBar from './MobilePricingBar.vue'
import Step1ProjectType from './steps/Step1ProjectType.vue'
import Step2Design from './steps/Step2Design.vue'
import Step3Complexity from './steps/Step3Complexity.vue'
import Step4Options from './steps/Step4Options.vue'
import Step5LeadCapture from './steps/Step5LeadCapture.vue'
import Step6Summary from './steps/Step6Summary.vue'

const emit = defineEmits(['submitted'])
const store = useQuoteStore()

const direction = ref(1)

const steps = [
  { key: 'type',       label: 'Projet' },
  { key: 'design',     label: 'Design' },
  { key: 'complexity', label: 'Complexité' },
  { key: 'options',    label: 'Options' },
  { key: 'contact',    label: 'Contact' },
  { key: 'recap',      label: 'Récap' },
]

const stepComponents = [
  Step1ProjectType, Step2Design, Step3Complexity,
  Step4Options, Step5LeadCapture, Step6Summary,
]

const currentStepComponent = computed(() => stepComponents[store.currentStep - 1])
const transitionName = computed(() => direction.value > 0 ? 'slide-left' : 'slide-right')

// Une étape est complétée si elle est AVANT l'étape courante
function isCompleted(step) { return step < store.currentStep }

// On peut naviguer vers une étape si elle est déjà complétée (retour) ou c'est l'étape courante
function canNavigateTo(step) {
  if (step === store.currentStep) return false
  if (step < store.currentStep) return true
  return false
}

function navigateTo(step) {
  if (!canNavigateTo(step)) return
  direction.value = step > store.currentStep ? 1 : -1
  store.goToStep(step)
}

function stepCircleClass(step) {
  if (step === store.currentStep) return 'bg-primary-600 text-white ring-4 ring-primary-100 dark:ring-primary-900'
  if (isCompleted(step)) return 'bg-primary-500 text-white cursor-pointer hover:bg-primary-600 transition-colors'
  return 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-500'
}

function stepLabelClass(step) {
  if (step === store.currentStep) return 'text-primary-600 dark:text-primary-400'
  if (isCompleted(step)) return 'text-gray-600 dark:text-gray-300'
  return 'text-gray-500 dark:text-gray-600'
}

function handleNext() {
  if (store.canGoNext) {
    direction.value = 1
    store.nextStep()
  }
}

function handleBack() {
  direction.value = -1
  store.prevStep()
}

async function handleSubmit() {
  try {
    const quote = await store.submitQuote()
    emit('submitted', quote)
  } catch (err) {
    // Erreur gérée dans le store
  }
}
</script>

<style scoped>
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.25s ease;
}
.slide-left-enter-from  { opacity: 0; transform: translateX(20px); }
.slide-left-leave-to    { opacity: 0; transform: translateX(-20px); }
.slide-right-enter-from { opacity: 0; transform: translateX(-20px); }
.slide-right-leave-to   { opacity: 0; transform: translateX(20px); }
</style>
