<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div v-if="agent" class="bg-white rounded-xl shadow-md p-8">
      <!-- 头部 -->
      <div class="flex items-center gap-6">
        <div class="w-20 h-20 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center text-4xl">
          {{ agent.icon }}
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-800">{{ agent.name }}</h1>
          <span class="text-sm bg-blue-100 text-blue-600 px-2 py-1 rounded mt-2 inline-block">
            {{ agent.category_name || '其他' }}
          </span>
        </div>
      </div>
      
      <!-- 简介 -->
      <div class="mt-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">简介</h2>
        <p class="text-gray-600">{{ agent.description }}</p>
      </div>
      
      <!-- 对话按钮 -->
      <button 
        @click="goToChat"
        class="mt-8 w-full py-3 bg-blue-600 text-white rounded-lg text-lg hover:bg-blue-700 transition"
      >
        开始对话
      </button>
    </div>
    
    <div v-else class="text-center py-12 text-gray-400">
      加载中...
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
}

const agent = ref<Agent | null>(null)
const router = useRouter()
const route = useRoute()

const goToChat = () => {
  if (agent.value) {
    router.push(`/chat/${agent.value.id}`)
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