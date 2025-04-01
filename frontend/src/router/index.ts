import { createRouter, createWebHistory } from 'vue-router'
import UploadPage from '../views/UploadPage.vue'
import ResultsPage from '../views/ResultsPage.vue'
import ChatPage from '../views/ChatPage.vue'
import HomeView from '../views/HomeView.vue'
const routes = [
  {
    path: '/upload',
    name: 'Upload',
    component: UploadPage,
  },
  {
    path: '/results',
    name: 'Results',
    component: ResultsPage,
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatPage,
  },
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router 