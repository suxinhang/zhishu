import { ref, onMounted, watch } from 'vue'

// 全局状态（单例）
const isDark = ref(false)
let initialized = false

export function useDarkMode() {
  const updateTheme = () => {
    localStorage.setItem('darkMode', isDark.value)
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  const toggleDark = () => {
    isDark.value = !isDark.value
  }

  // 只初始化一次
  if (!initialized) {
    onMounted(() => {
      const saved = localStorage.getItem('darkMode')
      if (saved) {
        isDark.value = saved === 'true'
      } else {
        isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      updateTheme()
      initialized = true
    })

    watch(isDark, updateTheme)
  }

  return { isDark, toggleDark }
}