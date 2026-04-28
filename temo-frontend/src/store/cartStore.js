import { create } from 'zustand'
import { cartApi } from '../api/cart'

export const useCartStore = create((set, get) => ({
  cart: null,
  itemCount: 0,
  loading: false,
  open: false,

  setOpen: (open) => set({ open }),

  fetchCart: async () => {
    set({ loading: true })
    try {
      const { data } = await cartApi.get()
      const count = data.items?.reduce((sum, i) => sum + i.quantity, 0) || 0
      set({ cart: data, itemCount: count, loading: false })
    } catch {
      set({ loading: false })
    }
  },

  addItem: async (variantId, quantity = 1) => {
    const { data } = await cartApi.add(variantId, quantity)
    // Store session token for guests
    if (data.session_token) {
      localStorage.setItem('session_token', data.session_token)
    }
    await get().fetchCart()
    set({ open: true })
  },

  updateItem: async (variantId, quantity) => {
    await cartApi.update(variantId, quantity)
    await get().fetchCart()
  },

  removeItem: async (variantId) => {
    await cartApi.remove(variantId)
    await get().fetchCart()
  },

  clearCart: async () => {
    await cartApi.clear()
    set({ cart: null, itemCount: 0 })
  },

  validate: async () => {
    const { data } = await cartApi.validate()
    return data
  },
}))
