<template>
  <div class="tgmeng-app">
    <header class="tgmeng-header">
      <div class="tgmeng-container">
        <div class="tgmeng-header-inner">
          <router-link to="/tgmeng" class="tgmeng-logo">
            <span class="tgmeng-logo-icon">🍭</span>
            <span class="tgmeng-logo-text">糖果梦热榜</span>
          </router-link>
          <div class="tgmeng-back">
            <router-link to="/tgmeng">← 返回首页</router-link>
          </div>
        </div>
      </div>
    </header>

    <main class="tgmeng-main">
      <div class="tgmeng-container">
        <div v-if="topic" class="tgmeng-topic-detail">
          <div class="tgmeng-topic-header">
            <div class="tgmeng-topic-rank">TOP {{ rank }}</div>
            <h1 class="tgmeng-topic-title">{{ topic.title }}</h1>
            <div class="tgmeng-topic-meta">
              <span class="tgmeng-source">{{ topic.source }}</span>
              <span class="tgmeng-category">{{ topic.category }}</span>
            </div>
          </div>
          
          <div class="tgmeng-topic-stats">
            <div class="tgmeng-stat-item">
              <div class="tgmeng-stat-value">{{ topic.sugar_index }}</div>
              <div class="tgmeng-stat-label">糖果指数</div>
            </div>
            <div class="tgmeng-stat-item">
              <div class="tgmeng-stat-value">{{ formatNumber(topic.view_count) }}</div>
              <div class="tgmeng-stat-label">浏览量</div>
            </div>
            <div class="tgmeng-stat-item">
              <div class="tgmeng-stat-value">{{ topic.comment_count }}</div>
              <div class="tgmeng-stat-label">评论数</div>
            </div>
          </div>
          
          <a :href="topic.url" target="_blank" class="tgmeng-topic-link">查看原文 →</a>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const topic = ref<any>(null)
const rank = ref(0)

const formatNumber = (num: number) => num >= 10000 ? (num / 10000).toFixed(1) + 'w' : num

onMounted(async () => {
  topic.value = await (await fetch(`/api/topics/${route.params.id}`)).json()
})
</script>

<style scoped>
@import './TgmengHome.vue';
.tgmeng-back a { color: #666; text-decoration: none; }
.tgmeng-topic-detail { background: #FFF; border-radius: 12px; padding: 32px; }
.tgmeng-topic-header { margin-bottom: 24px; }
.tgmeng-topic-rank { display: inline-block; padding: 4px 12px; background: #FF6B6B; color: #FFF; border-radius: 4px; font-size: 12px; margin-bottom: 12px; }
.tgmeng-topic-title { font-size: 24px; font-weight: 600; margin: 0 0 12px 0; }
.tgmeng-topic-meta { display: flex; gap: 8px; }
.tgmeng-topic-stats { display: flex; gap: 32px; padding: 24px 0; border-top: 1px solid #F0F0F0; border-bottom: 1px solid #F0F0F0; margin: 24px 0; }
.tgmeng-stat-item { text-align: center; }
.tgmeng-stat-value { font-size: 24px; font-weight: 600; color: #FF6B6B; }
.tgmeng-stat-label { font-size: 12px; color: #999; margin-top: 4px; }
.tgmeng-topic-link { display: inline-block; padding: 12px 24px; background: #1890FF; color: #FFF; border-radius: 6px; text-decoration: none; }
</style>