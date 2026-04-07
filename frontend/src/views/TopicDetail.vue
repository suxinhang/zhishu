<template>
  <div class="max-w-4xl mx-auto px-6 py-8">
    <div v-if="topic" class="animate-fade-in">
      <!-- 返回链接 -->
      <router-link 
        to="/" 
        class="inline-flex items-center gap-2 text-slate-500 hover:text-amber-500 transition mb-6"
      >
        <span>←</span> 返回首页
      </router-link>
      
      <!-- 热点卡片 -->
      <div class="bg-white rounded-2xl shadow-card overflow-hidden">
        <!-- 热度条 -->
        <div class="h-2 bg-gradient-to-r from-amber-400 via-orange-500 to-red-500"></div>
        
        <div class="p-8">
          <!-- 头部信息 -->
          <div class="flex items-start justify-between mb-6">
            <div>
              <div class="flex items-center gap-3 mb-3">
                <span class="px-3 py-1.5 bg-amber-100 text-amber-600 rounded-lg font-medium">
                  {{ topic.platform_icon }} {{ topic.platform_name }}
                </span>
                <span class="text-slate-400">#{{ topic.rank }}</span>
              </div>
              <h1 class="text-2xl font-bold text-slate-800 leading-snug">{{ topic.title }}</h1>
            </div>
          </div>
          
          <!-- 热度值 -->
          <div class="flex items-center gap-4 mb-6 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl">
            <div class="flex-1">
              <p class="text-sm text-slate-500 mb-1">热度值</p>
              <p class="text-3xl font-bold text-amber-500">{{ formatHotValue(topic.hot_value) }}</p>
            </div>
            <div class="w-px h-12 bg-amber-200"></div>
            <div class="flex-1">
              <p class="text-sm text-slate-500 mb-1">平台排名</p>
              <p class="text-3xl font-bold text-slate-700">#{{ topic.rank }}</p>
            </div>
            <div class="w-px h-12 bg-amber-200"></div>
            <div class="flex-1">
              <p class="text-sm text-slate-500 mb-1">所属分类</p>
              <p class="text-xl font-semibold text-slate-700">{{ topic.category_name }}</p>
            </div>
          </div>
          
          <!-- AI摘要 -->
          <div v-if="topic.summary" class="mb-6 p-5 bg-slate-50 rounded-xl border border-slate-200">
            <h3 class="font-semibold text-slate-700 mb-2 flex items-center gap-2">
              <span>🤖</span> AI 智能摘要
            </h3>
            <p class="text-slate-600 leading-relaxed">{{ topic.summary }}</p>
          </div>
          
          <!-- 外链按钮 -->
          <div class="flex gap-4">
            <a 
              :href="topic.url"
              target="_blank"
              rel="noopener noreferrer"
              class="flex-1 py-4 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl text-lg font-semibold flex items-center justify-center gap-2 hover:shadow-lg transition"
            >
              <span>🔗</span> 跳转原平台查看
            </a>
            <button 
              class="px-6 py-4 bg-white text-slate-600 rounded-xl border border-slate-200 hover:border-amber-300 hover:bg-amber-50 transition font-medium flex items-center gap-2"
            >
              <span>❤️</span> 收藏
            </button>
          </div>
        </div>
        
        <!-- 底部装饰 -->
        <div class="flex justify-center gap-2 py-3 bg-slate-50 opacity-40">
          <div class="w-2 h-2 rounded-full bg-amber-300"></div>
          <div class="w-2 h-2 rounded-full bg-orange-300"></div>
          <div class="w-2 h-2 rounded-full bg-amber-300"></div>
        </div>
      </div>
      
      <!-- 相关热点（可选） -->
      <div class="mt-8">
        <h3 class="font-semibold text-slate-800 mb-4 flex items-center gap-2">
          <span>📌</span> 相关热点
        </h3>
        <div class="grid grid-cols-2 gap-4">
          <div 
            v-for="rel in relatedTopics" 
            :key="rel.id"
            @click="goToTopic(rel.id)"
            class="bg-white rounded-xl shadow-card p-4 cursor-pointer hover:shadow-card-hover hover:-translate-y-1 transition"
          >
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xs text-slate-500">{{ rel.platform_name }}</span>
              <span class="text-xs text-amber-500">🔥 {{ formatHotValue(rel.hot_value) }}</span>
            </div>
            <p class="text-sm font-medium text-slate-700 line-clamp-2">{{ rel.title }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-else class="text-center py-16">
      <div class="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mx-auto mb-4 animate-pulse-slow">
        🔥
      </div>
      <p class="text-slate-400">加载中...</p>
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
    
    // 加载相关热点
    if (topic.value) {
      const relatedRes = await fetch(`/api/topics?category=${topic.value.category_id}&sort=hot`)
      const allRelated = await relatedRes.json()
      relatedTopics.value = allRelated.filter((t: any) => t.id !== topic.value!.id).slice(0, 4)
    }
  } catch (e) {
    console.error('Failed to load topic:', e)
  }
}

onMounted(async () => {
  await loadTopic()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>