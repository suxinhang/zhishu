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
            href="#"
            @click.prevent="selectSource(cat.id)"
            class="nav-cat"
            :class="{ active: currentSource === cat.id }"
          >
            {{ cat.name }}
          </a>
        </div>
      </div>
    </header>

    <!-- 热榜 -->
    <div class="main">
      <div class="list-wrap">
        <div class="source-info" v-if="currentData">
          <h2>{{ currentData.title }}</h2>
          <p>{{ currentData.description }}</p>
          <span class="update-time">更新时间: {{ formatTime(currentData.updateTime) }}</span>
        </div>
        
        <div class="list">
          <a 
            v-for="(item, idx) in hotList" 
            :key="item.id"
            :href="item.url"
            target="_blank"
            class="item"
          >
            <span class="num" :class="'top' + (idx + 1)">{{ idx + 1 }}</span>
            <span class="title">{{ item.title }}</span>
            <span class="desc" v-if="item.desc && item.desc !== item.title">{{ item.desc.slice(0, 30) }}</span>
          </a>
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <div class="footer">
      <p>🍭 糖果梦热榜 · 科技不该冰冷，人性不该傲慢</p>
      <p class="footer-small">数据来源: 微博 · 知乎 · 抖音 · B站 等 45+ 平台实时聚合</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// API 基础地址 - 通过 nginx 代理访问
const API_BASE = '/api/hot'

// 数据源列表
const categories = ref([
  { id: 'weibo', name: '微博' },
  { id: 'zhihu', name: '知乎' },
  { id: 'bilibili', name: 'B站' },
  { id: 'douyin', name: '抖音' },
  { id: 'baidu', name: '百度' },
  { id: 'toutiao', name: '头条' },
  { id: '36kr', name: '36氪' },
  { id: 'juejin', name: '掘金' },
  { id: 'v2ex', name: 'V2EX' },
  { id: 'hupu', name: '虎扑' },
])

const currentSource = ref('weibo')
const currentData = ref(null)
const hotList = ref([])

const formatTime = (t) => {
  if (!t) return ''
  return new Date(t).toLocaleString('zh-CN')
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

/* 数据源信息 */
.source-info {
  padding: 16px;
  border-bottom: 1px solid #f5f5f5;
}
.source-info h2 {
  font-size: 18px;
  margin-bottom: 4px;
}
.source-info p {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}
.update-time {
  font-size: 11px;
  color: #bbb;
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
  width: 24px;
  font-size: 12px;
  color: #999;
  font-weight: 500;
  flex-shrink: 0;
}
.num.top1 { color: #ff6b6b; font-weight: 600; font-size: 14px; }
.num.top2 { color: #ff8c42; font-weight: 600; font-size: 14px; }
.num.top3 { color: #ffb347; font-weight: 600; font-size: 14px; }

.title {
  flex: 1;
  margin: 0 12px;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.desc {
  font-size: 12px;
  color: #999;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  .desc { display: none; }
}
</style>