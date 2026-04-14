<template>
  <div class="relative">
    <button
      @click="open = !open"
      class="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      :aria-expanded="open"
      aria-haspopup="true"
    >
      <div class="w-7 h-7 bg-primary-600 rounded-full flex items-center justify-center text-white text-xs font-bold select-none" aria-hidden="true">
        {{ initials }}
      </div>
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300 max-w-[120px] truncate">
        {{ displayName }}
      </span>
      <svg
        class="w-4 h-4 text-gray-500 transition-transform"
        :class="{ 'rotate-180': open }"
        fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <Transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95 -translate-y-1"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-95 -translate-y-1"
    >
      <div
        v-if="open"
        v-click-outside="() => open = false"
        class="absolute right-0 mt-2 w-52 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 py-1 z-50 origin-top-right"
        role="menu"
      >
        <div class="px-4 py-2.5 border-b border-gray-100 dark:border-gray-700">
          <p class="text-xs text-gray-500">Connecté en tant que</p>
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ user?.email }}</p>
        </div>

        <RouterLink
          v-if="user?.is_staff"
          to="/tableau-de-bord"
          class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
          role="menuitem"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Tableau de bord
        </RouterLink>

        <div v-if="user?.is_staff" class="border-t border-gray-100 dark:border-gray-700 my-1"></div>

        <RouterLink
          to="/espace-client"
          class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          role="menuitem"
        >
          <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Mes projets
        </RouterLink>

        <RouterLink
          to="/espace-client/profil"
          class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          role="menuitem"
        >
          <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Mon profil
        </RouterLink>

        <div class="border-t border-gray-100 dark:border-gray-700 mt-1 pt-1">
          <button
            @click="$emit('logout')"
            class="w-full flex items-center gap-2.5 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            role="menuitem"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Se déconnecter
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  user: { type: Object, default: null },
})

defineEmits(['logout'])

const open = ref(false)

const initials = computed(() =>
  props.user?.first_name?.[0]?.toUpperCase()
  || props.user?.email?.[0]?.toUpperCase()
  || '?'
)

const displayName = computed(() =>
  props.user?.first_name || props.user?.email || ''
)

defineExpose({ close: () => { open.value = false } })
</script>
