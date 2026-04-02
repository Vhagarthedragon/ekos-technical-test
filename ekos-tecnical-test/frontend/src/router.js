import { createRouter, createWebHistory } from 'vue-router'
import SupportView from './views/SupportView.vue'
import SalesView from './views/SalesView.vue'
import AdminView from './views/AdminView.vue'

const routes = [
  { path: '/', redirect: '/support' },
  { path: '/support', component: SupportView },
  { path: '/sales', component: SalesView },
  { path: '/admin', component: AdminView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
