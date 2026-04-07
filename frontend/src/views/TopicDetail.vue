<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition">
          <span>←</span>
          <span>返回热榜</span>
        </router-link>
        <div class="flex items-center gap-2 text-gray-400 text-sm">
          <span>🔥</span>
          <span>知枢热榜</span>
        </div>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto px-6 py-8" v-if="topic">
      <!-- 热点卡片 -->
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
        <!-- 头部：平台 + 排名 -->
        <div class="px-8 py-6 border-b border-gray-100 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-2xl">{{ topic.platform_icon }}</span>
            <span class="text-lg font-medium text-gray-800">{{ topic.platform_name }}</span>
            <span class="px-3 py-1 bg-orange-100 text-orange-600 rounded-full text-sm font-medium">
              热榜 #{{ topic.rank }}
            </span>
          </div>
          <span class="text-sm text-gray-400">{{ topic.category_icon }} {{ topic.category_name }}</span>
        </div>
        
        <!-- 标题 -->
        <div class="px-8 py-6">
          <h1 class="text-2xl font-bold text-gray-900 leading-relaxed">{{ topic.title }}</h1>
        </div>
        
        <!-- 热度数据 -->
        <div class="px-8 py-6 bg-gradient-to-r from-orange-50 to-red-50 border-y border-gray-100">
          <div class="flex items-center gap-8">
            <div>
              <p class="text-sm text-gray-500 mb-1">热度指数</p>
              <p class="text-3xl font-bold text-orange-500">{{ formatHotValue(topic.hot_value) }}</p>
            </div>
            <div class="flex-1">
              <p class="text-sm text-gray-500 mb-2">热度趋势</p>
              <div class="h-3 bg-white rounded-full overflow-hidden shadow-inner">
                <div 
                  class="h-full bg-gradient-to-r from-orange-400 to-red-500 rounded-full"
                  :style="{ width: '100%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- AI摘要 -->
        <div v-if="topic.summary" class="px-8 py-6 border-b border-gray-100">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-lg">🤖</span>
            <span class="font-medium text-gray-700">AI 智能摘要</span>
          </div>
          <p class="text-gray-600 leading-relaxed">{{ topic.summary }}</p>
        </div>
        
        <!-- 操作按钮 -->
        <div class="px-8 py-6 flex gap-4">
          <a 
            :href="topic.url"
            target="_blank"
            rel="noopener noreferrer"
            class="flex-1 py-3 bg-orange-500 text-white rounded-xl text-center font-medium hover:bg-orange-600 transition flex items-center justify-center gap-2"
          >
            <span>🔗</span> 跳转到 {{ topic.platform_name }} 查看
          </a>
          <button class="px-6 py-3 border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 transition">
            ❤️ 收藏
          </button>
          <button class="px-6 py-3 border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 transition">
            📤 分享
          </button>
        </div>
      </div>
      
      <!-- 相关热点 -->
      <div class="mt-8" v-if="relatedTopics.length > 0">
        <h3 class="font-medium text-gray-800 mb-4 flex items-center gap-2">
          <span>📌</span> 相关热点
        </h3>
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div 
            v-for="rel in relatedTopics" 
            :key="rel.id"
            @click="goToTopic(rel.id)"
            class="px-6 py-4 border-b border-gray-100 last:border-0 hover:bg-gray-50 cursor-pointer transition flex items-center justify-between"
          >
            <span class="text-gray-700 hover:text-orange-600 transition">{{ rel.title }}</span>
            <div class="flex items-center gap-3 text-sm text-gray-400">
              <span>{{ topic.platform_icon }}</span>
              <span>{{ formatHotValue(rel.hot_value) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-else class="text-center py-20">
      <span class="text-4xl animate-pulse inline-block">🔥</span>
      <p class="text-gray-400 mt-4">加载中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

interface Topic {
  id: number
  title: string
  platform_id: number
  platform_name: string
  platform_icon: string
  category_id: number
  category_name: string
  category_icon: string
  hot_value: number
  rank: number
  url: string
  summary: string
  created_at: string
}

const topic = ref<Topic | null>(null)
const relatedTopics = ref<Topic[]>([])
const router = useRouter()
const route = useRoute()

const formatHotValue = (value: number) => {
  if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
  if (value >= 1000) return (value / 1000).toFixed(0) + 'K'
  return value.toString()
}

const goToTopic = (id: number) => {
  router.push(`/topic/${id}`)
}

const loadTopic = async () => {
  const id = route.params.id
  try {
    const res = await fetch(`/api/topics/${id}`)
    topic.value = await res.json()
    
    if (topic.value) {
      const relatedRes = await fetch(`/api/topics?category=${topic.value.category_id}&sort=hot`)
      const allRelated = await relatedRes.json()
      relatedTopics.value = allRelated.filter((t: any) => t.id !== topic.value!.id).slice(0, 5)
    }
  } catch (e) {
    console.error('Failed to load topic:', e)
  }
}

onMounted(async () => {
  await loadTopic()
})
</script>