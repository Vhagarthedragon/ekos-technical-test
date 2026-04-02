import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
})

export const support = {
  startSession: (userIdentifier) =>
    http.post('/support/sessions', { user_identifier: userIdentifier }),
  chat: (sessionId, message) =>
    http.post(`/support/sessions/${sessionId}/chat`, { message }),
  history: (sessionId) =>
    http.get(`/support/sessions/${sessionId}/history`),
}

export const admin = {
  stats: () => http.get('/admin/stats'),
  sessions: () => http.get('/admin/sessions'),
  session: (id) => http.get(`/admin/sessions/${id}`),
  escalations: () => http.get('/admin/escalations'),
  articles: () => http.get('/admin/articles'),
  createArticle: (data) => http.post('/admin/articles', data),
  deleteArticle: (id) => http.delete(`/admin/articles/${id}`),
}

export const sales = {
  research: (clinicName, websiteUrl) =>
    http.post('/sales/research', { clinic_name: clinicName, website_url: websiteUrl || null }),
  prospects: () =>
    http.get('/sales/prospects'),
  prospect: (id) =>
    http.get(`/sales/prospects/${id}`),
  approveDraft: (draftId) =>
    http.post(`/sales/drafts/${draftId}/approve`),
}
