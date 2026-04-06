<template>
  <section class="py-20 bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="section-title">Simulez le ROI de votre projet</h2>
        <p class="section-subtitle mx-auto">Estimez le retour sur investissement de votre nouveau site web.</p>
      </div>

      <div class="card">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Inputs -->
          <div class="space-y-5">
            <h3 class="font-semibold text-gray-900">Votre situation actuelle</h3>

            <div v-for="input in inputConfig" :key="input.key" class="space-y-1">
              <label class="text-sm font-medium text-gray-700">{{ input.label }}</label>
              <div class="flex items-center gap-3">
                <input
                  type="range"
                  :min="input.min"
                  :max="input.max"
                  :step="input.step"
                  :value="roiInputs[input.key]"
                  @input="updateInput(input.key, $event.target.value)"
                  class="flex-1 h-2 bg-gray-200 rounded-lg accent-primary-600"
                />
                <span class="w-20 text-right text-sm font-semibold text-gray-900">
                  {{ roiInputs[input.key] }}{{ input.suffix }}
                </span>
              </div>
            </div>
          </div>

          <!-- Résultats -->
          <div class="bg-gradient-to-br from-primary-50 to-accent-50 rounded-xl p-6 space-y-4">
            <h3 class="font-semibold text-gray-900">Votre gain estimé</h3>

            <div class="space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Revenus actuels / mois</span>
                <span class="font-semibold">{{ formatCurrency(results.currentMonthlyRevenue) }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Revenus avec nouveau site</span>
                <span class="font-semibold text-green-600">{{ formatCurrency(results.newMonthlyRevenue) }}</span>
              </div>
              <div class="border-t border-gray-200 pt-3 flex justify-between items-center">
                <span class="text-sm font-medium">Gain mensuel</span>
                <span class="text-xl font-bold text-primary-600">+{{ formatCurrency(results.monthlyGain) }}</span>
              </div>
            </div>

            <div class="bg-white rounded-lg p-4 mt-4">
              <div class="text-center">
                <div class="text-3xl font-bold text-green-600">{{ formatCurrency(results.roi12Months) }}</div>
                <div class="text-sm text-gray-500">ROI sur 12 mois</div>
                <div v-if="results.monthsToROI" class="text-xs text-gray-400 mt-1">
                  Rentabilisé en {{ results.monthsToROI }} mois
                </div>
              </div>
            </div>

            <RouterLink to="/devis" class="btn-primary w-full justify-center mt-4">
              Obtenir mon devis →
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useROI } from '@/composables/useROI.js'

const { inputs: roiInputs, results, formatCurrency, updateInput } = useROI()

const inputConfig = [
  { key: 'monthlyVisitors', label: 'Visiteurs / mois actuels', min: 100, max: 50000, step: 100, suffix: '' },
  { key: 'currentConversionRate', label: 'Taux de conversion actuel (%)', min: 0.1, max: 10, step: 0.1, suffix: '%' },
  { key: 'averageOrderValue', label: 'Valeur client moyenne (€)', min: 50, max: 5000, step: 50, suffix: '€' },
  { key: 'expectedTrafficIncrease', label: 'Augmentation trafic attendue (%)', min: 10, max: 200, step: 10, suffix: '%' },
]
</script>
