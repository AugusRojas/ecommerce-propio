import { api } from './api'

export const getAccessToken = () => (typeof window === 'undefined' ? null : localStorage.getItem('access_token'))
export const getRefreshToken = () => (typeof window === 'undefined' ? null : localStorage.getItem('refresh_token'))

export const saveAuth = (access: string, refresh: string) => {
  if (typeof window === 'undefined') return
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}

export const logout = () => {
  if (typeof window === 'undefined') return
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export async function login(email: string, password: string) {
  const { data } = await api.post('/api/auth/login', { email, password })
  saveAuth(data.access_token, data.refresh_token)
  return data
}

export async function register(payload: { first_name: string; last_name: string; email: string; password: string }) {
  const { data } = await api.post('/api/auth/register', payload)
  saveAuth(data.access_token, data.refresh_token)
  return data
}

export async function forgotPassword(email: string) {
  const { data } = await api.post('/api/auth/forgot-password', { email })
  return data
}

export async function resetPassword(token: string, newPassword: string) {
  const { data } = await api.post('/api/auth/reset-password', { token, new_password: newPassword })
  return data
}
