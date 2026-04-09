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
        <span class="update-time">{{ updateTime }}</span>
      </div>
    </header>

    <!-- 热榜网格 -->
    <main class="main">
      <div class="container">
        <div class="hot-grid">
          <div v-for="source in displaySources" :key="source.id" class="hot-card">
            <div class="card-header">
              <h2 class="card-title">{{ source.name }}</h2>
              <a :href="source.link" target="_blank" class="card-link">更多 →</a>
            </div>
            <div class="card-list">
              <a 
                v-for="(item, idx) in source.items" 
                :key="item.id"
                :href="item.url"
                target="_blank"
                class="list-item"
              >
                <span class="item-rank" :class="'rank-' + (idx + 1)">{{ idx + 1 }}</span>
                <span class="item-title">{{ item.title }}</span>
              </a>
              <div v-if="!source.items || source.items.length === 0" class="loading">
                加载中...
              </div>
            </div>
          </div>
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

// 要显示的数据源
const displaySources = ref([
  { id: 'weibo', name: '微博', link: 'https://s.weibo.com/top/summary/', items: [] },
  { id: 'zhihu', name: '知乎', link: 'https://www.zhihu.com/hot', items: [] },
  { id: 'douyin', name: '抖音', link: 'https://www.douyin.com/hot', items: [] },
  { id: 'bilibili', name: 'B站', link: 'https://www.bilibili.com/v/popular/rank/all', items: [] },
  { id: 'toutiao', name: '头条', link: 'https://www.toutiao.com/', items: [] },
  { id: 'baidu', name: '百度', link: 'https://top.baidu.com/board', items: [] },
  { id: 'kuaishou', name: '快手', link: 'https://www.kuaishou.com/hot', items: [] },
  { id: 'tieba', name: '贴吧', link: 'https://tieba.baidu.com/hottopic', items: [] },
])

const updateTime = ref('')

const loadAllData = async () => {
  const time = new Date()
  updateTime.value = time.getHours() + ':' + String(time.getMinutes()).padStart(2, '0')
  
  // 并行加载所有数据源
  await Promise.all(
    displaySources.value.map(async (source) => {
      try {
        const res = await fetch(`${API_BASE}/${source.id}`)
        const json = await res.json()
        if (json.code === 200 && json.data) {
          source.items = json.data.slice(0, 5) // 每个平台只显示前5条
        }
      } catch (e) {
        console.error(`加载 ${source.name} 失败:`, e)
      }
    })
  )
}

onMounted(() => {
  loadAllData()
})
</script>

<style scoped>
/* 基础 */
.hot-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
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
  height: 52px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #1a1a1a;
}

.logo-mark { color: #4F46E5; }
.logo-text { font-size: 15px; font-weight: 600; }

.update-time {
  font-size: 12px;
  color: #999;
}

/* 热榜网格 */
.main {
  padding: 20px 0;
}

.hot-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

/* 卡片 */
.hot-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
}

.card-link {
  font-size: 12px;
  color: #999;
  text-decoration: none;
}

.card-link:hover {
  color: #4F46E5;
}

/* 列表 */
.card-list {
  padding: 8px 0;
}

.list-item {
  display: flex;
  align-items: flex-start;
  padding: 10px 16px;
  text-decoration: none;
  color: #1a1a1a;
}

.list-item:hover {
  background: #fafafa;
}

.list-item:hover .item-title {
  color: #4F46E5;
}

.item-rank {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  color: #999;
  flex-shrink: 0;
}

.item-rank.rank-1 { color: #F59E0B; }
.item-rank.rank-2 { color: #9CA3AF; }
.item-rank.rank-3 { color: #B45309; }

.item-title {
  font-size: 13px;
  line-height: 1.4;
  margin-left: 10px;
  transition: color 0.2s;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.loading {
  padding: 20px;
  text-align: center;
  color: #999;
  font-size: 13px;
}

/* Footer */
.footer {
  padding: 32px 0;
  text-align: center;
  color: #999;
  font-size: 13px;
}

/* 响应式 */
@media (max-width: 900px) {
  .hot-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .hot-grid {
    grid-template-columns: 1fr;
  }
}
</style>