import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // 门户首页
    {
      path: '/',
      name: 'Portal',
      component: () => import('../views/Portal.vue'),
      meta: { title: '知枢 - 智能体聚合平台' }
    },
    
    // 知枢智能体平台
    {
      path: '/agents',
      name: 'AgentsHome',
      component: () => import('../views/AgentsHome.vue'),
      meta: { title: '智能体 - 知枢' }
    },
    {
      path: '/agents/category',
      name: 'AgentsCategory',
      component: () => import('../views/AgentsCategory.vue'),
      meta: { title: '分类 - 知枢' }
    },
    {
      path: '/agents/:id',
      name: 'AgentDetail',
      component: () => import('../views/AgentDetail.vue'),
      meta: { title: '智能体详情 - 知枢' }
    },
    {
      path: '/chat/:id',
      name: 'Chat',
      component: () => import('../views/Chat.vue'),
      meta: { title: '对话 - 知枢' }
    },
    
    // 知枢热榜
    {
      path: '/tgmeng',
      name: 'TgmengHome',
      component: () => import('../views/TgmengHome.vue'),
      meta: { title: '知枢热榜' }
    },
    {
      path: '/tgmeng/category/:id',
      name: 'TgmengCategory',
      component: () => import('../views/TgmengCategory.vue'),
      meta: { title: '分类 - 知枢热榜' }
    },
    {
      path: '/tgmeng/topic/:id',
      name: 'TgmengTopic',
      component: () => import('../views/TgmengTopic.vue'),
      meta: { title: '热点详情 - 知枢热榜' }
    },
    
    // 404
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFound.vue'),
      meta: { title: '页面不存在' }
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, _from, next) => {
  document.title = (to.meta?.title as string) || '知枢'
  next()
})

export default router