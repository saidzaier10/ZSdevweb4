<template>
  <div class="card">
    <h2 class="font-bold text-gray-900 mb-5">Avancement du projet</h2>

    <!-- Étapes -->
    <div class="flex items-center gap-0 mb-6 overflow-x-auto pb-2">
      <template v-for="(step, i) in steps" :key="step.key">
        <div class="flex flex-col items-center flex-shrink-0 min-w-[80px]">
          <div
            class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all"
            :class="stepClass(step.key)"
          >
            <svg v-if="isStepDone(step.key)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <span class="text-xs text-center mt-1.5 text-gray-500 leading-tight">{{ step.label }}</span>
        </div>
        <div
          v-if="i < steps.length - 1"
          class="flex-1 h-0.5 min-w-[20px] transition-all"
          :class="isStepDone(steps[i + 1].key) || status === steps[i + 1].key ? 'bg-primary-500' : 'bg-gray-200'"
        />
      </template>
    </div>

    <!-- Barre % -->
    <div class="flex justify-between text-sm text-gray-500 mb-2">
      <span>Progression globale</span>
      <span class="font-bold text-gray-900">{{ progress }}%</span>
    </div>
    <div class="h-3 bg-gray-100 rounded-full overflow-hidden">
      <div
        class="h-3 bg-gradient-to-r from-primary-500 to-primary-400 rounded-full transition-all duration-700"
        :style="{ width: `${progress}%` }"
      />
    </div>

    <!-- Dates -->
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-100">
      <div v-if="startedAt">
        <div class="text-xs text-gray-400 uppercase tracking-wide mb-1">Démarrage</div>
        <div class="font-semibold text-gray-900">{{ formatDate(startedAt) }}</div>
      </div>
      <div v-if="estimatedDelivery">
        <div class="text-xs text-gray-400 uppercase tracking-wide mb-1">Livraison prévue</div>
        <div class="font-semibold text-gray-900">{{ formatDate(estimatedDelivery) }}</div>
      </div>
      <div v-if="deliveredAt">
        <div class="text-xs text-gray-400 uppercase tracking-wide mb-1">Livré le</div>
        <div class="font-semibold text-green-600">{{ formatDate(deliveredAt) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  status:            { type: String, required: true },
  progress:          { type: Number, default: 0 },
  startedAt:         { type: String, default: null },
  estimatedDelivery: { type: String, default: null },
  deliveredAt:       { type: String, default: null },
})

const steps = [
  { key: 'briefing',    label: 'Briefing' },
  { key: 'design',      label: 'Design' },
  { key: 'development', label: 'Dév.' },
  { key: 'review',      label: 'Révision' },
  { key: 'delivered',   label: 'Livré' },
]
const stepOrder = steps.map(s => s.key)

function isStepDone(key) {
  const current = stepOrder.indexOf(props.status)
  return current > stepOrder.indexOf(key)
}

function stepClass(key) {
  if (props.status === key)   return 'bg-primary-600 text-white ring-4 ring-primary-100'
  if (isStepDone(key))        return 'bg-primary-500 text-white'
  return 'bg-gray-100 text-gray-400'
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
