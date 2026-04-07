import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Category from '../views/Category.vue'
import AgentDetail from '../views/AgentDetail.vue'
import Chat from '../views/Chat.vue'
import About from '../views/About.vue'
import TopicDetail from '../views/TopicDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/category', name: 'Category', component: Category },
    { path: '/agent/:id', name: 'AgentDetail', component: AgentDetail },
    { path: '/chat/:id', name: 'Chat', component: Chat },
    { path: '/topic/:id', name: 'TopicDetail', component: TopicDetail },
    { path: '/about', name: 'About', component: About },
  ]
})

export default router