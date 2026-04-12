import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Idea from '@/view/Idea.vue'
import IssueList from '@/view/IssueList.vue'

const routes = [
  { path: ''+link_prefix, name: 'Home', component: Home },
  { path: link_prefix+'/idea/:id', name: 'Idea', component: Idea },
  { path: link_prefix+'/issuelist', name: 'IssueList', component: IssueList },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
