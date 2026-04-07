<template>
  <div 
    class="bg-white rounded-xl shadow-card card-glow cursor-pointer node-decoration overflow-hidden"
    @click="goToDetail"
  >
    <!-- 顶部装饰线 -->
    <div class="h-1 bg-gradient-to-r from-zhishu-600 via-amber-400 to-zhishu-600 opacity-30"></div>
    
    <!-- 图标区域 -->
    <div class="p-5">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-zhishu-100 to-zhishu-50 flex items-center justify-center text-3xl shadow-inner">
        {{ agent.icon }}
      </div>
    </div>
    
    <!-- 内容区域 -->
    <div class="px-5 pb-5">
      <!-- 名称 -->
      <h3 class="text-lg font-semibold text-slate-800 truncate">{{ agent.name }}</h3>
      
      <!-- 评分区域 -->
      <div class="flex items-center gap-2 mt-2">
        <div class="flex items-center gap-0.5">
          <button 
            v-for="i in 5" 
            :key="i"
            @click.stop="rateAgent(i)"
            class="star-rating text-lg"
            :class="i <= Math.round(agent.rating) ? 'text-amber-400' : 'text-slate-200'"
          >
            ★
          </button>
        </div>
        <span class="text-sm text-slate-500">
          <span class="font-medium text-slate-700">{{ agent.rating.toFixed(1) }}</span>
          <span class="text-xs ml-1">({{ agent.rating_count }}人评)</span>
        </span>
      </div>
      
      <!-- 简介 -->
      <p class="text-sm text-slate-500 mt-3 line-clamp-2 leading-relaxed">{{ agent.description }}</p>
      
      <!-- 分类和热度 -->
      <div class="flex items-center justify-between mt-4">
        <span class="px-2.5 py-1 bg-zhishu-50 text-zhishu-600 rounded-lg text-xs font-medium">
          {{ agent.category_name || '其他' }}
        </span>
        <div v-if="agent.hot_score" class="hot-badge">
          🔥 {{ agent.hot_score }}
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="flex gap-2 mt-4">
        <button 
          class="flex-1 py-2.5 btn-primary text-sm"
          @click.stop="goToChat"
        >
          立即对话
        </button>
        <button 
          class="px-4 py-2.5 btn-secondary text-sm"
          @click.stop="goToDetail"
        >
          详情
        </button>
      </div>
    </div>
    
    <!-- 底部装饰点 -->
    <div class="flex justify-center gap-2 py-2 opacity-40">
      <div class="w-2 h-2 rounded-full bg-zhishu-300"></div>
      <div class="w-2 h-2 rounded-full bg-amber-300"></div>
      <div class="w-2 h-2 rounded-full bg-zhishu-300"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

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

const props = defineProps<{ agent: Agent }>()
const emit = defineEmits(['rated'])
const router = useRouter()

const goToDetail = () => {
  router.push(`/agent/${props.agent.id}`)
}

const goToChat = () => {
  router.push(`/chat/${props.agent.id}`)
}

const rateAgent = async (score: number) => {
  try {
    await fetch(`/api/agents/${props.agent.id}/rate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score })
    })
    emit('rated')
  } catch (e) {
    console.error('Failed to rate:', e)
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>