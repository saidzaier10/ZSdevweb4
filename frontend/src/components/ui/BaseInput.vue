<template>
  <div class="space-y-1">
    <label v-if="label" :for="stableId" class="block text-sm font-medium" :class="error ? 'text-red-700' : 'text-gray-700'">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1" aria-hidden="true">*</span>
    </label>
    <input
      :id="stableId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="error ? `${stableId}-error` : hint ? `${stableId}-hint` : undefined"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="$emit('blur', $event)"
      class="input-field"
      :class="{ 'border-red-300 focus:ring-red-500 bg-red-50': error }"
    />
    <p v-if="error" :id="`${stableId}-error`" class="text-sm text-red-600 flex items-center gap-1" role="alert">
      <svg class="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      {{ error }}
    </p>
    <p v-else-if="hint" :id="`${stableId}-hint`" class="text-sm text-gray-600">{{ hint }}</p>
  </div>
</template>

<script setup>
let _counter = 0

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  required: Boolean,
  disabled: Boolean,
  error: String,
  hint: String,
  inputId: { type: String, default: null },
})

defineEmits(['update:modelValue', 'blur'])

// ID stable : priorité à la prop explicite, sinon compteur créé une seule fois à l'instanciation
const stableId = props.inputId ?? `input-${++_counter}`
</script>
