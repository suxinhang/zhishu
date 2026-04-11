<template>
  <div class="chat-page">
    <!-- 科技感背景 -->
    <div class="tech-bg">
      <div class="matrix-rain"></div>
    </div>
    
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <a href="/agents" class="back-link">← 返回</a>
        <div class="agent-info" v-if="agent">
          <span class="agent-icon">{{ agent.icon }}</span>
          <span class="agent-name">{{ agent.name }}</span>
        </div>
        <DarkModeToggle />
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
            <div class="message-content">
              <!-- 用户消息：纯文本 -->
              <template v-if="msg.role === 'user'">
                {{ msg.content }}
              </template>
              <!-- AI消息：Markdown渲染 -->
              <template v-else>
                <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
              </template>
            </div>
          </div>
          
          <!-- 打字机效果 -->
          <div v-if="typingText" class="message agent">
            <div class="message-content">
              <div class="markdown-body" v-html="renderMarkdown(typingText)"}></div>
              <span class="typing-cursor">▌</span>
            </div>
          </div>
          
          <!-- PPT生成按钮（仅PPT大纲助手） -->
          <div v-if="pptData && agent && agent.id === 24" class="ppt-action">
            <button @click="generatePPT" class="btn-ppt">
              📊 下载 PPT 文件 (.pptx)
            </button>
          </div>
          
          <div v-if="loading && !typingText" class="message agent">
            <div class="message-content loading">
              <span class="loading-dots">
                <span></span><span></span><span></span>
              </span>
              正在思考...
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入框 -->
    <footer class="footer">
      <div class="container">
        <div class="input-options">
          <button 
            @click="toggleEnterMode" 
            class="enter-mode-btn"
            :title="enterToSend ? '当前: Enter发送' : '当前: Enter换行'"
          >
            {{ enterToSend ? '↵ 发送' : '↵ 换行' }}
          </button>
        </div>
        <div class="input-area">
          <textarea 
            v-model="inputText"
            :placeholder="enterToSend ? '输入消息... (Enter发送, Shift+Enter换行)' : '输入消息... (Enter换行, Ctrl+Enter发送)'"
            @keydown.enter.exact="handleEnter"
            rows="2"
          />
          <button @click="sendMessage()" :disabled="loading || !inputText.trim()">
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
import { marked } from 'marked'
import DarkModeToggle from '@/components/DarkModeToggle.vue'

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true
})

const route = useRoute()

// Enter键模式
const enterToSend = ref(true)

// 打字机效果
const typingText = ref('')
const typingTimer = ref(null)

// Markdown渲染
const renderMarkdown = (text) => {
  return marked.parse(text || '')
}

const toggleEnterMode = () => {
  enterToSend.value = !enterToSend.value
  localStorage.setItem('enterToSend', enterToSend.value)
}

const handleEnter = (e) => {
  if (enterToSend.value) {
    if (!e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  } else {
    if (e.ctrlKey) {
      e.preventDefault()
      sendMessage()
    }
  }
}

// 打字机效果函数
const typeWriter = (text, speed = 30) => {
  typingText.value = ''
  let index = 0
  
  // 清除之前的定时器
  if (typingTimer.value) {
    clearInterval(typingTimer.value)
  }
  
  typingTimer.value = setInterval(() => {
    if (index < text.length) {
      typingText.value += text.charAt(index)
      index++
      scrollToBottom()
    } else {
      clearInterval(typingTimer.value)
      typingTimer.value = null
      // 完成后添加到消息列表
      messages.value.push({ role: 'agent', content: text })
      typingText.value = ''
      loading.value = false
      // 尝试解析PPT JSON（仅当agent_id为24时）
      lastResponse.value = text
      if (agent.value && agent.value.id === 24) {
        pptData.value = parsePPTJson(text)
      }
    }
  }, speed)
}

onMounted(() => {
  const savedEnterMode = localStorage.getItem('enterToSend')
  if (savedEnterMode !== null) {
    enterToSend.value = savedEnterMode === 'true'
  }
  
  loadAgent()
})

const agent = ref(null)
const messages = ref([])
const inputText = ref('')
const loading = ref(false)
const messagesRef = ref(null)
const pptData = ref(null)  // 存储解析后的PPT JSON数据
const lastResponse = ref('')  // 存储最后一条AI回复

// 尝试解析PPT JSON结构
const parsePPTJson = (text) => {
  try {
    // 尝试从文本中提取JSON
    const jsonMatch = text.match(/```json\s*([\s\S]*?)\s*```/)
    if (jsonMatch) {
      return JSON.parse(jsonMatch[1])
    }
    // 尝试直接解析
    const directJson = JSON.parse(text)
    if (directJson.topic && directJson.pages) {
      return directJson
    }
  } catch (e) {
    // 解析失败，返回null
  }
  return null
}

// 生成PPT文件
const generatePPT = async () => {
  if (!pptData.value) return
  
  try {
    const res = await fetch('/api/ppt/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pptData.value)
    })
    
    // 下载文件
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${pptData.value.topic || 'PPT'}.pptx`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    alert('生成PPT失败，请稍后再试')
  }
}

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
    // 使用打字机效果展示回复
    typeWriter(data.response, 25)
  } catch (e) {
    messages.value.push({ role: 'agent', content: '抱歉，发生错误，请稍后再试。' })
    loading.value = false
  }
  
  await nextTick()
  scrollToBottom()
}

const scrollToBottom = () => {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}
</script>

<style scoped>
/* 科技感背景 */
.tech-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.matrix-rain {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(ellipse at top, rgba(79, 70, 229, 0.1) 0%, transparent 50%),
    radial-gradient(ellipse at bottom, rgba(79, 70, 229, 0.05) 0%, transparent 70%);
  animation: matrix-shift 15s ease-in-out infinite alternate;
}

@keyframes matrix-shift {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}

.chat-page {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  position: relative;
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
  line-height: 1.6;
}

.message.user .message-content {
  background: linear-gradient(135deg, var(--primary) 0%, #6366f1 100%);
  color: #fff;
  border-bottom-right-radius: 4px;
  box-shadow: 0 2px 10px rgba(79, 70, 229, 0.3);
}

.message.agent .message-content {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  color: var(--text);
  border-bottom-left-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.message-content.loading {
  color: var(--text-muted);
}

/* 加载动画 */
.loading-dots {
  display: inline-flex;
  gap: 4px;
  margin-right: 8px;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(1) { animation-delay: 0s; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
}

/* 打字机光标 */
.typing-cursor {
  color: var(--primary);
  animation: blink 1s step-end infinite;
  margin-left: 2px;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Markdown样式 */
.markdown-body {
  line-height: 1.6;
}

.markdown-body p {
  margin: 0 0 8px;
}

.markdown-body p:last-child {
  margin-bottom: 0;
}

.markdown-body code {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.markdown-body pre {
  background: rgba(0, 0, 0, 0.1);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.markdown-body pre code {
  background: none;
  padding: 0;
}

.markdown-body ul, .markdown-body ol {
  padding-left: 20px;
  margin: 8px 0;
}

.markdown-body li {
  margin: 4px 0;
}

.markdown-body strong {
  font-weight: 600;
}

.markdown-body a {
  color: var(--primary);
  text-decoration: none;
}

/* 输入框 */
.footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  padding: 12px 0;
}

.input-options {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}

.enter-mode-btn {
  font-size: 12px;
  padding: 4px 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.enter-mode-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
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
  transition: all 0.2s;
}

button:hover:not(:disabled) {
  background: #6366f1;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* PPT生成按钮 */
.ppt-action {
  display: flex;
  justify-content: center;
  padding: 20px;
  margin-top: 10px;
}

.btn-ppt {
  background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-ppt:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.dark .btn-ppt {
  background: linear-gradient(135deg, #667EEA 0%, #9333EA 100%);
}
</style>