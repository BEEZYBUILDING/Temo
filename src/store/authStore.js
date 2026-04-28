import { create } from 'zustand'
import { authApi } from '../api/auth'

export const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,

  initialize: async () => {
    if (!localStorage.getItem('access_token')) return
    try {
      const { data } = await authApi.me()
      set({ user: data, isAuthenticated: true })
    } catch {
      get().logout()
    }
  },

  login: async (credentials) => {
    set({ loading: true })
    const sessionToken = localStorage.getItem('session_token')
    const { data } = await authApi.login(credentials, sessionToken)
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.removeItem('session_token') // merged into user cart
    const { data: user } = await authApi.me()
    set({ user, isAuthenticated: true, loading: false })
    return user
  },

  logout: async () => {
    const refresh = localStorage.getItem('refresh_token')
    if (refresh) {
      try { await authApi.logout(refresh) } catch {}
    }
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null, isAuthenticated: false })
  },

  register: async (data) => {
    set({ loading: true })
    await authApi.register(data)
    set({ loading: false })
  },

  setLoading: (loading) => set({ loading }),
}))
