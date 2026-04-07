<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- 智能体信息 -->
    <div v-if="agent" class="bg-white rounded-xl shadow-md p-6 mb-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center text-2xl">
          {{ agent.icon }}
        </div>
        <div>
          <h2 class="text-xl font-semibold text-gray-800">{{ agent.name }}</h2>
          <p class="text-sm text-gray-500">{{ agent.description }}</p>
        </div>
      </div>
    </div>

    <!-- 对话区域 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <!-- 消息列表 -->
      <div class="space-y-4 mb-6 max-h-96 overflow-y-auto">
        <div 
          v-for="(msg, idx) in messages" 
          :key="idx"
          :class="[
            'p-3 rounded-lg max-w-[80%]',
            msg.role === 'user' 
              ? 'bg-blue-600 text-white ml-auto' 
              : 'bg-gray-100 text-gray-800'
          ]"
        >
          {{ msg.content }}
        </div>
        
        <div v-if="isLoading" class="p-3 rounded-lg bg-gray-100 text-gray-500 max-w-[80%]">
          正在思考...
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="flex gap-2">
        <textarea 
          v-model="inputText"
          placeholder="输入消息..."
          class="flex-1 p-3 border border-gray-200 rounded-lg outline-none focus:border-blue-400 resize-none"
          rows="2"
          @keyup.ctrl.enter="sendMessage"
        />
        <button 
          @click="sendMessage"
          :disabled="isLoading || !inputText.trim()"
          class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

interface Agent {
  id: number
  name: string
  icon: string
  description: string
}

interface Message {
  role: 'user' | 'agent'
  content: string
}

const agent = ref<Agent | null>(null)
const messages = ref<Message[]>([])
const inputText = ref('')
const isLoading = ref(false)
const route = useRoute()

// 模拟回复库
const mockResponses = [
  '你好！有什么我可以帮助你的吗？',
  '这是一个很有趣的问题，让我想想...',
  '根据我的理解，这个问题可以这样解决。',
  '我很乐意帮助你！请告诉我更多细节。',
  '好的，我来帮你分析一下。',
  '这个话题很有意思，我们可以深入讨论。',
]

const sendMessage = async () => {
  if (!inputText.trim() || isLoading.value) return
  
  const userMsg = inputText.value.trim()
  messages.value.push({ role: 'user', content: userMsg })
  inputText.value = ''
  isLoading.value = true
  
  // 模拟延迟响应
  await new Promise(r => setTimeout(r, 1000 + Math.random() * 1000))
  
  // 随机选择回复
  const response = mockResponses[Math.floor(Math.random() * mockResponses.length)]
  messages.value.push({ role: 'agent', content: response })
  isLoading.value = false
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