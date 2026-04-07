<template>
  <div class="max-w-4xl mx-auto px-6 py-8">
    <div v-if="agent" class="animate-fade-in">
      <!-- 顶部导航 -->
      <router-link 
        to="/" 
        class="inline-flex items-center gap-2 text-slate-500 hover:text-zhishu-600 transition mb-6"
      >
        <span>←</span> 返回首页
      </router-link>
      
      <!-- 智能体卡片 -->
      <div class="bg-white rounded-2xl shadow-card overflow-hidden">
        <!-- 顶部装饰线 -->
        <div class="h-2 bg-gradient-to-r from-zhishu-600 via-amber-400 to-zhishu-600"></div>
        
        <!-- 头部信息 -->
        <div class="p-8">
          <div class="flex items-start gap-6">
            <!-- 图标 -->
            <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-zhishu-100 to-zhishu-50 flex items-center justify-center text-5xl shadow-lg">
              {{ agent.icon }}
            </div>
            
            <!-- 基本信息 -->
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-slate-800 mb-2">{{ agent.name }}</h1>
              
              <!-- 评分 -->
              <div class="flex items-center gap-3 mb-3">
                <div class="flex items-center gap-0.5">
                  <span v-for="i in 5" :key="i" class="text-xl" :class="i <= Math.round(agent.rating) ? 'text-amber-400' : 'text-slate-200'">
                    ★
                  </span>
                </div>
                <span class="text-slate-600">
                  <span class="font-semibold">{{ agent.rating.toFixed(1) }}</span>
                  <span class="text-slate-400 text-sm ml-1">({{ agent.rating_count }} 人评分)</span>
                </span>
              </div>
              
              <!-- 分类标签 -->
              <div class="flex items-center gap-2">
                <span class="px-3 py-1.5 bg-zhishu-50 text-zhishu-600 rounded-lg text-sm font-medium">
                  {{ agent.category_name || '其他' }}
                </span>
                <span v-if="agent.hot_score" class="hot-badge">
                  🔥 {{ agent.hot_score }} 热度
                </span>
              </div>
            </div>
          </div>
          
          <!-- 简介 -->
          <div class="mt-8 p-4 bg-slate-50 rounded-xl">
            <h2 class="text-sm font-semibold text-slate-600 mb-2 flex items-center gap-1">
              <span>📝</span> 简介
            </h2>
            <p class="text-slate-700 leading-relaxed">{{ agent.description }}</p>
          </div>
          
          <!-- 功能特点（可扩展） -->
          <div class="mt-6 grid grid-cols-2 gap-4">
            <div class="p-4 bg-white rounded-xl border border-slate-200/50 flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-green-50 flex items-center justify-center text-lg">⚡</div>
              <div>
                <h3 class="font-medium text-slate-700">即时响应</h3>
                <p class="text-xs text-slate-400">秒级回复</p>
              </div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-slate-200/50 flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center text-lg">🧠</div>
              <div>
                <h3 class="font-medium text-slate-700">智能对话</h3>
                <p class="text-xs text-slate-400">多轮交互</p>
              </div>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex gap-4 mt-8">
            <button 
              @click="goToChat"
              class="flex-1 py-4 btn-primary text-lg font-semibold flex items-center justify-center gap-2"
            >
              <span>💬</span> 开始对话
            </button>
            <button 
              class="px-8 py-4 btn-secondary font-medium flex items-center gap-2"
            >
              <span>❤️</span> 收藏
            </button>
          </div>
        </div>
        
        <!-- 底部装饰 -->
        <div class="flex justify-center gap-2 py-3 bg-slate-50 opacity-40">
          <div class="w-2 h-2 rounded-full bg-zhishu-300"></div>
          <div class="w-2 h-2 rounded-full bg-amber-300"></div>
          <div class="w-2 h-2 rounded-full bg-zhishu-300"></div>
        </div>
      </div>
      
      <!-- 评分区域 -->
      <div class="mt-8 bg-white rounded-xl shadow-card p-6">
        <h3 class="font-semibold text-slate-800 mb-4 flex items-center gap-2">
          <span>⭐</span> 为这个智能体评分
        </h3>
        <div class="flex items-center gap-2">
          <button 
            v-for="i in 5" 
            :key="i"
            @click="rateAgent(i)"
            class="w-12 h-12 rounded-xl border border-slate-200 hover:border-amber-300 hover:bg-amber-50 transition-all duration-200 flex items-center justify-center text-2xl"
            :class="{ 'bg-amber-50 border-amber-300': hoverRating >= i }"
            @mouseenter="hoverRating = i"
            @mouseleave="hoverRating = 0"
          >
            ★
          </button>
        </div>
        <p class="text-sm text-slate-500 mt-3">
          你的评分将帮助其他用户找到更好的智能体
        </p>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-else class="text-center py-16">
      <div class="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mx-auto mb-4 animate-pulse-slow">
        🧠
      </div>
      <p class="text-slate-400">加载中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

interface Agent {
  id: number
  name: string
  icon: string
  description: string
  category_name?: string
  rating: number
  rating_count: number
  hot_score?: number
}

const agent = ref<Agent | null>(null)
const hoverRating = ref(0)
const router = useRouter()
const route = useRoute()

const goToChat = () => {
  if (agent.value) {
    router.push(`/chat/${agent.value.id}`)
  }
}

const rateAgent = async (score: number) => {
  if (!agent.value) return
  try {
    await fetch(`/api/agents/${agent.value.id}/rate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score })
    })
    // 重新加载智能体信息
    const res = await fetch(`/api/agents/${agent.value.id}`)
    agent.value = await res.json()
  } catch (e) {
    console.error('Failed to rate:', e)
  }
}

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await fetch(`/api/agents/${id}`)
    agent.value = await res.json()
  } catch (e) {
    console.error('Failed to load agent:', e)
  }
})
</script>