<template>
  <div class="tgmeng-app">
    <header class="tgmeng-header">
      <div class="tgmeng-container">
        <div class="tgmeng-header-inner">
          <router-link to="/tgmeng" class="tgmeng-logo">
            <span class="tgmeng-logo-icon">🔥</span>
            <span class="logo-text">知枢·看点</span>
          </router-link>
          <div class="tgmeng-back">
            <router-link to="/tgmeng">← 返回首页</router-link>
          </div>
        </div>
      </div>
    </header>

    <main class="tgmeng-main">
      <div class="tgmeng-container">
        <h1 class="tgmeng-page-title">{{ category?.icon }} {{ category?.name }}</h1>
        
        <div class="tgmeng-list">
          <div v-for="(topic, index) in topics" :key="topic.id" class="tgmeng-list-item" @click="openTopic(topic)">
            <div class="tgmeng-rank">
              <span v-if="index < 3" :class="['tgmeng-rank-badge', `rank-${index + 1}`]">{{ index + 1 }}</span>
              <span v-else class="tgmeng-rank-num">{{ index + 1 }}</span>
            </div>
            <div class="tgmeng-content">
              <h3 class="tgmeng-title">{{ topic.title }}</h3>
              <div class="tgmeng-meta">
                <span class="tgmeng-source">{{ topic.source }}</span>
              </div>
            </div>
            <div class="tgmeng-stats">
              <span>👁 {{ formatNumber(topic.view_count) }}</span>
            </div>
            <div class="tgmeng-sugar">
              <div class="tgmeng-sugar-num">{{ topic.sugar_index }}</div>
              <div class="tgmeng-sugar-label">糖果指数</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const category = ref<{ id: number; name: string; icon: string } | null>(null)
const topics = ref<any[]>([])

const formatNumber = (num: number) => num >= 10000 ? (num / 10000).toFixed(1) + 'w' : num
const openTopic = (topic: any) => window.open(topic.url, '_blank')

const loadData = async () => {
  const catId = route.params.id
  const [cats, topicsData] = await Promise.all([
    fetch('/api/categories').then(r => r.json()),
    fetch(`/api/topics?category=${catId}`).then(r => r.json())
  ])
  category.value = cats.find((c: any) => c.id === Number(catId))
  topics.value = topicsData
}

watch(() => route.params.id, loadData)
onMounted(loadData)
</script>

<style scoped>
.tgmeng-app {
  min-height: 100vh;
  background: var(--bg);
}
.tgmeng-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}
.tgmeng-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.tgmeng-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
}
.tgmeng-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text);
}
.tgmeng-logo-icon { font-size: 20px; }
.logo-text { font-size: 15px; font-weight: 600; }
.tgmeng-back a { color: #666; text-decoration: none; }
.tgmeng-back a:hover { color: var(--primary); }
.tgmeng-page-title { font-size: 24px; font-weight: 600; margin-bottom: 24px; color: var(--text); }
.tgmeng-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.tgmeng-list-item {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
}
.tgmeng-list-item:hover {
  border-color: var(--primary);
}
.tgmeng-rank { flex-shrink: 0; }
.tgmeng-rank-badge {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: bold;
  font-size: 14px;
}
.tgmeng-rank-badge.rank-1 { background: #FFD700; color: #333; }
.tgmeng-rank-badge.rank-2 { background: #C0C0C0; color: #333; }
.tgmeng-rank-badge.rank-3 { background: #CD7F32; color: white; }
.tgmeng-rank-num { font-size: 14px; color: var(--text-muted); }
.tgmeng-content { flex: 1; }
.tgmeng-title { font-size: 16px; color: var(--text); margin: 0; }
.tgmeng-meta { margin-top: 4px; }
.tgmeng-source { font-size: 12px; color: var(--text-muted); }
.tgmeng-stats { font-size: 13px; color: var(--text-muted); }
.tgmeng-sugar { text-align: center; }
.tgmeng-sugar-num { font-size: 18px; font-weight: 600; color: var(--primary); }
.tgmeng-sugar-label { font-size: 11px; color: var(--text-muted); }
</style>