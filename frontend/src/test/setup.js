/**
 * Setup global Vitest — exécuté avant chaque fichier de test.
 */
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach } from 'vitest'

// Recrée une instance Pinia fraîche avant chaque test
beforeEach(() => {
  setActivePinia(createPinia())
})
