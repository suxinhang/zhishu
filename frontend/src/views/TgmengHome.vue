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

    <!-- 快捷入口 -->
    <div class="quick-access">
      <div class="container">
        <div class="quick-list">
          <button 
            v-for="item in quickList" 
            :key="item.id"
            @click="selectSource(item.id)"
            :class="['quick-btn', { active: currentSource === item.id }]"
          >
            {{ item.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- 分类标签 -->
    <nav class="categories">
      <div class="container">
        <div class="cat-tabs">
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="activeCategory = cat.id"
            :class="['cat-tab', { active: activeCategory === cat.id }]"
          >
            {{ cat.name }}
          </button>
        </div>
        
        <div class="cat-sources">
          <button 
            v-for="item in currentCategorySources" 
            :key="item.id"
            @click="selectSource(item.id)"
            :class="['source-btn', { active: currentSource === item.id }]"
          >
            {{ item.name }}
          </button>
        </div>
      </div>
    </nav>

    <!-- 热榜信息 -->
    <div class="source-info" v-if="currentData">
      <div class="container">
        <h1>{{ currentData.title }}</h1>
        <span class="update-time">{{ formatTime(currentData.updateTime) }}</span>
      </div>
    </div>

    <!-- 列表 -->
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
            </div>
            <svg class="item-arrow" viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="#ccc" stroke-width="1.5">
              <path d="M6 4l4 4-4 4"/>
            </svg>
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
import { ref, computed, onMounted } from 'vue'

const API_BASE = '/api/hot'

// 快捷入口
const quickList = ref([
  { id: 'weibo', name: '微博' },
  { id: 'zhihu', name: '知乎' },
  { id: 'douyin', name: '抖音' },
  { id: 'bilibili', name: 'B站' },
  { id: 'toutiao', name: '头条' },
  { id: 'baidu', name: '百度' },
])

// 分类
const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'tech', name: '科技' },
  { id: 'finance', name: '财经' },
  { id: 'entertainment', name: '娱乐' },
  { id: 'game', name: '游戏' },
  { id: 'community', name: '社区' },
])

// 所有数据源
const allSources = ref({
  all: [
    { id: 'weibo', name: '微博' },
    { id: 'zhihu', name: '知乎' },
    { id: 'baidu', name: '百度' },
    { id: 'douyin', name: '抖音' },
    { id: 'toutiao', name: '头条' },
    { id: 'bilibili', name: 'B站' },
    { id: 'kuaishou', name: '快手' },
    { id: 'tieba', name: '贴吧' },
  ],
  tech: [
    { id: '36kr', name: '36氪' },
    { id: 'ithome', name: 'IT之家' },
    { id: 'csdn', name: 'CSDN' },
    { id: 'juejin', name: '掘金' },
    { id: 'v2ex', name: 'V2EX' },
    { id: 'github', name: 'GitHub' },
    { id: 'hackernews', name: 'Hacker News' },
    { id: 'sspai', name: '少数派' },
    { id: 'geekpark', name: '极客公园' },
    { id: 'linuxdo', name: 'Linux.do' },
  ],
  finance: [
    { id: 'sina', name: '新浪' },
    { id: 'thepaper', name: '澎湃新闻' },
    { id: 'netease-news', name: '网易新闻' },
  ],
  entertainment: [
    { id: 'douban-movie', name: '豆瓣电影' },
    { id: 'douban-group', name: '豆瓣小组' },
    { id: 'hupu', name: '虎扑' },
    { id: 'acfun', name: 'AcFun' },
  ],
  game: [
    { id: 'ngabbs', name: 'NGA' },
    { id: 'yystv', name: '游研社' },
    { id: 'genshin', name: '原神' },
    { id: 'starrail', name: '星穹铁道' },
    { id: 'honkai', name: '崩坏3' },
    { id: 'miyoushe', name: '米游社' },
  ],
  community: [
    { id: 'coolapk', name: '酷安' },
    { id: 'jianshu', name: '简书' },
    { id: 'smzdm', name: '什么值得买' },
    { id: 'zhihu-daily', name: '知乎日报' },
    { id: 'guokr', name: '果壳' },
  ],
})

const currentSource = ref('weibo')
const currentData = ref(null)
const hotList = ref([])
const activeCategory = ref('all')

const currentCategorySources = computed(() => {
  return allSources.value[activeCategory.value] || []
})

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

.back-link {
  font-size: 13px;
  color: #666;
  text-decoration: none;
}

/* 快捷入口 */
.quick-access {
  background: #fff;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.quick-list {
  display: flex;
  gap: 8px;
  overflow-x: auto;
}

.quick-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: none;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}

.quick-btn:hover {
  background: #eee;
}

.quick-btn.active {
  background: #1a1a1a;
  color: #fff;
}

/* 分类 */
.categories {
  background: #fff;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 52px;
  z-index: 99;
}

.cat-tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 12px;
}

.cat-tab {
  padding: 10px 20px;
  background: none;
  border: none;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  position: relative;
}

.cat-tab:hover {
  color: #1a1a1a;
}

.cat-tab.active {
  color: #1a1a1a;
  font-weight: 500;
}

.cat-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 16px;
  right: 16px;
  height: 2px;
  background: #1a1a1a;
}

.cat-sources {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.source-btn {
  padding: 6px 14px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
}

.source-btn:hover {
  border-color: #4F46E5;
  color: #4F46E5;
}

.source-btn.active {
  background: #4F46E5;
  border-color: #4F46E5;
  color: #fff;
}

/* 信息 */
.source-info {
  padding: 16px 0;
}

.source-info .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.source-info h1 {
  font-size: 16px;
  margin: 0;
}

.update-time {
  font-size: 12px;
  color: #999;
}

/* 列表 */
.main {
  padding: 16px 0;
}

.list {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #eee;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
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

.item-rank {
  width: 24px;
  flex-shrink: 0;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 600;
}

.rank-badge.rank-1 { background: #F59E0B; color: #fff; }
.rank-badge.rank-2 { background: #9CA3AF; color: #fff; }
.rank-badge.rank-3 { background: #B45309; color: #fff; }

.rank-num {
  color: #999;
  font-size: 13px;
  font-weight: 500;
}

.item-content {
  flex: 1;
  padding: 0 12px;
}

.item-title {
  font-size: 14px;
  color: #1a1a1a;
  margin: 0;
  transition: color 0.2s;
}

.item-arrow {
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.2s;
}

.list-item:hover .item-arrow {
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
  .cat-tabs {
    overflow-x: auto;
  }
  
  .cat-tab {
    padding: 10px 14px;
    white-space: nowrap;
  }
  
  .cat-sources {
    overflow-x: auto;
    flex-wrap: nowrap;
  }
  
  .source-btn {
    flex-shrink: 0;
  }
}
</style>