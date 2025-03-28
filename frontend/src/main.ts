import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// Create the app instance
const app = createApp(App)

// Register router
app.use(router)

// Mount the app
app.mount('#app')
