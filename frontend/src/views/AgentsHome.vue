<template>
  <div class="agents-page">
    <!-- 科技感背景 -->
    <div class="tech-bg">
      <div class="grid-lines"></div>
      <div class="glow-orb"></div>
    </div>
    
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <div class="nav">
          <a href="/" class="logo">
            <svg class="logo-mark" viewBox="0 0 32 32" width="24" height="24">
              <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/>
              <circle cx="16" cy="12" r="3" fill="currentColor"/>
              <circle cx="10" cy="20" r="2" fill="currentColor"/>
              <circle cx="22" cy="20" r="2" fill="currentColor"/>
            </svg>
            <span class="logo-text">知枢</span>
          </a>
          <div class="nav-tabs">
            <span class="active">识客</span>
            <a href="/tgmeng">热榜</a>
          </div>
          <button @click="toggleDark" class="dark-toggle" :title="isDark ? '切换亮色模式' : '切换暗黑模式'">
            <svg v-if="isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/>
              <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- 搜索 -->
    <section class="search-section">
      <div class="container">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="搜索智能体..."
            @input="doSearch"
          />
        </div>
      </div>
    </section>

    <!-- 分类 -->
    <section class="categories">
      <div class="container">
        <div class="category-list">
          <button 
            @click="selectCategory(null)"
            :class="['cat-btn', { active: !selectedCategory }]"
          >
            全部
          </button>
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectCategory(cat.id)"
            :class="['cat-btn', { active: selectedCategory === cat.id }]"
          >
            {{ cat.icon }} {{ cat.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- 智能体列表 -->
    <main class="main">
      <div class="container">
        <div class="agents-grid">
          <div 
            v-for="agent in filteredAgents" 
            :key="agent.id"
            class="agent-card"
            @click="goToChat(agent)"
          >
            <div class="card-icon">{{ agent.icon }}</div>
            <h3 class="card-name">{{ agent.name }}</h3>
            <p class="card-desc">{{ agent.description }}</p>
            <div class="card-meta">
              <span class="rating">⭐ {{ agent.rating }}</span>
              <span class="chat-count">{{ agent.chat_count }} 次对话</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 暗黑模式
const isDark = ref(false)

// 函数定义必须在使用前
const updateTheme = () => {
  localStorage.setItem('darkMode', isDark.value)
  document.documentElement.classList.toggle('dark', isDark.value)
}

const toggleDark = () => {
  isDark.value = !isDark.value
}

onMounted(() => {
  const saved = localStorage.getItem('darkMode')
  if (saved) {
    isDark.value = saved === 'true'
  } else {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  updateTheme()
})

watch(isDark, updateTheme)

const categories = ref([])
const agents = ref([])
const selectedCategory = ref(null)
const searchQuery = ref('')

const filteredAgents = computed(() => {
  let result = agents.value
  if (selectedCategory.value) {
    result = result.filter(a => a.category_id === selectedCategory.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(a => 
      a.name.toLowerCase().includes(q) || 
      a.description.toLowerCase().includes(q)
    )
  }
  return result
})

const selectCategory = (catId) => {
  selectedCategory.value = catId
}

const doSearch = () => {
  // 已通过 computed 自动过滤
}

const goToChat = (agent) => {
  router.push(`/chat/${agent.id}`)
}

const loadData = async () => {
  const [catRes, agentRes] = await Promise.all([
    fetch('/api/categories'),
    fetch('/api/agents')
  ])
  categories.value = await catRes.json()
  agents.value = await agentRes.json()
}

onMounted(loadData)
</script>

<style scoped>
/* 科技感背景 */
.tech-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.grid-lines {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(79, 70, 229, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(79, 70, 229, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: grid-pulse 10s ease-in-out infinite;
}

@keyframes grid-pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.glow-orb {
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.15) 0%, transparent 70%);
  top: 50%;
  right: -100px;
  transform: translateY(-50%);
  animation: orb-float 8s ease-in-out infinite;
  filter: blur(40px);
}

@keyframes orb-float {
  0%, 100% { transform: translateY(-50%) scale(1); }
  50% { transform: translateY(-60%) scale(1.2); }
}

.agents-page {
  min-height: 100vh;
  background: var(--bg);
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* 头部 */
.header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text);
}

.logo-mark { color: var(--primary); }
.logo-text { font-size: 15px; font-weight: 600; }

.nav-tabs {
  display: flex;
  gap: 24px;
}

.nav-tabs a, .nav-tabs span {
  font-size: 14px;
  color: var(--text-muted);
  text-decoration: none;
  cursor: pointer;
}

.nav-tabs .active {
  color: var(--text);
  font-weight: 500;
}

/* 搜索 */
.search-section {
  padding: 20px 0;
}

.search-box {
  display: flex;
  align-items: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 16px;
}

.search-icon {
  color: var(--text-muted);
  margin-right: 12px;
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  color: var(--text);
  outline: none;
}

.search-box input::placeholder {
  color: var(--text-muted);
}

/* 分类 */
.categories {
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.category-list {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 4px 0;
}

.cat-btn {
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-muted);
  cursor: pointer;
  white-space: nowrap;
}

.cat-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.cat-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
}

/* 智能体网格 */
.main {
  padding: 24px 0;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.agent-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.agent-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--primary), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.agent-card:hover {
  transform: translateY(-5px);
  border-color: rgba(79, 70, 229, 0.3);
  box-shadow: 
    0 10px 30px rgba(79, 70, 229, 0.2),
    0 0 20px rgba(79, 70, 229, 0.1);
}

.agent-card:hover::before {
  opacity: 1;
}

.card-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.card-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--text);
}

.card-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0 0 12px;
  line-height: 1.5;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
}

.rating {
  color: #F59E0B;
}

/* 响应式 */
@media (max-width: 768px) {
  .agents-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .nav-tabs {
    gap: 16px;
  }
  
  .nav-tabs span,
  .nav-tabs a {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .agents-grid {
    grid-template-columns: 1fr;
  }
  
  .header .container {
    padding: 0 12px;
  }
  
  .nav {
    gap: 8px;
  }
  
  .nav-tabs {
    gap: 12px;
  }
  
  .nav-tabs span,
  .nav-tabs a {
    font-size: 12px;
  }
  
  .dark-toggle {
    padding: 4px 8px;
  }
  
  .dark-toggle svg {
    width: 16px;
    height: 16px;
  }
}
</style>