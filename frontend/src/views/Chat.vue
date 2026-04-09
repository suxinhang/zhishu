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
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
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
  background: #f5f5f5;
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
  background: #fff;
  border-bottom: 1px solid #eee;
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
  color: #666;
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
  background: #1a1a1a;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message.agent .message-content {
  background: #fff;
  color: #1a1a1a;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.message-content.loading {
  color: #999;
}

/* 输入框 */
.footer {
  background: #fff;
  border-top: 1px solid #eee;
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
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  resize: none;
  outline: none;
}

textarea:focus {
  border-color: #1a1a1a;
}

button {
  padding: 12px 24px;
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>