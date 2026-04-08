<template>
  <div class="tgmeng-app">
    <!-- 顶部导航 -->
    <header class="tgmeng-header">
      <div class="tgmeng-container">
        <div class="tgmeng-header-inner">
          <!-- Logo -->
          <div class="tgmeng-logo">
            <span class="tgmeng-logo-icon">🍭</span>
            <span class="tgmeng-logo-text">糖果梦热榜</span>
          </div>
          
          <!-- 分类导航 -->
          <nav class="tgmeng-nav">
            <div class="tgmeng-nav-scroll">
              <button 
                v-for="cat in categories" 
                :key="cat.id"
                @click="selectCategory(cat.id)"
                :class="['tgmeng-nav-item', { active: selectedCategory === cat.id }]"
              >
                <span>{{ cat.icon }}</span>
                <span>{{ cat.name }}</span>
              </button>
            </div>
          </nav>
          
          <!-- 搜索框 -->
          <div class="tgmeng-search">
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="搜索热点..."
              @keyup.enter="search"
            />
            <button @click="search" class="tgmeng-search-btn">🔍</button>
          </div>
        </div>
      </div>
    </header>

    <!-- 工具栏 -->
    <div class="tgmeng-toolbar">
      <div class="tgmeng-container">
        <div class="tgmeng-toolbar-inner">
          <!-- 模式切换 -->
          <div class="tgmeng-modes">
            <button 
              @click="mode = 'ai'"
              :class="['tgmeng-mode-btn', { active: mode === 'ai' }]"
            >
              🤖 AI模式
            </button>
            <button 
              @click="mode = 'sugar'"
              :class="['tgmeng-mode-btn', { active: mode === 'sugar' }]"
            >
              🍭 糖果模式
            </button>
          </div>
          
          <!-- 排序 -->
          <div class="tgmeng-sort">
            <span class="tgmeng-sort-label">排序：</span>
            <button 
              v-for="s in sortOptions" 
              :key="s.value"
              @click="sortBy(s.value)"
              :class="['tgmeng-sort-btn', { active: currentSort === s.value }]"
            >
              {{ s.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容 -->
    <main class="tgmeng-main">
      <div class="tgmeng-container">
        <!-- AI 分析面板 -->
        <div v-if="mode === 'ai' && aiSummary" class="tgmeng-ai-panel">
          <div class="tgmeng-ai-header">
            <span class="tgmeng-ai-icon">🤖</span>
            <span class="tgmeng-ai-title">AI 实时简报</span>
          </div>
          <p class="tgmeng-ai-content">{{ aiSummary }}</p>
          <div class="tgmeng-ai-meta">
            <span>📈 热点趋势：上升</span>
            <span>⏰ {{ lastUpdate }}</span>
          </div>
        </div>

        <!-- 热榜列表 -->
        <div class="tgmeng-list">
          <div 
            v-for="(topic, index) in topics" 
            :key="topic.id"
            class="tgmeng-list-item"
            @click="openTopic(topic)"
          >
            <!-- 排名 -->
            <div class="tgmeng-rank">
              <span v-if="index < 3" :class="['tgmeng-rank-badge', `rank-${index + 1}`]">
                {{ index + 1 }}
              </span>
              <span v-else class="tgmeng-rank-num">{{ index + 1 }}</span>
            </div>
            
            <!-- 内容 -->
            <div class="tgmeng-content">
              <h3 class="tgmeng-title">{{ topic.title }}</h3>
              <div class="tgmeng-meta">
                <span class="tgmeng-source">{{ topic.source }}</span>
                <span class="tgmeng-category">{{ topic.category }}</span>
              </div>
            </div>
            
            <!-- 数据 -->
            <div class="tgmeng-stats">
              <span>👁 {{ formatNumber(topic.view_count) }}</span>
              <span>💬 {{ topic.comment_count }}</span>
            </div>
            
            <!-- 糖果指数 -->
            <div class="tgmeng-sugar">
              <div class="tgmeng-sugar-num">{{ topic.sugar_index }}</div>
              <div class="tgmeng-sugar-label">糖果指数</div>
            </div>
          </div>
        </div>

        <!-- 加载更多 -->
        <div class="tgmeng-more">
          <button @click="loadMore" class="tgmeng-more-btn">加载更多</button>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="tgmeng-footer">
      <div class="tgmeng-container">
        <div class="tgmeng-footer-content">
          <p class="tgmeng-footer-logo">🍭 糖果梦热榜</p>
          <p class="tgmeng-footer-slogan">科技不该冰冷，人性不该傲慢</p>
          <p class="tgmeng-footer-info">数据来源：微博、知乎、抖音等 200+ 平台 · 每分钟更新</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

interface Category { id: number; name: string; icon: string }
interface Topic { id: number; title: string; url: string; source: string; category: string; score: number; view_count: number; comment_count: number; sugar_index: number }

const categories = ref<Category[]>([])
const topics = ref<Topic[]>([])
const searchQuery = ref('')
const mode = ref('sugar')
const currentSort = ref('hot')
const selectedCategory = ref<number | null>(null)
const lastUpdate = ref('')
const aiSummary = ref('')

const sortOptions = [
  { label: '🔥 热门', value: 'hot' },
  { label: '🍭 指数', value: 'sugar' },
  { label: '🕐 最新', value: 'new' },
]

const formatNumber = (num: number) => num >= 10000 ? (num / 10000).toFixed(1) + 'w' : num >= 1000 ? (num / 1000).toFixed(1) + 'k' : num
const selectCategory = (catId: number | null) => { selectedCategory.value = selectedCategory.value === catId ? null : catId; loadTopics() }
const loadCategories = async () => { categories.value = await (await fetch('/api/categories')).json() }
const loadTopics = async () => {
  const params = new URLSearchParams()
  params.append('sort', currentSort.value)
  if (selectedCategory.value) params.append('category', selectedCategory.value.toString())
  topics.value = await (await fetch(`/api/topics?${params}`)).json()
}
const search = async () => { if (searchQuery.value.trim()) topics.value = await (await fetch(`/api/search?q=${encodeURIComponent(searchQuery.value)}`)).json() }
const sortBy = (sort: string) => { currentSort.value = sort; loadTopics() }
const loadMore = () => {}
const openTopic = (topic: Topic) => { window.open(topic.url, '_blank') }

watch(mode, (newMode) => { if (newMode === 'ai' && topics.value.length > 0) aiSummary.value = `当前全网热点主要集中在科技和财经领域。${topics.value[0]?.title}位居榜首，热度持续上升。` })

onMounted(async () => { await Promise.all([loadCategories(), loadTopics()]); lastUpdate.value = new Date().toLocaleTimeString() })
</script>

<style scoped>
/* 全局样式 */
.tgmeng-app {
  min-height: 100vh;
  background: #F5F5F5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

.tgmeng-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* 顶部导航 */
.tgmeng-header {
  background: #FFFFFF;
  border-bottom: 1px solid #E5E5E5;
  position: sticky;
  top: 0;
  z-index: 100;
}

.tgmeng-header-inner {
  display: flex;
  align-items: center;
  height: 56px;
}

.tgmeng-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.tgmeng-logo-icon {
  font-size: 24px;
}

.tgmeng-logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #1A1A1A;
}

.tgmeng-nav {
  flex: 1;
  margin: 0 24px;
  overflow: hidden;
}

.tgmeng-nav-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none;
}

.tgmeng-nav-scroll::-webkit-scrollbar {
  display: none;
}

.tgmeng-nav-item {
  padding: 6px 16px;
  border-radius: 16px;
  border: none;
  background: transparent;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tgmeng-nav-item:hover {
  background: #F5F5F5;
}

.tgmeng-nav-item.active {
  background: #1890FF;
  color: #FFFFFF;
}

.tgmeng-search {
  display: flex;
  align-items: center;
  position: relative;
  flex-shrink: 0;
}

.tgmeng-search input {
  width: 180px;
  height: 32px;
  padding: 0 36px 0 12px;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  transition: all 0.2s;
}

.tgmeng-search input:focus {
  border-color: #1890FF;
}

.tgmeng-search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

/* 工具栏 */
.tgmeng-toolbar {
  background: #FFFFFF;
  border-bottom: 1px solid #E5E5E5;
  padding: 12px 0;
}

.tgmeng-toolbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tgmeng-modes {
  display: flex;
  gap: 8px;
}

.tgmeng-mode-btn {
  padding: 6px 16px;
  border-radius: 6px;
  border: none;
  background: #F5F5F5;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.tgmeng-mode-btn:hover {
  background: #EBEBEB;
}

.tgmeng-mode-btn.active {
  background: #1890FF;
  color: #FFFFFF;
}

.tgmeng-sort {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tgmeng-sort-label {
  color: #999;
  font-size: 13px;
}

.tgmeng-sort-btn {
  padding: 4px 12px;
  border: none;
  background: transparent;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.tgmeng-sort-btn:hover {
  color: #333;
}

.tgmeng-sort-btn.active {
  color: #1890FF;
  font-weight: 500;
}

/* 主内容 */
.tgmeng-main {
  padding: 20px 0;
}

/* AI 面板 */
.tgmeng-ai-panel {
  background: linear-gradient(135deg, #F3E5F5 0%, #FCE4EC 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
}

.tgmeng-ai-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.tgmeng-ai-icon {
  font-size: 20px;
}

.tgmeng-ai-title {
  font-size: 16px;
  font-weight: 600;
  color: #1A1A1A;
}

.tgmeng-ai-content {
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.tgmeng-ai-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #999;
}

/* 热榜列表 */
.tgmeng-list {
  background: #FFFFFF;
  border-radius: 12px;
  overflow: hidden;
}

.tgmeng-list-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #F0F0F0;
  cursor: pointer;
  transition: background 0.2s;
}

.tgmeng-list-item:last-child {
  border-bottom: none;
}

.tgmeng-list-item:hover {
  background: #FAFAFA;
}

.tgmeng-rank {
  width: 32px;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
}

.tgmeng-rank-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.tgmeng-rank-badge.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #8B4513;
}

.tgmeng-rank-badge.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
  color: #333;
}

.tgmeng-rank-badge.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #8B4513);
  color: #FFF;
}

.tgmeng-rank-num {
  color: #999;
  font-size: 14px;
  font-weight: 500;
}

.tgmeng-content {
  flex: 1;
  min-width: 0;
  margin: 0 16px;
}

.tgmeng-title {
  font-size: 15px;
  font-weight: 500;
  color: #1A1A1A;
  margin: 0 0 6px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 0.2s;
}

.tgmeng-list-item:hover .tgmeng-title {
  color: #1890FF;
}

.tgmeng-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.tgmeng-source {
  color: #1890FF;
}

.tgmeng-category {
  color: #999;
}

.tgmeng-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #999;
  flex-shrink: 0;
}

.tgmeng-sugar {
  text-align: center;
  flex-shrink: 0;
  margin-left: 20px;
}

.tgmeng-sugar-num {
  font-size: 16px;
  font-weight: 600;
  color: #FF6B6B;
}

.tgmeng-sugar-label {
  font-size: 10px;
  color: #CCC;
  margin-top: 2px;
}

/* 加载更多 */
.tgmeng-more {
  text-align: center;
  margin-top: 20px;
}

.tgmeng-more-btn {
  padding: 10px 24px;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  background: #FFFFFF;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.tgmeng-more-btn:hover {
  border-color: #1890FF;
  color: #1890FF;
}

/* Footer */
.tgmeng-footer {
  background: #FFFFFF;
  border-top: 1px solid #E5E5E5;
  padding: 32px 0;
  margin-top: 40px;
}

.tgmeng-footer-content {
  text-align: center;
}

.tgmeng-footer-logo {
  font-size: 16px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 8px 0;
}

.tgmeng-footer-slogan {
  font-size: 14px;
  color: #666;
  margin: 0 0 8px 0;
}

.tgmeng-footer-info {
  font-size: 12px;
  color: #999;
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .tgmeng-nav {
    margin: 0 12px;
  }
  
  .tgmeng-search input {
    width: 120px;
  }
  
  .tgmeng-stats {
    display: none;
  }
  
  .tgmeng-sugar {
    margin-left: 12px;
  }
}
</style>