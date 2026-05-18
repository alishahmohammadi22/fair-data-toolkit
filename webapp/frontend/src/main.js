import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HomeView from './views/HomeView.vue'
import AssessView from './views/AssessView.vue'
import ResultView from './views/ResultView.vue'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/assess/:id', component: AssessView, name: 'assess' },
    { path: '/result/:id', component: ResultView, name: 'result' },
  ],
})

createApp(App).use(router).mount('#app')
