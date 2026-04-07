<template>
  <div class="max-w-4xl mx-auto px-6 py-8">
    <!-- 智能体信息卡片 -->
    <div v-if="agent" class="animate-fade-in">
      <!-- 返回链接 -->
      <router-link 
        :to="`/agent/${agent.id}`"
        class="inline-flex items-center gap-2 text-slate-500 hover:text-zhishu-600 transition mb-6"
      >
        <span>←</span> 返回详情
      </router-link>
      
      <!-- 智能体头部 -->
      <div class="bg-white rounded-xl shadow-card p-4 mb-6 flex items-center gap-4">
        <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-zhishu-100 to-zhishu-50 flex items-center justify-center text-2xl shadow-inner">
          {{ agent.icon }}
        </div>
        <div class="flex-1">
          <h2 class="text-lg font-semibold text-slate-800">{{ agent.name }}</h2>
          <p class="text-sm text-slate-500 truncate">{{ agent.description }}</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="px-3 py-1 bg-green-50 text-green-600 rounded-lg text-xs font-medium flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            在线
          </span>
        </div>
      </div>

      <!-- 对话区域 -->
      <div class="bg-white rounded-2xl shadow-card overflow-hidden">
        <!-- 顶部装饰 -->
        <div class="h-1 bg-gradient-to-r from-zhishu-600 via-amber-400 to-zhishu-600 opacity-50"></div>
        
        <!-- 消息列表 -->
        <div ref="messagesContainer" class="p-6 space-y-4 min-h-[400px] max-h-[500px] overflow-y-auto">
          <!-- 欢迎消息 -->
          <div v-if="messages.length === 0" class="text-center py-8 animate-fade-in">
            <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-zhishu-100 to-zhishu-50 flex items-center justify-center text-3xl mx-auto mb-4 shadow-lg">
              {{ agent.icon }}
            </div>
            <p class="text-slate-600 font-medium">你好！我是 {{ agent.name }}</p>
            <p class="text-slate-400 text-sm mt-2">有什么可以帮助你的吗？</p>
          </div>
          
          <!-- 消息气泡 -->
          <div 
            v-for="(msg, idx) in messages" 
            :key="idx"
            :class="[
              'message-bubble animate-slide-up',
              msg.role === 'user' ? 'user' : 'agent'
            ]"
          >
            {{ msg.content }}
          </div>
          
          <!-- 加载中 -->
          <div v-if="isLoading" class="message-bubble agent flex items-center gap-2">
            <div class="flex gap-1">
              <div class="w-2 h-2 rounded-full bg-zhishu-300 animate-bounce" style="animation-delay: 0ms"></div>
              <div class="w-2 h-2 rounded-full bg-zhishu-300 animate-bounce" style="animation-delay: 150ms"></div>
              <div class="w-2 h-2 rounded-full bg-zhishu-300 animate-bounce" style="animation-delay: 300ms"></div>
            </div>
            <span class="text-slate-400 text-sm">正在思考...</span>
          </div>
          
          <!-- 错误提示 -->
          <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
            {{ error }}
            <button @click="error = ''" class="ml-2 text-red-400 hover:text-red-600">关闭</button>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="p-4 bg-slate-50 border-t border-slate-200/50">
          <div class="flex gap-3">
            <textarea 
              v-model="inputText"
              placeholder="输入消息，Ctrl+Enter 发送..."
              class="flex-1 p-4 bg-white border border-slate-200 rounded-xl outline-none focus:border-zhishu-300 focus:ring-2 focus:ring-zhishu-100 resize-none text-slate-700 placeholder:text-slate-400"
              rows="2"
              @keyup.ctrl.enter="sendMessage"
              :disabled="isLoading"
            />
            <button 
              @click="sendMessage"
              :disabled="isLoading || !inputText.trim()"
              class="px-6 py-4 btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <span>发送</span>
              <span class="text-sm opacity-70">↵</span>
            </button>
          </div>
          <div class="flex items-center justify-between mt-3">
            <p class="text-xs text-slate-400">
              ⚡ AI智能对话 · 支持多轮对话
            </p>
            <button 
              v-if="messages.length > 0"
              @click="clearChat"
              class="text-xs text-slate-400 hover:text-red-500 transition"
            >
              清空对话
            </button>
          </div>
        </div>
      </div>
      
      <!-- 快捷操作 -->
      <div class="mt-6 flex flex-wrap gap-2">
        <button 
          v-for="prompt in quickPrompts" 
          :key="prompt"
          @click="inputText = prompt"
          class="px-4 py-2 bg-white text-slate-600 rounded-lg border border-slate-200 hover:border-zhishu-300 hover:bg-zhishu-50 transition text-sm"
        >
          {{ prompt }}
        </button>
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
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'

interface Agent {
  id: number
  name: string
  icon: string
  description: string
}

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const agent = ref<Agent | null>(null)
const messages = ref<Message[]>([])
const inputText = ref('')
const isLoading = ref(false)
const error = ref('')
const route = useRoute()
const messagesContainer = ref<HTMLElement | null>(null)

// 快捷提示词
const quickPrompts = [
  '你好！',
  '介绍一下你自己',
  '你能帮我做什么？',
  '给我一个建议',
]

// 发送消息
const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return
  
  const userMsg = inputText.value.trim()
  messages.value.push({ role: 'user', content: userMsg })
  inputText.value = ''
  isLoading.value = true
  error.value = ''
  
  // 构建对话历史
  const history = messages.value.slice(0, -1).map(m => ({
    role: m.role,
    content: m.content
  }))
  
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agent_id: agent.value?.id,
        message: userMsg,
        history: history
      })
    })
    
    const data = await res.json()
    
    if (data.success) {
      messages.value.push({ role: 'assistant', content: data.reply })
    } else {
      error.value = data.error || '发送失败，请重试'
    }
  } catch (e) {
    error.value = '网络错误，请检查连接'
  }
  
  isLoading.value = false
  
  // 滚动到底部
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 清空对话
const clearChat = () => {
  messages.value = []
  error.value = ''
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