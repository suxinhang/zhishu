<template>
  <div class="agents-page">
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
            <span class="active">智能体</span>
            <a href="/tgmeng">热榜</a>
          </div>
        </div>
      </div>
    </header>

    <!-- 搜索 -->
    <section class="search-section">
      <div class="container">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#999" stroke-width="2">
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
            {{ cat.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- 推荐 -->
    <section class="featured" v-if="!searchQuery">
      <div class="container">
        <div class="section-header">
          <h2>热门推荐</h2>
        </div>
        <div class="featured-grid">
          <div 
            v-for="agent in featuredAgents" 
            :key="agent.id"
            class="featured-card"
            @click="goToChat(agent)"
          >
            <div class="featured-icon">
              <svg viewBox="0 0 40 40" width="40" height="40" fill="none">
                <rect width="40" height="40" rx="10" :fill="agent.color"/>
                <circle cx="20" cy="16" r="6" stroke="#fff" stroke-width="2"/>
                <path d="M10 32c0-5 4-8 10-8s10 3 10 8" stroke="#fff" stroke-width="2"/>
              </svg>
            </div>
            <div class="featured-info">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
              <div class="featured-meta">
                <span class="rating">
                  <svg viewBox="0 0 16 16" width="14" height="14" fill="#F59E0B">
                    <path d="M8 0l2.5 5 5.5.8-4 3.8 1 5.4-5-2.6-5 2.6 1-5.4-4-3.8 5.5-.8z"/>
                  </svg>
                  {{ agent.rating }}
                </span>
                <span class="users">{{ formatNum(agent.users) }} 人使用</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 列表 -->
    <section class="agents-list">
      <div class="container">
        <div class="section-header">
          <h2>{{ searchQuery ? '搜索结果' : '全部智能体' }}</h2>
          <div class="sort-btns">
            <button @click="sortBy('hot')" :class="{ active: sort === 'hot' }">最热</button>
            <button @click="sortBy('rating')" :class="{ active: sort === 'rating' }">评分</button>
          </div>
        </div>
        
        <div class="agents-grid">
          <div 
            v-for="agent in filteredAgents" 
            :key="agent.id"
            class="agent-card"
            @click="goToDetail(agent)"
          >
            <div class="card-icon">
              <svg viewBox="0 0 48 48" width="48" height="48" fill="none">
                <rect width="48" height="48" rx="12" :fill="agent.color"/>
                <circle cx="24" cy="20" r="7" stroke="#fff" stroke-width="2"/>
                <path d="M12 38c0-6 5-10 12-10s12 4 12 10" stroke="#fff" stroke-width="2"/>
              </svg>
            </div>
            <div class="card-body">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
              <div class="card-tags">
                <span class="tag">{{ agent.category }}</span>
              </div>
            </div>
            <div class="card-footer">
              <div class="card-stats">
                <span>
                  <svg viewBox="0 0 16 16" width="12" height="12" fill="#F59E0B">
                    <path d="M8 0l2.5 5 5.5.8-4 3.8 1 5.4-5-2.6-5 2.6 1-5.4-4-3.8 5.5-.8z"/>
                  </svg>
                  {{ agent.rating }}
                </span>
                <span>{{ formatNum(agent.users) }}人</span>
              </div>
              <button class="chat-btn" @click.stop="goToChat(agent)">对话</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 能力 -->
    <section class="capabilities">
      <div class="container">
        <h2>智能体能力</h2>
        <div class="cap-grid">
          <div class="cap-card">
            <div class="cap-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#4F46E5" stroke-width="2">
                <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                <path d="M2 2l7.586 7.586"/>
              </svg>
            </div>
            <h3>内容创作</h3>
            <p>文案写作、小说创作、公文写作</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#4F46E5" stroke-width="2">
                <polyline points="16 18 22 12 16 6"/>
                <polyline points="8 6 2 12 8 18"/>
              </svg>
            </div>
            <h3>编程开发</h3>
            <p>代码生成、Bug修复、架构设计</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#4F46E5" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="2" y1="12" x2="22" y2="12"/>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
              </svg>
            </div>
            <h3>语言翻译</h3>
            <p>多语言互译、文档翻译</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#4F46E5" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
              </svg>
            </div>
            <h3>数据分析</h3>
            <p>数据可视化、报表生成</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>知枢 · 让智能触手可及</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const categories = ref([
  { id: 1, name: '写作' },
  { id: 2, name: '编程' },
  { id: 3, name: '翻译' },
  { id: 4, name: '设计' },
  { id: 5, name: '学习' },
  { id: 6, name: '效率' },
])

const agents = ref([
  { id: 1, name: '文案大师', description: '专业文案创作', category: '写作', rating: 4.9, users: 12580, color: '#EEF2FF' },
  { id: 2, name: '代码助手', description: '智能编程助手', category: '编程', rating: 4.8, users: 8960, color: '#ECFDF5' },
  { id: 3, name: '翻译官', description: '多语言翻译', category: '翻译', rating: 4.7, users: 15320, color: '#FEF3C7' },
  { id: 4, name: '设计精灵', description: 'AI设计助手', category: '设计', rating: 4.6, users: 6740, color: '#FCE7F3' },
  { id: 5, name: '论文帮手', description: '学术写作辅助', category: '学习', rating: 4.8, users: 9850, color: '#DBEAFE' },
  { id: 6, name: 'PPT大师', description: '演示文稿生成', category: '效率', rating: 4.5, users: 11200, color: '#F3E8FF' },
])

const searchQuery = ref('')
const selectedCategory = ref(null)
const sort = ref('hot')

const featuredAgents = computed(() => [...agents.value].sort((a, b) => b.users - a.users).slice(0, 3))

const filteredAgents = computed(() => {
  let result = agents.value
  if (selectedCategory.value) {
    result = result.filter(a => a.category === categories.value.find(c => c.id === selectedCategory.value)?.name)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(a => a.name.toLowerCase().includes(q) || a.description.toLowerCase().includes(q))
  }
  if (sort.value === 'hot') result = [...result].sort((a, b) => b.users - a.users)
  else if (sort.value === 'rating') result = [...result].sort((a, b) => b.rating - a.rating)
  return result
})

const formatNum = n => n >= 10000 ? (n/10000).toFixed(1) + 'w' : n >= 1000 ? (n/1000).toFixed(1) + 'k' : n
const selectCategory = id => { selectedCategory.value = selectedCategory.value === id ? null : id }
const sortBy = s => { sort.value = s }
const doSearch = () => {}
const goToDetail = agent => { window.location.href = '/agents/' + agent.id }
const goToChat = agent => { window.location.href = '/chat/' + agent.id }
</script>

<style scoped>
.agents-page { min-height: 100vh; background: #f8f9fa; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; }

/* Header */
.header { background: #fff; border-bottom: 1px solid #eee; }
.nav { display: flex; align-items: center; justify-content: space-between; height: 56px; }
.logo { display: flex; align-items: center; gap: 8px; text-decoration: none; color: #1a1a1a; }
.logo-mark { color: #4F46E5; }
.logo-text { font-size: 16px; font-weight: 600; }
.nav-tabs { display: flex; gap: 24px; }
.nav-tabs a, .nav-tabs span { color: #666; text-decoration: none; font-size: 14px; cursor: pointer; }
.nav-tabs .active { color: #4F46E5; font-weight: 500; }

/* Search */
.search-section { padding: 32px 0 16px; }
.search-box { position: relative; max-width: 500px; margin: 0 auto; }
.search-box input { width: 100%; padding: 14px 14px 14px 44px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; outline: none; }
.search-box input:focus { border-color: #4F46E5; }
.search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); }

/* Categories */
.categories { padding: 12px 0; }
.category-list { display: flex; gap: 10px; overflow-x: auto; }
.cat-btn { padding: 8px 18px; background: #fff; border: 1px solid #ddd; border-radius: 20px; font-size: 13px; color: #666; cursor: pointer; white-space: nowrap; }
.cat-btn:hover { border-color: #4F46E5; color: #4F46E5; }
.cat-btn.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }

/* Featured */
.featured { padding: 32px 0; }
.section-header { margin-bottom: 20px; }
.section-header h2 { font-size: 18px; margin: 0; }
.featured-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.featured-card { display: flex; align-items: center; gap: 14px; padding: 18px; background: #fff; border: 1px solid #eee; border-radius: 10px; cursor: pointer; }
.featured-card:hover { border-color: #ccc; }
.featured-info { flex: 1; }
.featured-info h3 { margin: 0 0 4px; font-size: 15px; }
.featured-info p { margin: 0; font-size: 12px; color: #666; }
.featured-meta { margin-top: 8px; font-size: 12px; color: #999; }
.rating { display: inline-flex; align-items: center; gap: 2px; color: #F59E0B; }

/* Grid */
.agents-list { padding: 32px 0; }
.sort-btns { display: flex; gap: 6px; }
.sort-btns button { padding: 5px 12px; background: #fff; border: 1px solid #ddd; border-radius: 14px; font-size: 12px; color: #666; cursor: pointer; }
.sort-btns button.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
.agents-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.agent-card { background: #fff; border: 1px solid #eee; border-radius: 10px; overflow: hidden; cursor: pointer; }
.agent-card:hover { border-color: #ccc; }
.card-icon { padding: 20px 16px 12px; }
.card-body { padding: 0 16px 12px; }
.card-body h3 { margin: 0 0 4px; font-size: 14px; }
.card-body p { margin: 0; font-size: 12px; color: #666; }
.card-tags { margin-top: 8px; }
.tag { display: inline-block; padding: 2px 8px; background: #f0f0f0; border-radius: 4px; font-size: 11px; color: #666; }
.card-footer { padding: 10px 16px; border-top: 1px solid #f5f5f5; display: flex; justify-content: space-between; align-items: center; }
.card-stats { font-size: 11px; color: #999; }
.card-stats span { margin-right: 10px; }
.chat-btn { padding: 5px 14px; background: #1a1a1a; color: #fff; border: none; border-radius: 14px; font-size: 12px; cursor: pointer; }

/* Capabilities */
.capabilities { padding: 40px 0; background: #fff; }
.capabilities h2 { text-align: center; margin: 0 0 28px; font-size: 22px; }
.cap-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.cap-card { text-align: center; padding: 20px; }
.cap-icon { width: 48px; height: 48px; background: #F5F3FF; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; }
.cap-card h3 { margin: 0 0 6px; font-size: 14px; }
.cap-card p { margin: 0; font-size: 12px; color: #666; }

/* Footer */
.footer { padding: 32px 0; text-align: center; color: #999; font-size: 13px; }

/* Responsive */
@media (max-width: 900px) {
  .featured-grid { grid-template-columns: 1fr; }
  .agents-grid { grid-template-columns: repeat(2, 1fr); }
  .cap-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .agents-grid { grid-template-columns: 1fr; }
}
</style>