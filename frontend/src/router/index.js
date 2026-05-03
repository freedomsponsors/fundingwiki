import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Idea from '@/view/Idea.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/idea/:id', name: 'Idea', component: Idea },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
