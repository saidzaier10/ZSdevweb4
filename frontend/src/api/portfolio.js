import api from './axios.js'

export const portfolioApi = {
  getProjects: () => api.get('/api/v1/portfolio/projects/'),
  getTestimonials: () => api.get('/api/v1/portfolio/testimonials/'),
}
