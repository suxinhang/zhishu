<template>
  <div class="tgmeng-app">
    <header class="tgmeng-header">
      <div class="tgmeng-container">
        <div class="tgmeng-header-inner">
          <router-link to="/tgmeng" class="tgmeng-logo">
            <span class="tgmeng-logo-icon">🍭</span>
            <span class="logo-text">知枢热榜</span>
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
@import './TgmengHome.vue';
.tgmeng-back a { color: #666; text-decoration: none; }
.tgmeng-back a:hover { color: #1890FF; }
.tgmeng-page-title { font-size: 24px; font-weight: 600; margin-bottom: 24px; }
</style>