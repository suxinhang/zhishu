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
          <span class="logo-text">知枢·看点</span>
        </a>
        <div class="header-right">
          <span class="update-time">{{ updateTime }}</span>
          <DarkModeToggle />
        </div>
      </div>
    </header>

    <!-- 分类 -->
    <nav class="category-nav">
      <div class="container">
        <div class="cat-list">
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectCategory(cat.id)"
            :class="['cat-btn', { active: currentCategory === cat.id }]"
          >
            {{ cat.name }}
          </button>
        </div>
      </div>
    </nav>

    <!-- 热榜网格 -->
    <main class="main">
      <div class="container">
        <div class="hot-grid">
          <div v-for="source in currentSources" :key="source.id" class="hot-card">
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
        <p>知枢·看点 · 实时聚合全网热点</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DarkModeToggle from '@/components/DarkModeToggle.vue'

const API_BASE = '/api/hot'

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
const allSources = [
  { id: 'weibo', name: '微博', link: 'https://s.weibo.com/top/summary/', category: 'all', items: [] },
  { id: 'zhihu', name: '知乎', link: 'https://www.zhihu.com/hot', category: 'all', items: [] },
  { id: 'douyin', name: '抖音', link: 'https://www.douyin.com/hot', category: 'all', items: [] },
  { id: 'bilibili', name: 'B站', link: 'https://www.bilibili.com/v/popular/rank/all', category: 'all', items: [] },
  { id: 'toutiao', name: '头条', link: 'https://www.toutiao.com/', category: 'all', items: [] },
  { id: 'baidu', name: '百度', link: 'https://top.baidu.com/board', category: 'all', items: [] },
  { id: 'kuaishou', name: '快手', link: 'https://www.kuaishou.com/hot', category: 'all', items: [] },
  { id: 'tieba', name: '贴吧', link: 'https://tieba.baidu.com/hottopic', category: 'all', items: [] },
  { id: '36kr', name: '36氪', link: 'https://36kr.com/hot', category: 'tech', items: [] },
  { id: 'ithome', name: 'IT之家', link: 'https://www.ithome.com/', category: 'tech', items: [] },
  { id: 'csdn', name: 'CSDN', link: 'https://www.csdn.net/', category: 'tech', items: [] },
  { id: 'juejin', name: '掘金', link: 'https://juejin.cn/', category: 'tech', items: [] },
  { id: 'v2ex', name: 'V2EX', link: 'https://www.v2ex.com/', category: 'tech', items: [] },
  { id: 'github', name: 'GitHub', link: 'https://github.com/trending', category: 'tech', items: [] },
  { id: 'sina', name: '新浪', link: 'https://news.sina.com.cn/', category: 'finance', items: [] },
  { id: 'thepaper', name: '澎湃', link: 'https://www.thepaper.cn/', category: 'finance', items: [] },
  { id: 'douban-movie', name: '豆瓣电影', link: 'https://movie.douban.com/', category: 'entertainment', items: [] },
  { id: 'douban-group', name: '豆瓣小组', link: 'https://www.douban.com/group/', category: 'entertainment', items: [] },
  { id: 'hupu', name: '虎扑', link: 'https://www.hupu.com/', category: 'entertainment', items: [] },
  { id: 'ngabbs', name: 'NGA', link: 'https://ngabbs.com/', category: 'game', items: [] },
  { id: 'coolapk', name: '酷安', link: 'https://www.coolapk.com/', category: 'community', items: [] },
  { id: 'jianshu', name: '简书', link: 'https://www.jianshu.com/', category: 'community', items: [] },
  { id: 'guokr', name: '果壳', link: 'https://www.guokr.com/', category: 'community', items: [] },
]

const sources = ref(allSources)
const currentCategory = ref('all')
const updateTime = ref('')
const loadingCount = ref(0)

// 当前分类的数据源
const currentSources = computed(() => {
  return sources.value.filter(s => s.category === currentCategory.value || currentCategory.value === 'all')
})

const selectCategory = (catId) => {
  currentCategory.value = catId
}

const loadAllData = async () => {
  const time = new Date()
  updateTime.value = time.getHours() + ':' + String(time.getMinutes()).padStart(2, '0')
  
  loadingCount.value = sources.value.length
  
  // 并行加载所有数据
  await Promise.all(
    sources.value.map(async (source) => {
      try {
        const res = await fetch(`${API_BASE}/${source.id}`)
        const json = await res.json()
        if (json.code === 200 && json.data) {
          source.items = json.data.slice(0, 5)
        }
      } catch (e) {
        console.error(`加载 ${source.name} 失败:`, e)
      } finally {
        loadingCount.value--
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
  background: var(--bg);
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

.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
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

.update-time {
  font-size: 12px;
  color: var(--text-muted);
}

/* 分类导航 */
.category-nav {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 52px;
  z-index: 99;
}

.cat-list {
  display: flex;
  gap: 4px;
  padding: 10px 0;
  overflow-x: auto;
}

.cat-btn {
  padding: 8px 20px;
  background: var(--bg);
  border: none;
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-muted);
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}

.cat-btn:hover {
  background: var(--border);
}

.cat-btn.active {
  background: var(--text);
  color: var(--bg);
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
  background: var(--bg-card);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-light);
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
  color: var(--text);
}

.card-link {
  font-size: 12px;
  color: var(--text-muted);
  text-decoration: none;
}

.card-link:hover {
  color: var(--primary);
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
  color: var(--text);
}

.list-item:hover {
  background: var(--bg);
}

.list-item:hover .item-title {
  color: var(--primary);
}

.item-rank {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
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
  color: var(--text-muted);
  font-size: 13px;
}

/* Footer */
.footer {
  padding: 32px 0;
  text-align: center;
  color: var(--text-muted);
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