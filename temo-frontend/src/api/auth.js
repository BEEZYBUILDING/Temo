import api from './client'

export const authApi = {
  register: (data) => api.post('/users/register/', data),
  login: (data, sessionToken) =>
    api.post('/users/login/', data, {
      headers: sessionToken ? { 'X-Session-Token': sessionToken } : {},
    }),
  logout: (refresh) => api.post('/users/logout/', { refresh }),
  me: () => api.get('/users/me/'),
  updateMe: (data) => api.put('/users/me/', data),
  changePassword: (data) => api.post('/users/me/change-password/', data),
  getAddresses: () => api.get('/users/addresses/'),
  createAddress: (data) => api.post('/users/addresses/', data),
  updateAddress: (id, data) => api.put(`/users/addresses/${id}/`, data),
  deleteAddress: (id) => api.delete(`/users/addresses/${id}/`),
}
