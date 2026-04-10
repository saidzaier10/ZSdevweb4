/**
 * Tests du composable useApiCache.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { nextTick } from 'vue'
import { useApiCache, clearApiCache } from '@/composables/useApiCache.js'

beforeEach(() => {
  clearApiCache()
})

const mockFetcher = (data) => vi.fn().mockResolvedValue({ data })
const mockFetcherPaginated = (items) =>
  vi.fn().mockResolvedValue({ data: { results: items, count: items.length } })
const mockFetcherError = () =>
  vi.fn().mockRejectedValue(new Error('Network Error'))

describe('useApiCache', () => {
  it('fetches data and stores it', async () => {
    const fetcher = mockFetcher([{ id: 1 }])
    const { data, loading } = useApiCache('test:list', fetcher)

    expect(loading.value).toBe(true)
    await nextTick()
    await new Promise((r) => setTimeout(r, 0))

    expect(loading.value).toBe(false)
    expect(data.value).toEqual([{ id: 1 }])
    expect(fetcher).toHaveBeenCalledTimes(1)
  })

  it('extracts results from paginated response', async () => {
    const items = [{ id: 1 }, { id: 2 }]
    const fetcher = mockFetcherPaginated(items)
    const { data } = useApiCache('test:paginated', fetcher)

    await new Promise((r) => setTimeout(r, 10))
    expect(data.value).toEqual(items)
  })

  it('uses cache on second call with same key', async () => {
    const fetcher = mockFetcher([{ id: 1 }])
    useApiCache('test:cache', fetcher)
    await new Promise((r) => setTimeout(r, 10))

    const { data } = useApiCache('test:cache', fetcher)
    await new Promise((r) => setTimeout(r, 10))

    // Fetcher appelé une seule fois — deuxième appel depuis le cache
    expect(fetcher).toHaveBeenCalledTimes(1)
    expect(data.value).toEqual([{ id: 1 }])
  })

  it('force=true bypasses the cache', async () => {
    const fetcher = mockFetcher([{ id: 99 }])
    const { fetch } = useApiCache('test:force', fetcher)
    await new Promise((r) => setTimeout(r, 10))

    await fetch(true)
    expect(fetcher).toHaveBeenCalledTimes(2)
  })

  it('sets error on fetch failure', async () => {
    const fetcher = mockFetcherError()
    const { data, loading, error } = useApiCache('test:error', fetcher)

    await new Promise((r) => setTimeout(r, 10))
    expect(loading.value).toBe(false)
    expect(data.value).toBeNull()
    expect(error.value).toBeInstanceOf(Error)
    expect(error.value.message).toBe('Network Error')
  })

  it('does not fetch when eager=false', async () => {
    const fetcher = mockFetcher([])
    useApiCache('test:lazy', fetcher, { eager: false })

    await new Promise((r) => setTimeout(r, 10))
    expect(fetcher).not.toHaveBeenCalled()
  })

  it('invalidate removes entry from cache', async () => {
    const fetcher = mockFetcher([{ id: 1 }])
    const { invalidate } = useApiCache('test:invalidate', fetcher)
    await new Promise((r) => setTimeout(r, 10))

    invalidate()

    // Nouvel appel avec la même clé → refetch
    const fetcher2 = mockFetcher([{ id: 2 }])
    const { data } = useApiCache('test:invalidate', fetcher2)
    await new Promise((r) => setTimeout(r, 10))
    expect(data.value).toEqual([{ id: 2 }])
  })

  it('clearApiCache empties all entries', async () => {
    const fetcher1 = mockFetcher('a')
    const fetcher2 = mockFetcher('b')
    useApiCache('key1', fetcher1)
    useApiCache('key2', fetcher2)
    await new Promise((r) => setTimeout(r, 10))

    clearApiCache()

    const fetcher3 = mockFetcher('c')
    useApiCache('key1', fetcher3)
    await new Promise((r) => setTimeout(r, 10))
    expect(fetcher3).toHaveBeenCalledTimes(1)
  })

  it('respects custom TTL', async () => {
    const fetcher = mockFetcher([{ id: 1 }])
    // TTL de 1ms → expiré immédiatement
    useApiCache('test:ttl', fetcher, { ttl: 1 })
    await new Promise((r) => setTimeout(r, 10))

    const fetcher2 = mockFetcher([{ id: 2 }])
    const { data } = useApiCache('test:ttl', fetcher2, { ttl: 1 })
    await new Promise((r) => setTimeout(r, 10))

    // Le cache a expiré → refetch avec fetcher2
    expect(fetcher2).toHaveBeenCalledTimes(1)
    expect(data.value).toEqual([{ id: 2 }])
  })
})
