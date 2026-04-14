<template>
  <div class="animate-fade-in">
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Résumé de votre projet</h2>
    <p class="text-gray-600 mb-6">Vérifiez les informations avant d'envoyer votre demande.</p>

    <!-- Récapitulatif projet -->
    <div class="space-y-4">
      <div class="card">
        <h3 class="font-semibold text-gray-900 mb-3">Votre projet</h3>
        <dl class="space-y-2">
          <div class="flex justify-between text-sm">
            <dt class="text-gray-600">Type</dt>
            <dd class="font-medium">{{ projectType?.name || '—' }}</dd>
          </div>
          <div class="flex justify-between text-sm">
            <dt class="text-gray-600">Design</dt>
            <dd class="font-medium">{{ designOption?.name || '—' }}</dd>
          </div>
          <div class="flex justify-between text-sm">
            <dt class="text-gray-600">Complexité</dt>
            <dd class="font-medium">{{ complexity?.name || '—' }}</dd>
          </div>
          <div v-if="selectedOptions.length > 0" class="flex justify-between text-sm">
            <dt class="text-gray-600">Options</dt>
            <dd class="font-medium text-right">{{ selectedOptions.map(o => o.name).join(', ') }}</dd>
          </div>
        </dl>
      </div>

      <div class="card">
        <h3 class="font-semibold text-gray-900 mb-3">Vos coordonnées</h3>
        <dl class="space-y-2">
          <div class="flex justify-between text-sm">
            <dt class="text-gray-600">Nom</dt>
            <dd class="font-medium">{{ quoteStore.formData.clientName }}</dd>
          </div>
          <div class="flex justify-between text-sm">
            <dt class="text-gray-600">Email</dt>
            <dd class="font-medium">{{ quoteStore.formData.clientEmail }}</dd>
          </div>
        </dl>
      </div>

      <!-- Description -->
      <div>
        <label for="project_description" class="block text-sm font-medium text-gray-700 mb-1">
          Description du projet <span class="text-gray-500">(facultatif)</span>
        </label>
        <textarea
          id="project_description"
          v-model="description"
          rows="4"
          placeholder="Décrivez votre projet en quelques mots, vos objectifs, les fonctionnalités souhaitées..."
          class="input-field resize-none"
        />
      </div>
    </div>

    <!-- Estimation prix mobile -->
    <div class="lg:hidden mt-6">
      <InstallmentPlan v-if="pricing" :pricing="pricing" />
    </div>

    <!-- Message erreur -->
    <div v-if="quoteStore.error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">
      Une erreur est survenue. Veuillez réessayer ou nous contacter directement.
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useQuoteStore } from '@/stores/quote.js'
import { useCatalogStore } from '@/stores/catalog.js'
import { usePricing } from '@/composables/usePricing.js'
import InstallmentPlan from '../InstallmentPlan.vue'

defineEmits(['next'])

const quoteStore = useQuoteStore()
const catalogStore = useCatalogStore()
const { pricing } = usePricing()

const description = ref(quoteStore.formData.projectDescription)
watch(description, (val) => quoteStore.updateFormData({ projectDescription: val }))

const projectType = computed(() => catalogStore.getProjectTypeById(quoteStore.formData.projectTypeId))
const designOption = computed(() => catalogStore.getDesignOptionById(quoteStore.formData.designOptionId))
const complexity = computed(() => catalogStore.getComplexityById(quoteStore.formData.complexityId))
const selectedOptions = computed(() => catalogStore.getOptionsByIds(quoteStore.formData.optionIds))
</script>
