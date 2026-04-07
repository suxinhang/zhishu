<template>
  <div class="max-w-7xl mx-auto px-6 py-8">
    <!-- Hero 区域 -->
    <div class="text-center py-16 animate-fade-in">
      <!-- 主标题 -->
      <div class="flex items-center justify-center gap-3 mb-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-zhishu-800 to-zhishu-600 flex items-center justify-center shadow-lg">
          <span class="text-2xl">🧠</span>
        </div>
        <h1 class="text-4xl font-bold gradient-text">知枢</h1>
      </div>
      
      <!-- 副标题 -->
      <p class="text-slate-500 mb-2 text-lg">发现你的智能伙伴</p>
      <p class="text-slate-400 text-sm">聚合全网优质 AI 智能体，即开即用，无需注册</p>
      
      <!-- 搜索框 -->
      <div class="max-w-2xl mx-auto mt-10">
        <div class="search-box flex items-center px-6 py-4">
          <span class="text-slate-400 mr-3">🔍</span>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜索智能体..."
            class="flex-1 outline-none text-slate-700 placeholder:text-slate-400"
            @keyup.enter="searchAgents"
            @focus="showHistory = true"
            @blur="hideHistory"
          />
          <button 
            @click="searchAgents"
            class="px-6 py-2 bg-gradient-to-r from-zhishu-800 to-zhishu-600 text-white rounded-full hover:shadow-lg transition-all duration-200 font-medium"
          >
            搜索
          </button>
        </div>
        
        <!-- 搜索历史 -->
        <div 
          v-if="showHistory && searchHistory.length > 0" 
          class="mt-3 bg-white rounded-xl shadow-lg p-4 animate-slide-up"
        >
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-slate-500 flex items-center gap-1">
              <span>🕐</span> 搜索历史
            </span>
            <button 
              @click="clearHistory" 
              class="text-sm text-slate-400 hover:text-red-500 transition"
            >
              清空
            </button>
          </div>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="(item, idx) in searchHistory" 
              :key="idx"
              @click="useHistory(item)"
              class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg hover:bg-zhishu-50 hover:text-zhishu-600 transition text-sm"
            >
              {{ item }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门智能体横向滚动 -->
    <div v-if="hotAgents.length > 0" class="mb-12">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-slate-800 flex items-center gap-2">
          <span class="text-amber-400">🔥</span> 
          <span>热门智能体</span>
          <span class="text-sm text-slate-400 ml-2">实时热度排行</span>
        </h2>
        <router-link 
          to="/category" 
          class="text-sm text-zhishu-600 hover:text-zhishu-700 transition flex items-center gap-1"
        >
          查看全部 <span>→</span>
        </router-link>
      </div>
      
      <div class="flex gap-4 overflow-x-auto pb-4 snap-x snap-mandatory scrollbar-hide">
        <div 
          v-for="agent in hotAgents" 
          :key="agent.id"
          @click="goToChat(agent.id)"
          class="flex-shrink-0 w-52 bg-white rounded-xl shadow-card hover:shadow-card-hover cursor-pointer transition-all duration-300 hover:-translate-y-2 snap-start overflow-hidden"
        >
          <!-- 顶部热度条 -->
          <div class="h-1.5 bg-gradient-to-r from-amber-400 via-amber-500 to-orange-400"></div>
          
          <div class="p-4">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-50 to-amber-100 flex items-center justify-center text-2xl shadow-inner">
                {{ agent.icon }}
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-slate-800 truncate">{{ agent.name }}</h3>
                <div class="flex items-center gap-1 mt-1">
                  <span class="text-amber-400 text-sm">★</span>
                  <span class="text-sm text-slate-600">{{ agent.rating }}</span>
                </div>
              </div>
            </div>
            <p class="text-xs text-slate-500 truncate mb-3">{{ agent.description }}</p>
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 bg-zhishu-50 text-zhishu-600 rounded text-xs">{{ agent.category_name || '其他' }}</span>
              <span class="text-xs text-amber-500 font-medium flex items-center gap-0.5">
                🔥 {{ agent.hot_score }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和排序区域 -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-8 p-4 bg-white/50 rounded-xl border border-slate-200/50">
      <!-- 排序按钮 -->
      <div class="flex gap-2">
        <button 
          @click="sortBy('hot')"
          :class="[
            'category-tag px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-1.5',
            currentSort === 'hot' 
              ? 'active' 
              : 'text-slate-600 hover:bg-zhishu-50'
          ]"
        >
          <span>🔥</span> 热门
        </button>
        <button 
          @click="sortBy('rating')"
          :class="[
            'category-tag px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-1.5',
            currentSort === 'rating' 
              ? 'active' 
              : 'text-slate-600 hover:bg-zhishu-50'
          ]"
        >
          <span>⭐</span> 高评分
        </button>
        <button 
          @click="sortBy()"
          :class="[
            'category-tag px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-1.5',
            !currentSort 
              ? 'active' 
              : 'text-slate-600 hover:bg-zhishu-50'
          ]"
        >
          <span>📋</span> 默认
        </button>
      </div>
      
      <!-- 分类筛选 -->
      <div class="flex flex-wrap gap-2">
        <button 
          @click="selectCategory(null)"
          :class="[
            'category-tag px-3 py-1.5 rounded-lg transition-all duration-200 text-sm',
            !selectedCategory 
              ? 'active' 
              : 'text-slate-600 hover:bg-zhishu-50'
          ]"
        >
          全部
        </button>
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="selectCategory(cat.id)"
          :class="[
            'category-tag px-3 py-1.5 rounded-lg transition-all duration-200 text-sm flex items-center gap-1',
            selectedCategory === cat.id 
              ? 'active' 
              : 'text-slate-600 hover:bg-zhishu-50'
          ]"
        >
          <span>{{ cat.icon }}</span> {{ cat.name }}
        </button>
      </div>
    </div>

    <!-- 智能体卡片网格 -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <AgentCard 
        v-for="agent in filteredAgents" 
        :key="agent.id"
        :agent="agent"
        @rated="loadAgents"
      />
    </div>

    <!-- 空状态 -->
    <div v-if="filteredAgents.length === 0" class="text-center py-16 animate-fade-in">
      <div class="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mx-auto mb-4">
        🔍
      </div>
      <p class="text-slate-400 text-lg">暂无匹配的智能体</p>
      <p class="text-slate-300 text-sm mt-2">试试其他关键词或分类</p>
    </div>
    
    <!-- 加载更多提示 -->
    <div v-if="filteredAgents.length > 0 && filteredAgents.length >= 20" class="text-center py-8">
      <button 
        @click="loadMore"
        class="px-6 py-3 bg-white text-slate-600 rounded-xl border border-slate-200 hover:border-zhishu-300 hover:bg-zhishu-50 transition-all duration-200"
      >
        加载更多智能体
      </button>
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

const loadMore = () => {
  // TODO: 实现分页加载
  console.log('Load more agents...')
}

onMounted(async () => {
  loadHistory()
  await Promise.all([loadAgents(), loadHotAgents(), loadCategories()])
})
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>