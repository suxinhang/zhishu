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
              <div class="markdown-body" v-html="renderMarkdown(typingText)"></div>
              <span class="typing-cursor">▌</span>
            </div>
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
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true
})

const route = useRoute()

// 暗黑模式
const isDark = ref(false)

// Enter键模式
const enterToSend = ref(true)

// 打字机效果
const typingText = ref('')
const typingTimer = ref(null)

// Markdown渲染
const renderMarkdown = (text) => {
  return marked.parse(text || '')
}

const updateTheme = () => {
  localStorage.setItem('darkMode', isDark.value)
  document.documentElement.classList.toggle('dark', isDark.value)
}

const toggleDark = () => {
  isDark.value = !isDark.value
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
    }
  }, speed)
}

onMounted(() => {
  const saved = localStorage.getItem('darkMode')
  if (saved) {
    isDark.value = saved === 'true'
  } else {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  updateTheme()
  
  const savedEnterMode = localStorage.getItem('enterToSend')
  if (savedEnterMode !== null) {
    enterToSend.value = savedEnterMode === 'true'
  }
  
  loadAgent()
})

watch(isDark, updateTheme)

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
</style>