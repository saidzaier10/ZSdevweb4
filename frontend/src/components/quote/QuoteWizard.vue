<template>
  <div class="max-w-4xl mx-auto pb-24 lg:pb-0">
    <!-- En-tête du wizard -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-3">
        <span class="text-sm font-medium text-gray-500">
          Étape {{ store.currentStep }} sur {{ store.TOTAL_STEPS }}
        </span>
        <span class="text-sm font-medium text-primary-600">{{ store.progress }}% complété</span>
      </div>
      <ProgressBar :value="store.progress" height="md" />
    </div>

    <!-- Étapes -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Formulaire principal -->
      <div class="lg:col-span-2">
        <Transition
          :name="transitionName"
          mode="out-in"
        >
          <component
            :is="currentStepComponent"
            :key="store.currentStep"
            @next="handleNext"
          />
        </Transition>

        <!-- Navigation -->
        <div class="flex items-center justify-between mt-8">
          <BaseButton
            v-if="store.currentStep > 1"
            variant="ghost"
            @click="store.prevStep()"
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

      <!-- Sidebar prix en temps réel (desktop) -->
      <div class="hidden lg:block">
        <PricingDisplay />
      </div>
    </div>

    <!-- Barre de prix sticky (mobile/tablet) -->
    <MobilePricingBar />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'
import ProgressBar from '@/components/ui/ProgressBar.vue'
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
const catalogStore = useCatalogStore()

const direction = ref(1)

const stepComponents = [
  Step1ProjectType,
  Step2Design,
  Step3Complexity,
  Step4Options,
  Step5LeadCapture,
  Step6Summary,
]

const currentStepComponent = computed(() => stepComponents[store.currentStep - 1])

const transitionName = computed(() => direction.value > 0 ? 'slide-left' : 'slide-right')

function handleNext() {
  if (store.canGoNext) {
    direction.value = 1
    store.nextStep()
  }
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

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.slide-right-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
