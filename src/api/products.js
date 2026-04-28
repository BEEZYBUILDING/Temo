import api from './client'

export const productsApi = {
  list: (params) => api.get('/products/', { params }),
  detail: (id) => api.get(`/products/${id}/detail/`),
  create: (data) => api.post('/products/', data),
  update: (id, data) => api.put(`/products/${id}/`, data),
  delete: (id) => api.delete(`/products/${id}/`),
  addVariant: (id, data) => api.post(`/products/${id}/variants/`, data),
  updateVariant: (id, variantId, data) => api.put(`/products/${id}/variants/${variantId}/`, data),
  addImage: (id, data) => api.post(`/products/${id}/images/`, data),
}
