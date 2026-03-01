import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000,
})

api.interceptors.response.use(
  res => res,
  err => {
    const msg = err.response?.data?.detail || err.message || 'Error de red'
    console.error('[API Error]', msg)
    return Promise.reject(new Error(msg))
  }
)

export default api
