<template>
  <div class="home-old">
    <!-- 头部 -->
    <header class="header">
      <div class="header-inner">
        <a href="/" class="logo">
          <span class="logo-icon">🧠</span>
          <span class="logo-text">知枢</span>
        </a>
        <nav class="nav">
          <router-link to="/agents/category">分类</router-link>
        </nav>
        <div class="search">
          <input v-model="query" placeholder="搜索智能体..." @keyup.enter="search" />
        </div>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="main">
      <div class="container">
        <h1 class="page-title">🧠 知枢 · 智能体平台</h1>
        
        <div class="agents-grid">
          <div v-for="agent in agents" :key="agent.id" class="agent-card" @click="goChat(agent)">
            <div class="agent-icon">{{ agent.icon }}</div>
            <div class="agent-info">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.desc }}</p>
              <span class="agent-cat">{{ agent.category }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const agents = ref([
  { id: 1, icon: '🤖', name: '写作助手', desc: '智能写作创作', category: '写作' },
  { id: 2, icon: '💻', name: '编程助手', desc: '代码生成与优化', category: '编程' },
  { id: 3, icon: '🌐', name: '翻译助手', desc: '多语言翻译', category: '翻译' },
])

const search = () => {}
const goChat = (a) => { window.location.href = '/chat/' + a.id }
</script>

<style scoped>
.home-old { min-height: 100vh; background: #f5f5f5; }
.header { background: #fff; border-bottom: 1px solid #eee; }
.header-inner { max-width: 1000px; margin: 0 auto; padding: 0 20px; height: 50px; display: flex; align-items: center; gap: 20px; }
.logo { display: flex; align-items: center; gap: 8px; text-decoration: none; color: #333; }
.logo-icon { font-size: 20px; }
.logo-text { font-size: 16px; font-weight: 600; }
.nav a { color: #666; text-decoration: none; font-size: 14px; }
.search input { padding: 6px 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 13px; width: 150px; }
.main { padding: 20px; }
.container { max-width: 1000px; margin: 0 auto; }
.page-title { font-size: 18px; margin: 0 0 20px; }
.agents-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.agent-card { background: #fff; border-radius: 8px; padding: 16px; cursor: pointer; }
.agent-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.agent-icon { font-size: 32px; margin-bottom: 8px; }
.agent-info h3 { margin: 0 0 4px; font-size: 14px; }
.agent-info p { margin: 0; font-size: 12px; color: #666; }
.agent-cat { display: inline-block; margin-top: 8px; padding: 2px 8px; background: #f0f0f0; border-radius: 4px; font-size: 11px; color: #666; }
</style>