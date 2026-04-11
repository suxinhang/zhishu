<template>
  <button 
    @click="toggleDark" 
    class="dark-toggle" 
    :title="isDark ? '切换亮色模式' : '切换暗黑模式'"
  >
    <!-- 太阳图标（暗黑模式时显示） -->
    <svg v-if="isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="5"/>
      <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
    </svg>
    <!-- 月亮图标（亮色模式时显示） -->
    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
    </svg>
  </button>
</template>

<script setup>
import { useDarkMode } from '@/composables/useDarkMode'

const { isDark, toggleDark } = useDarkMode()
</script>

<style scoped>
.dark-toggle {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: background 0.2s, border-color 0.2s;
}

.dark-toggle:hover {
  background: var(--border);
  border-color: var(--text-muted);
}

.dark-toggle svg {
  width: 18px;
  height: 18px;
}
</style>