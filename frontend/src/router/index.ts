import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // 门户首页
    {
      path: '/',
      name: 'Portal',
      component: () => import('../views/Portal.vue'),
      meta: { title: '知枢 · 知识聚合平台' }
    },
    
    // 知枢智能体平台
    {
      path: '/agents',
      name: 'AgentsHome',
      component: () => import('../views/AgentsHome.vue'),
      meta: { title: '识客 - 知枢' }
    },
    {
      path: '/agents/category',
      name: 'AgentsCategory',
      component: () => import('../views/AgentsCategory.vue'),
      meta: { title: '分类 - 知枢·识客' }
    },
    // 详情页已删除（2026-04-10 决策：点击卡片直接对话）
    // 旧链接重定向到对话页
    {
      path: '/agents/:id',
      redirect: to => `/chat/${to.params.id}`
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
      meta: { title: '知枢·看点' }
    },
    {
      path: '/tgmeng/category/:id',
      name: 'TgmengCategory',
      component: () => import('../views/TgmengCategory.vue'),
      meta: { title: '分类 - 知枢·看点' }
    },
    {
      path: '/tgmeng/topic/:id',
      name: 'TgmengTopic',
      component: () => import('../views/TgmengTopic.vue'),
      meta: { title: '热点详情 - 知枢·看点' }
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