import { createRouter, createWebHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import UploadPage from '../views/UploadPage.vue'
import ResultsPage from '../views/ResultsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Upload',
    component: UploadPage,
  },
  {
    path: '/results',
    name: 'Results',
    component: ResultsPage,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router 