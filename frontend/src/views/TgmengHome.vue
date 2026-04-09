<template>
  <div class="hot-page">
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <a href="/" class="logo">
          <svg class="logo-mark" viewBox="0 0 32 32" width="24" height="24">
            <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/>
            <circle cx="16" cy="12" r="3" fill="currentColor"/>
            <circle cx="10" cy="20" r="2" fill="currentColor"/>
            <circle cx="22" cy="20" r="2" fill="currentColor"/>
          </svg>
          <span class="logo-text">知枢热榜</span>
        </a>
        <a href="/" class="back-link">返回首页</a>
      </div>
    </header>

    <!-- 分类 -->
    <nav class="categories">
      <div class="container">
        <div class="cat-scroll">
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectSource(cat.id)"
            :class="['cat-btn', { active: currentSource === cat.id }]"
          >
            {{ cat.name }}
          </button>
        </div>
      </div>
    </nav>

    <!-- 热榜信息 -->
    <div class="source-info" v-if="currentData">
      <div class="container">
        <div class="info-left">
          <h1>{{ currentData.title }}</h1>
          <p>{{ currentData.description }}</p>
        </div>
        <div class="info-right">
          <span class="update-time">更新于 {{ formatTime(currentData.updateTime) }}</span>
        </div>
      </div>
    </div>

    <!-- 热榜列表 -->
    <main class="main">
      <div class="container">
        <div class="list">
          <a 
            v-for="(item, idx) in hotList" 
            :key="item.id"
            :href="item.url"
            target="_blank"
            class="list-item"
          >
            <div class="item-rank">
              <span v-if="idx < 3" :class="['rank-badge', 'rank-' + (idx + 1)]">{{ idx + 1 }}</span>
              <span v-else class="rank-num">{{ idx + 1 }}</span>
            </div>
            <div class="item-content">
              <h3 class="item-title">{{ item.title }}</h3>
              <p class="item-desc" v-if="item.desc && item.desc !== item.title">{{ item.desc }}</p>
            </div>
            <div class="item-meta">
              <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="#999" stroke-width="1.5">
                <path d="M8 1v8M4 5l4 4 4-4"/>
                <path d="M2 11v2a1 1 0 001 1h10a1 1 0 001-1v-2"/>
              </svg>
            </div>
          </a>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>知枢热榜 · 实时聚合全网热点</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = '/api/hot'

const categories = ref([
  { id: 'weibo', name: '微博' },
  { id: 'zhihu', name: '知乎' },
  { id: 'bilibili', name: 'B站' },
  { id: 'douyin', name: '抖音' },
  { id: 'baidu', name: '百度' },
  { id: 'toutiao', name: '头条' },
  { id: 'weixin', name: '微信' },
  { id: 'zhihu-daily', name: '知乎日报' },
])

const currentSource = ref('weibo')
const currentData = ref(null)
const hotList = ref([])

const formatTime = (t) => {
  if (!t) return ''
  const d = new Date(t)
  return d.getHours() + ':' + String(d.getMinutes()).padStart(2, '0')
}

const loadData = async (source) => {
  try {
    const res = await fetch(`${API_BASE}/${source}`)
    const json = await res.json()
    if (json.code === 200) {
      currentData.value = json
      hotList.value = json.data || []
    }
  } catch (e) {
    console.error('加载失败:', e)
  }
}

const selectSource = (source) => {
  currentSource.value = source
  loadData(source)
}

onMounted(() => {
  loadData('weibo')
})
</script>

<style scoped>
/* 基础 */
.hot-page {
  min-height: 100vh;
  background: #fafafa;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 头部 */
.header {
  background: #fff;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #1a1a1a;
}

.logo-mark {
  color: #4F46E5;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
}

.back-link {
  font-size: 13px;
  color: #666;
  text-decoration: none;
}

.back-link:hover {
  color: #1a1a1a;
}

/* 分类 */
.categories {
  background: #fff;
  border-bottom: 1px solid #eee;
}

.cat-scroll {
  display: flex;
  gap: 4px;
  overflow-x: auto;
  padding: 12px 0;
}

.cat-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: none;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  white-space: nowrap;
}

.cat-btn:hover {
  background: #eee;
}

.cat-btn.active {
  background: #1a1a1a;
  color: #fff;
}

/* 数据源信息 */
.source-info {
  background: #fff;
  padding: 24px 0;
  border-bottom: 1px solid #eee;
}

.source-info .container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.info-left h1 {
  font-size: 20px;
  margin: 0 0 6px;
}

.info-left p {
  font-size: 13px;
  color: #666;
  margin: 0;
}

.update-time {
  font-size: 12px;
  color: #999;
}

/* 列表 */
.main {
  padding: 20px 0;
}

.list {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #eee;
}

.list-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-bottom: 1px solid #f5f5f5;
  text-decoration: none;
  color: inherit;
}

.list-item:last-child {
  border-bottom: none;
}

.list-item:hover {
  background: #fafafa;
}

.list-item:hover .item-title {
  color: #4F46E5;
}

/* 排名 */
.item-rank {
  width: 28px;
  flex-shrink: 0;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.rank-badge.rank-1 {
  background: #F59E0B;
  color: #fff;
}

.rank-badge.rank-2 {
  background: #9CA3AF;
  color: #fff;
}

.rank-badge.rank-3 {
  background: #B45309;
  color: #fff;
}

.rank-num {
  color: #999;
  font-size: 14px;
  font-weight: 500;
}

/* 内容 */
.item-content {
  flex: 1;
  padding: 0 16px;
}

.item-title {
  font-size: 15px;
  font-weight: 500;
  color: #1a1a1a;
  margin: 0 0 4px;
  transition: color 0.2s;
}

.item-desc {
  font-size: 13px;
  color: #666;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.2s;
}

.list-item:hover .item-meta {
  opacity: 1;
}

/* Footer */
.footer {
  padding: 32px 0;
  text-align: center;
  color: #999;
  font-size: 13px;
}

/* 响应式 */
@media (max-width: 600px) {
  .source-info .container {
    flex-direction: column;
    gap: 8px;
  }
  
  .item-desc {
    display: none;
  }
}
</style>