import api from './client'

export const ordersApi = {
  create: (data) => api.post('/orders/', data),
  list: () => api.get('/orders/'),
  detail: (id) => api.get(`/orders/${id}/`),
  cancel: (id) => api.post(`/orders/${id}/cancel/`),
}
