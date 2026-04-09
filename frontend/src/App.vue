<template>
  <div class="app" :class="{ dark: isDark }">
    <nav class="nav">
      <div class="nav-container">
        <a href="/tgmeng" class="nav-link">热榜</a>
        <a href="/agents" class="nav-link">智能体</a>
        <button @click="toggleDark" class="dark-btn">
          {{ isDark ? '☀️' : '🌙' }}
        </button>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterView } from 'vue-router'

const isDark = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('darkMode')
  if (saved) {
    isDark.value = saved === 'true'
  } else {
    // 默认跟随系统
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
})

watch(isDark, (val) => {
  localStorage.setItem('darkMode', val)
})

const toggleDark = () => {
  isDark.value = !isDark.value
}
</script>

<style>
/* 暗黑模式变量 */
.app {
  --bg: #f5f5f5;
  --bg-card: #fff;
  --text: #1a1a1a;
  --text-muted: #666;
  --border: #eee;
  --border-light: #f0f0f0;
  --primary: #4F46E5;
}

.app.dark {
  --bg: #1a1a1a;
  --bg-card: #262626;
  --text: #f5f5f5;
  --text-muted: #999;
  --border: #333;
  --border-light: #404040;
  --primary: #6366F1;
}

/* 全局样式 */
body {
  background: var(--bg);
  color: var(--text);
  transition: background 0.3s, color 0.3s;
}

/* 导航 */
.nav {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
}

.nav-link {
  color: var(--text);
  text-decoration: none;
  margin-right: 24px;
  font-size: 14px;
}

.nav-link:hover {
  color: var(--primary);
}

.dark-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 4px 12px;
  font-size: 16px;
  cursor: pointer;
  color: var(--text);
}

.dark-btn:hover {
  background: var(--border);
}
</style>