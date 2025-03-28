import { createRouter, createWebHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import UploadPage from '../views/UploadPage.vue'
import ResultsPage from '../views/ResultsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Upload',
    component: UploadPage,
    meta: {
      title: 'Upload Schedules'
    }
  },
  {
    path: '/results',
    name: 'Results',
    component: ResultsPage,
    meta: {
      title: 'Analysis Results'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Update page title based on route
router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  document.title = `${to.meta.title as string} | Queen's Schedule Analyzer` || 'Queen\'s Schedule Analyzer'
  next()
})

export default router 