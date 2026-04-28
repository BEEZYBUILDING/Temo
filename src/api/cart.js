import api from './client'

export const cartApi = {
  get: () => api.get('/cart/'),
  add: (variantId, quantity = 1) => api.post('/cart/', { variant_id: variantId, quantity }),
  update: (variantId, quantity) => api.put(`/cart/items/${variantId}/`, { quantity }),
  remove: (variantId) => api.delete(`/cart/items/${variantId}/`),
  clear: () => api.delete('/cart/'),
  validate: () => api.post('/cart/validate/'),
}
