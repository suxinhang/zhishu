<template>
  <div class="chat-page">
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <a href="/agents" class="back-link">← 返回</a>
        <div class="agent-info" v-if="agent">
          <span class="agent-icon">{{ agent.icon }}</span>
          <span class="agent-name">{{ agent.name }}</span>
        </div>
        <button @click="toggleDark" class="dark-toggle" :title="isDark ? '切换亮色模式' : '切换暗黑模式'">
          <svg v-if="isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"/>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- 消息列表 -->
    <main class="main">
      <div class="container">
        <div class="messages" ref="messagesRef">
          <div 
            v-for="(msg, idx) in messages" 
            :key="idx"
            :class="['message', msg.role]"
          >
            <div class="message-content">{{ msg.content }}</div>
          </div>
          
          <div v-if="loading" class="message agent">
            <div class="message-content loading">正在思考...</div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入框 -->
    <footer class="footer">
      <div class="container">
        <div class="input-area">
          <textarea 
            v-model="inputText"
            placeholder="输入消息..."
            @keydown.enter.ctrl="sendMessage"
            rows="2"
          />
          <button @click="sendMessage" :disabled="loading || !inputText.trim()">
            发送
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 暗黑模式
const isDark = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('darkMode')
  if (saved) {
    isDark.value = saved === 'true'
  } else {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  updateTheme()
  loadAgent()
})

watch(isDark, updateTheme)

const updateTheme = () => {
  localStorage.setItem('darkMode', isDark.value)
  document.documentElement.classList.toggle('dark', isDark.value)
}

const toggleDark = () => {
  isDark.value = !isDark.value
}

const agent = ref(null)
const messages = ref([])
const inputText = ref('')
const loading = ref(false)
const messagesRef = ref(null)

const loadAgent = async () => {
  const res = await fetch(`/api/agents/${route.params.id}`)
  agent.value = await res.json()
}

const sendMessage = async () => {
  if (!inputText.value.trim() || loading.value) return
  
  const userMsg = inputText.value.trim()
  messages.value.push({ role: 'user', content: userMsg })
  inputText.value = ''
  loading.value = true
  
  await nextTick()
  scrollToBottom()
  
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agent_id: parseInt(route.params.id),
        message: userMsg
      })
    })
    
    const data = await res.json()
    messages.value.push({ role: 'agent', content: data.response })
  } catch (e) {
    messages.value.push({ role: 'agent', content: '抱歉，发生错误，请稍后再试。' })
  }
  
  loading.value = false
  await nextTick()
  scrollToBottom()
}

const scrollToBottom = () => {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

onMounted(loadAgent)
</script>

<style scoped>
.chat-page {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
  width: 100%;
}

/* 头部 */
.header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header .container {
  display: flex;
  align-items: center;
  height: 52px;
  gap: 16px;
}

.back-link {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.agent-icon {
  font-size: 20px;
}

.agent-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--text);
}

/* 消息 */
.main {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
}

.message.user .message-content {
  background: var(--primary);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message.agent .message-content {
  background: var(--bg-card);
  color: var(--text);
  border-bottom-left-radius: 4px;
  border: 1px solid var(--border);
}

.message-content.loading {
  color: var(--text-muted);
}

/* 输入框 */
.footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  padding: 12px 0;
}

.input-area {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: 20px;
  font-size: 14px;
  resize: none;
  outline: none;
  background: var(--bg);
  color: var(--text);
}

textarea:focus {
  border-color: var(--primary);
}

button {
  padding: 12px 24px;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>