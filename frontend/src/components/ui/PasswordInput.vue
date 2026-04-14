<template>
  <div>
    <label v-if="label" :for="stableId" class="block text-sm font-medium text-gray-700 dark:text-white mb-1">
      {{ label }}
    </label>
    <div class="relative">
      <input
        :id="stableId"
        :type="visible ? 'text' : 'password'"
        :value="modelValue"
        :placeholder="placeholder"
        :required="required"
        :minlength="minlength"
        :autocomplete="autocomplete"
        :class="['input-field w-full pr-10', { 'border-red-400': error }]"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <button
        type="button"
        @click="visible = !visible"
        class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
        :aria-label="visible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
        tabindex="-1"
      >
        <!-- Oeil ouvert -->
        <svg v-if="visible" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        <!-- Oeil barré -->
        <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.477 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
        </svg>
      </button>
    </div>
    <p v-if="error" class="text-xs text-red-600 mt-1">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

let _counter = 0

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '••••••••' },
  required: { type: Boolean, default: false },
  minlength: { type: [String, Number], default: null },
  autocomplete: { type: String, default: 'current-password' },
  error: { type: String, default: '' },
  inputId: { type: String, default: null },
})

defineEmits(['update:modelValue'])

const stableId = props.inputId ?? `password-${++_counter}`
const visible  = ref(false)
</script>
