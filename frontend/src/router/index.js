import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Idea from '@/view/Idea.vue'
import IssueList from '@/view/IssueList.vue'
import IssueAdd from '@/view/IssueAdd.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/idea/:id', name: 'Idea', component: Idea },
  { path: '/issuelist', name: 'IssueList', component: IssueList },
  { path: '/issueadd', name: 'IssueAdd', component: IssueAdd },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
