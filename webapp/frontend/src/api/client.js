import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

export const getIndicators = () => http.get('/indicators/')
export const createAssessment = (data) => http.post('/assessments/', data)
export const listAssessments = () => http.get('/assessments/')
export const getAssessment = (id) => http.get(`/assessments/${id}`)
export const updateScores = (id, scores) => http.put(`/assessments/${id}/scores`, scores)
export const deleteAssessment = (id) => http.delete(`/assessments/${id}`)
