<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- 搜索区域 -->
    <div class="text-center py-12">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">知枢 · 智能体开发平台</h1>
      <p class="text-gray-500 mb-8">发现、体验各类智能 AI 助手</p>
      <div class="max-w-xl mx-auto">
        <div class="flex bg-white rounded-full shadow-lg border border-gray-200">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜索智能体..."
            class="flex-1 px-6 py-3 rounded-full outline-none"
            @keyup.enter="searchAgents"
            @focus="showHistory = true"
            @blur="hideHistory"
          />
          <button 
            @click="searchAgents"
            class="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition"
          >
            搜索
          </button>
        </div>
        
        <!-- 搜索历史 -->
        <div v-if="showHistory && searchHistory.length > 0" class="mt-2 bg-white rounded-lg shadow-md p-3">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-500">搜索历史</span>
            <button @click="clearHistory" class="text-sm text-red-500 hover:text-red-700">清空</button>
          </div>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="(item, idx) in searchHistory" 
              :key="idx"
              @click="useHistory(item)"
              class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 text-sm"
            >
              {{ item }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门智能体 -->
    <div v-if="hotAgents.length > 0" class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        🔥 热门智能体
      </h2>
      <div class="flex gap-4 overflow-x-auto pb-2">
        <div 
          v-for="agent in hotAgents" 
          :key="agent.id"
          @click="goToChat(agent.id)"
          class="flex-shrink-0 w-48 bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-4 cursor-pointer hover:shadow-lg transition"
        >
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center text-xl">
              {{ agent.icon }}
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 truncate">{{ agent.name }}</h3>
              <div class="flex items-center gap-1 text-sm">
                <span class="text-yellow-500">⭐</span>
                <span class="text-gray-600">{{ agent.rating }}</span>
              </div>
            </div>
          </div>
          <p class="text-xs text-gray-500 truncate">{{ agent.description }}</p>
          <div class="mt-2 flex items-center gap-1 text-xs text-orange-600">
            🔥 {{ agent.hot_score }} 热度
          </div>
        </div>
      </div>
    </div>

    <!-- 排序和筛选 -->
    <div class="flex flex-wrap items-center gap-4 mb-8">
      <!-- 排序 -->
      <div class="flex gap-2">
        <button 
          @click="sortBy('hot')"
          :class="[
            'px-4 py-2 rounded-full transition',
            currentSort === 'hot' 
              ? 'bg-orange-600 text-white' 
              : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
          ]"
        >
          🔥 热门
        </button>
        <button 
          @click="sortBy('rating')"
          :class="[
            'px-4 py-2 rounded-full transition',
            currentSort === 'rating' 
              ? 'bg-yellow-500 text-white' 
              : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
          ]"
        >
          ⭐ 高评分
        </button>
        <button 
          @click="sortBy()"
          :class="[
            'px-4 py-2 rounded-full transition',
            !currentSort 
              ? 'bg-blue-600 text-white' 
              : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
          ]"
        >
          📋 默认
        </button>
      </div>
      
      <!-- 分类筛选 -->
      <div class="flex flex-wrap gap-2">
        <button 
          @click="selectCategory(null)"
          :class="[
            'px-3 py-1.5 rounded-full transition text-sm',
            !selectedCategory 
              ? 'bg-blue-600 text-white' 
              : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
          ]"
        >
          全部
        </button>
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="selectCategory(cat.id)"
          :class="[
            'px-3 py-1.5 rounded-full transition text-sm',
            selectedCategory === cat.id 
              ? 'bg-blue-600 text-white' 
              : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
          ]"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>
      </div>
    </div>

    <!-- 智能体卡片列表 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <AgentCard 
        v-for="agent in filteredAgents" 
        :key="agent.id"
        :agent="agent"
        @rated="loadAgents"
      />
    </div>

    <!-- 空状态 -->
    <div v-if="filteredAgents.length === 0" class="text-center py-12 text-gray-400">
      暂无匹配的智能体
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AgentCard from '../components/AgentCard.vue'
import { useRouter } from 'vue-router'

interface Agent {
  id: number
  name: string
  icon: string
  description: string
  category_name?: string
  rating: number
  rating_count: number
  hot_score?: number
}

interface Category {
  id: number
  name: string
  icon: string
}

const agents = ref<Agent[]>([])
const hotAgents = ref<Agent[]>([])
const categories = ref<Category[]>([])
const searchQuery = ref('')
const selectedCategory = ref<number | null>(null)
const currentSort = ref<string | null>(null)
const searchHistory = ref<string[]>([])
const showHistory = ref(false)
const router = useRouter()

// 加载搜索历史
const loadHistory = () => {
  const history = localStorage.getItem('searchHistory')
  if (history) {
    searchHistory.value = JSON.parse(history)
  }
}

// 保存搜索历史
const saveHistory = (query: string) => {
  if (!query.trim()) return
  const history = [...new Set([query, ...searchHistory.value])].slice(0, 10)
  searchHistory.value = history
  localStorage.setItem('searchHistory', JSON.stringify(history))
}

// 清空历史
const clearHistory = () => {
  searchHistory.value = []
  localStorage.removeItem('searchHistory')
}

// 使用历史记录
const useHistory = (item: string) => {
  searchQuery.value = item
  showHistory.value = false
  searchAgents()
}

// 隐藏历史（延迟以允许点击）
const hideHistory = () => {
  setTimeout(() => {
    showHistory.value = false
  }, 200)
}

const filteredAgents = computed(() => {
  let result = agents.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(a => 
      a.name.toLowerCase().includes(query) || 
      a.description.toLowerCase().includes(query)
    )
  }
  
  return result
})

const selectCategory = (catId: number | null) => {
  selectedCategory.value = catId
  loadAgents()
}

const sortBy = (sort?: string) => {
  currentSort.value = sort || null
  loadAgents()
}

const searchAgents = () => {
  if (searchQuery.value.trim()) {
    saveHistory(searchQuery.value.trim())
  }
  showHistory.value = false
}

const goToChat = (id: number) => {
  router.push(`/chat/${id}`)
}

const loadAgents = async () => {
  try {
    const params = new URLSearchParams()
    if (selectedCategory.value) params.append('category', selectedCategory.value.toString())
    if (currentSort.value) params.append('sort', currentSort.value)
    
    const res = await fetch(`/api/agents?${params}`)
    agents.value = await res.json()
  } catch (e) {
    console.error('Failed to load agents:', e)
  }
}

const loadHotAgents = async () => {
  try {
    const res = await fetch('/api/agents/hot')
    hotAgents.value = await res.json()
  } catch (e) {
    console.error('Failed to load hot agents:', e)
  }
}

const loadCategories = async () => {
  try {
    const res = await fetch('/api/categories')
    categories.value = await res.json()
  } catch (e) {
    console.error('Failed to load categories:', e)
  }
}

onMounted(async () => {
  loadHistory()
  await Promise.all([loadAgents(), loadHotAgents(), loadCategories()])
})
</script>