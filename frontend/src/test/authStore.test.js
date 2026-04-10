/**
 * Tests du store auth Pinia.
 * Les appels API sont mockés — on teste uniquement la logique du store.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useAuthStore } from '@/stores/auth.js'

// Mock des modules externes pour éviter les imports réels d'axios / api
vi.mock('@/api/auth.js', () => ({
  authApi: {
    login: vi.fn(),
    me: vi.fn(),
    refresh: vi.fn(),
    logout: vi.fn().mockResolvedValue({}),
  },
}))

vi.mock('@/api/axios.js', () => ({
  registerAuthCallbacks: vi.fn(),
}))

vi.mock('@/composables/useApiCache.js', () => ({
  clearApiCache: vi.fn(),
}))

import { authApi } from '@/api/auth.js'
import { clearApiCache } from '@/composables/useApiCache.js'

describe('useAuthStore', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('démarre sans token ni user', () => {
    const store = useAuthStore()
    expect(store.accessToken).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('login stocke le token et appelle fetchMe', async () => {
    authApi.login.mockResolvedValue({ data: { access: 'tok-abc' } })
    authApi.me.mockResolvedValue({ data: { email: 'user@example.com' } })

    const store = useAuthStore()
    await store.login('user@example.com', 'password')

    expect(store.accessToken).toBe('tok-abc')
    expect(store.user).toEqual({ email: 'user@example.com' })
    expect(store.isAuthenticated).toBe(true)
  })

  it('logout efface le token, le user et vide le cache', () => {
    const store = useAuthStore()
    store.setAccessToken('tok-to-clear')
    store.logout()

    expect(store.accessToken).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(clearApiCache).toHaveBeenCalled()
    expect(authApi.logout).toHaveBeenCalled()
  })

  it('fetchMe appelle logout si l\'API échoue', async () => {
    authApi.me.mockRejectedValue(new Error('401'))

    const store = useAuthStore()
    store.setAccessToken('tok')
    await store.fetchMe()

    expect(store.accessToken).toBeNull()
  })

  it('setAccessToken met à jour le token', () => {
    const store = useAuthStore()
    store.setAccessToken('nouveau-token')
    expect(store.accessToken).toBe('nouveau-token')
  })

  it('tryRestoreSession restaure la session si refresh réussit', async () => {
    authApi.refresh.mockResolvedValue({ data: { access: 'refreshed-tok' } })
    authApi.me.mockResolvedValue({ data: { email: 'restored@example.com' } })

    const store = useAuthStore()
    await store.tryRestoreSession()

    expect(store.accessToken).toBe('refreshed-tok')
    expect(store.user).toEqual({ email: 'restored@example.com' })
  })

  it('tryRestoreSession ne fait rien si token déjà présent', async () => {
    const store = useAuthStore()
    store.setAccessToken('existing-tok')
    await store.tryRestoreSession()

    expect(authApi.refresh).not.toHaveBeenCalled()
  })

  it('tryRestoreSession reste anonyme si refresh échoue', async () => {
    authApi.refresh.mockRejectedValue(new Error('No cookie'))

    const store = useAuthStore()
    await store.tryRestoreSession()

    expect(store.accessToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })
})
