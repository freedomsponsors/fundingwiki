import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Idea from '@/view/Idea.vue'

const link_prefix = import.meta.env.VITE_LINK_PREFIX

const routes = [
  { path: ''+link_prefix, name: 'Home', component: Home },
  { path: link_prefix+'/idea/:id', name: 'Idea', component: Idea },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router