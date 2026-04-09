<template>
  <div class="tgmeng-page">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="header-inner">
        <a href="/tgmeng" class="logo">
          <span class="logo-icon">🍭</span>
          <span class="logo-text">糖果梦热榜</span>
        </a>
        
        <!-- 分类 -->
        <div class="nav-cats">
          <a 
            v-for="cat in categories" 
            :key="cat.id"
            :href="`/tgmeng/category/${cat.id}`"
            class="nav-cat"
            :class="{ active: selectedCategory === cat.id }"
          >
            {{ cat.name }}
          </a>
        </div>
        
        <!-- 搜索 -->
        <div class="search-box">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="搜索"
            @keyup.enter="doSearch"
          />
        </div>
      </div>
    </header>

    <!-- 热榜 -->
    <div class="main">
      <div class="list-wrap">
        <div class="list">
          <a 
            v-for="(item, idx) in topics" 
            :key="item.id"
            :href="item.url"
            target="_blank"
            class="item"
          >
            <span class="num" :class="'top' + (idx + 1)">{{ idx + 1 }}</span>
            <span class="title">{{ item.title }}</span>
            <span class="from">{{ item.source }}</span>
            <span class="heat">{{ item.sugar_index }}</span>
          </a>
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <div class="footer">
      <p>🍭 糖果梦热榜 · 科技不该冰冷，人性不该傲慢</p>
      <p class="footer-small">微博 · 知乎 · 抖音 · V2EX 等 200+ 平台实时聚合</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const categories = ref([])
const topics = ref([])
const searchQuery = ref('')
const selectedCategory = ref(null)

const formatNum = n => n > 9999 ? (n/10000).toFixed(1) + '万' : n

const loadCats = async () => {
  const res = await fetch('/api/categories')
  categories.value = await res.json()
}

const loadTopics = async () => {
  const res = await fetch('/api/topics?limit=30')
  topics.value = await res.json()
}

const doSearch = async () => {
  if (!searchQuery.value.trim()) return
  const res = await fetch(`/api/search?q=${encodeURIComponent(searchQuery.value)}`)
  topics.value = await res.json()
}

onMounted(() => {
  loadCats()
  loadTopics()
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 14px;
  color: #333;
  background: #f6f6f6;
}

/* 头部 */
.header {
  background: #fff;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-inner {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 16px;
  height: 50px;
  display: flex;
  align-items: center;
  gap: 20px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: #333;
}
.logo-icon { font-size: 20px; }
.logo-text { font-size: 16px; font-weight: 600; }

/* 导航 */
.nav-cats {
  display: flex;
  gap: 4px;
  flex: 1;
  overflow-x: auto;
}
.nav-cat {
  padding: 5px 12px;
  color: #666;
  text-decoration: none;
  font-size: 13px;
  border-radius: 14px;
  white-space: nowrap;
}
.nav-cat:hover { background: #f5f5f5; }
.nav-cat.active { background: #ff6b6b; color: #fff; }

/* 搜索 */
.search-box input {
  width: 140px;
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 16px;
  font-size: 13px;
  outline: none;
}
.search-box input:focus { border-color: #aaa; }

/* 主体 */
.main {
  max-width: 1000px;
  margin: 0 auto;
  padding: 16px;
}
.list-wrap {
  background: #fff;
  border-radius: 8px;
}

/* 列表 */
.list {}
.item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f5f5f5;
  text-decoration: none;
  color: #333;
}
.item:last-child { border-bottom: none; }
.item:hover { background: #fafafa; }
.item:hover .title { color: #ff6b6b; }

.num {
  width: 20px;
  font-size: 12px;
  color: #999;
  font-weight: 500;
}
.num.top1 { color: #ff6b6b; font-weight: 600; }
.num.top2 { color: #ff8c42; font-weight: 600; }
.num.top3 { color: #ffb347; font-weight: 600; }

.title {
  flex: 1;
  margin: 0 12px;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.from {
  font-size: 12px;
  color: #999;
  margin-right: 12px;
}
.heat {
  font-size: 12px;
  color: #ff6b6b;
  font-weight: 500;
}

/* 底部 */
.footer {
  text-align: center;
  padding: 24px 16px;
  color: #999;
  font-size: 12px;
}
.footer-small {
  font-size: 11px;
  color: #bbb;
  margin-top: 4px;
}

/* 移动端 */
@media (max-width: 640px) {
  .nav-cats { gap: 2px; }
  .nav-cat { padding: 4px 8px; font-size: 12px; }
  .search-box input { width: 80px; }
  .from { display: none; }
}
</style>