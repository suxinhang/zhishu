<template>
  <router-view />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
/* 全局变量 - 定义在 :root */
:root {
  --bg: #f5f5f5;
  --bg-card: #fff;
  --text: #1a1a1a;
  --text-muted: #666;
  --border: #eee;
  --border-light: #f0f0f0;
  --primary: #4F46E5;
}

/* 暗黑模式 - 定义在 html.dark */
html.dark {
  --bg: #1a1a1a;
  --bg-card: #262626;
  --text: #f5f5f5;
  --text-muted: #999;
  --border: #333;
  --border-light: #404040;
  --primary: #6366F1;
}

/* 全局样式 */
html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--text);
  transition: background 0.3s, color 0.3s;
}

#app {
  min-height: 100vh;
  background: var(--bg);
}

/* 暗黑模式切换按钮 */
.dark-toggle {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text);
  transition: background 0.2s;
}

.dark-toggle:hover {
  background: var(--border);
}

.dark-toggle svg {
  width: 18px;
  height: 18px;
}
</style>