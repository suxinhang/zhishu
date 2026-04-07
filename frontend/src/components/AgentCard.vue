<template>
  <div 
    class="bg-white rounded-xl shadow-md p-6 cursor-pointer hover:shadow-lg hover:-translate-y-1 transition-all duration-200"
    @click="goToDetail"
  >
    <!-- 图标 -->
    <div class="w-16 h-16 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center text-3xl mb-4">
      {{ agent.icon }}
    </div>
    
    <!-- 名称 -->
    <h3 class="text-lg font-semibold text-gray-800 truncate">{{ agent.name }}</h3>
    
    <!-- 评分 -->
    <div class="flex items-center gap-2 mt-2">
      <div class="flex items-center">
        <button 
          v-for="i in 5" 
          :key="i"
          @click.stop="rateAgent(i)"
          :class="[
            'text-lg transition',
            i <= Math.round(agent.rating) ? 'text-yellow-400' : 'text-gray-300',
            'hover:text-yellow-500'
          ]"
        >
          ⭐
        </button>
      </div>
      <span class="text-sm text-gray-500">{{ agent.rating }} ({{ agent.rating_count }})</span>
    </div>
    
    <!-- 简介 -->
    <p class="text-sm text-gray-500 mt-2 line-clamp-2">{{ agent.description }}</p>
    
    <!-- 分类标签 -->
    <div class="mt-4">
      <span class="text-xs bg-blue-100 text-blue-600 px-2 py-1 rounded">{{ agent.category_name || '其他' }}</span>
    </div>
    
    <!-- 按钮 -->
    <button 
      class="mt-4 w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      @click.stop="goToChat"
    >
      立即体验
    </button>
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