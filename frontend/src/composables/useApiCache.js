/**
 * useApiCache — cache en mémoire pour les appels API GET répétitifs.
 *
 * Usage :
 *   const { data, loading, error } = useApiCache('portfolio', portfolioApi.getProjects, { ttl: 300_000 })
 *
 * - TTL par défaut : 5 minutes
 * - Le cache est partagé entre tous les composants (module-level Map)
 * - Pas de dépendance externe
 */
import { ref, readonly } from 'vue'

const _cache = new Map() // { key → { data, expiresAt } }

const DEFAULT_TTL = 5 * 60 * 1000 // 5 minutes

/**
 * @param {string} key         Clé unique du cache
 * @param {Function} fetcher   Fonction async () => axios response
 * @param {object} [options]
 * @param {number} [options.ttl]      TTL en ms (défaut 5 min)
 * @param {boolean} [options.eager]   Si true, déclenche le fetch immédiatement (défaut true)
 */
export function useApiCache(key, fetcher, { ttl = DEFAULT_TTL, eager = true } = {}) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetch(force = false) {
    const cached = _cache.get(key)
    if (!force && cached && Date.now() < cached.expiresAt) {
      data.value = cached.data
      return
    }

    loading.value = true
    error.value = null
    try {
      const response = await fetcher()
      const result = response.data?.results ?? response.data
      data.value = result
      _cache.set(key, { data: result, expiresAt: Date.now() + ttl })
    } catch (err) {
      error.value = err
    } finally {
      loading.value = false
    }
  }

  /** Force la suppression du cache pour cette clé. */
  function invalidate() {
    _cache.delete(key)
  }

  if (eager) {
    fetch()
  }

  return {
    data: readonly(data),
    loading: readonly(loading),
    error: readonly(error),
    fetch,
    invalidate,
  }
}

/** Vide tout le cache (ex : après logout). */
export function clearApiCache() {
  _cache.clear()
}
