<template>
  <div class="max-w-7xl mx-auto px-6 py-8">
    <!-- Hero 区域 -->
    <div class="text-center py-12 animate-fade-in">
      <div class="flex items-center justify-center gap-3 mb-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg">
          <span class="text-2xl">🔥</span>
        </div>
        <h1 class="text-4xl font-bold gradient-text">知枢热榜</h1>
      </div>
      
      <p class="text-slate-500 mb-2 text-lg">全网热点，一角尽览</p>
      <p class="text-slate-400 text-sm">聚合微博、知乎、抖音、百度等各大平台热榜</p>
      
      <!-- 搜索框 -->
      <div class="max-w-2xl mx-auto mt-10">
        <div class="search-box flex items-center px-6 py-4">
          <span class="text-slate-400 mr-3">🔍</span>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜索热点..."
            class="flex-1 outline-none text-slate-700 placeholder:text-slate-400"
            @keyup.enter="searchTopics"
            @focus="showHistory = true"
            @blur="hideHistory"
          />
          <button 
            @click="searchTopics"
            class="px-6 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-full hover:shadow-lg transition-all duration-200 font-medium"
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
              class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg hover:bg-amber-50 hover:text-amber-600 transition text-sm"
            >
              {{ item }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门热点横向滚动 -->
    <div v-if="hotTopics.length > 0" class="mb-10">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-slate-800 flex items-center gap-2">
          <span class="text-2xl">🔥</span> 
          <span>热门 TOP 10</span>
          <span class="text-sm text-slate-400 ml-2">实时热度排行</span>
        </h2>
      </div>
      
      <div class="flex gap-4 overflow-x-auto pb-4 snap-x snap-mandatory scrollbar-hide">
        <div 
          v-for="(topic, idx) in hotTopics" 
          :key="topic.id"
          class="flex-shrink-0 w-60 bg-white rounded-xl shadow-card hover:shadow-card-hover cursor-pointer transition-all duration-300 hover:-translate-y-2 snap-start overflow-hidden"
        >
          <!-- 热度条 -->
          <div class="h-1.5 bg-gradient-to-r from-amber-400 via-orange-500 to-red-500"></div>
          
          <div class="p-4">
            <!-- 排名标识 -->
            <div class="flex items-center justify-between mb-3">
              <span class="px-2 py-1 bg-amber-100 text-amber-600 rounded text-xs font-bold">
                TOP {{ idx + 1 }}
              </span>
              <span class="text-sm text-slate-500">{{ topic.platform_icon }} {{ topic.platform_name }}</span>
            </div>
            
            <h3 class="font-semibold text-slate-800 line-clamp-2 mb-3">{{ topic.title }}</h3>
            
            <div class="flex items-center justify-between">
              <span class="text-amber-500 font-medium flex items-center gap-1">
                🔥 {{ formatHotValue(topic.hot_value) }}
              </span>
              <button 
                @click="goToTopic(topic.id)"
                class="text-xs text-zhishu-600 hover:text-zhishu-700 flex items-center gap-1"
              >
                查看 →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 平台筛选 -->
    <div class="flex flex-wrap items-center gap-4 mb-8 p-4 bg-white/50 rounded-xl border border-slate-200/50">
      <span class="text-sm text-slate-500">平台筛选：</span>
      <div class="flex flex-wrap gap-2">
        <button 
          @click="selectPlatform(null)"
          :class="[
            'category-tag px-3 py-1.5 rounded-lg transition-all duration-200 text-sm',
            !selectedPlatform ? 'active' : 'text-slate-600 hover:bg-amber-50'
          ]"
        >
          全部
        </button>
        <button 
          v-for="plat in platforms" 
          :key="plat.id"
          @click="selectPlatform(plat.id)"
          :class="[
            'category-tag px-3 py-1.5 rounded-lg transition-all duration-200 text-sm flex items-center gap-1',
            selectedPlatform === plat.id ? 'active' : 'text-slate-600 hover:bg-amber-50'
          ]"
        >
          {{ plat.icon }} {{ plat.name }}
        </button>
      </div>
      
      <!-- 分类筛选 -->
      <div class="w-px h-6 bg-slate-200 mx-2"></div>
      <span class="text-sm text-slate-500">分类：</span>
      <div class="flex flex-wrap gap-2">
        <button 
          @click="selectCategory(null)"
          :class="[
            'category-tag px-3 py-1.5 rounded-lg transition-all duration-200 text-sm',
            !selectedCategory ? 'active' : 'text-slate-600 hover:bg-amber-50'
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
            selectedCategory === cat.id ? 'active' : 'text-slate-600 hover:bg-amber-50'
          ]"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>
      </div>
    </div>

    <!-- 热点卡片网格 -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div 
        v-for="topic in filteredTopics" 
        :key="topic.id"
        class="bg-white rounded-xl shadow-card card-glow cursor-pointer overflow-hidden"
        @click="goToTopic(topic.id)"
      >
        <!-- 顶部热度条 -->
        <div class="h-1 bg-gradient-to-r from-amber-400 via-orange-500 to-red-500 opacity-80"></div>
        
        <div class="p-5">
          <!-- 平台标识 -->
          <div class="flex items-center justify-between mb-3">
            <span class="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-medium">
              {{ topic.platform_name }}
            </span>
            <span class="text-xs text-slate-400">#{{ topic.rank }}</span>
          </div>
          
          <!-- 标题 -->
          <h3 class="font-semibold text-slate-800 line-clamp-2 mb-3 leading-snug">{{ topic.title }}</h3>
          
          <!-- 热度值 -->
          <div class="flex items-center gap-2 mb-3">
            <span class="hot-badge">
              🔥 {{ formatHotValue(topic.hot_value) }}
            </span>
          </div>
          
          <!-- 分类 -->
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-500">{{ topic.category_icon || '📋' }} {{ topic.category_name }}</span>
            <span class="text-xs text-zhishu-600 hover:text-zhishu-700">查看详情 →</span>
          </div>
        </div>
        
        <!-- 底部装饰 -->
        <div class="flex justify-center gap-2 py-2 opacity-40">
          <div class="w-2 h-2 rounded-full bg-amber-300"></div>
          <div class="w-2 h-2 rounded-full bg-orange-300"></div>
          <div class="w-2 h-2 rounded-full bg-amber-300"></div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredTopics.length === 0" class="text-center py-16 animate-fade-in">
      <div class="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mx-auto mb-4">
        🔍
      </div>
      <p class="text-slate-400 text-lg">暂无匹配的热点</p>
      <p class="text-slate-300 text-sm mt-2">试试其他筛选条件</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Platform {
  id: number
  name: string
  icon: string
  url: string
}

interface Category {
  id: number
  name: string
  icon: string
}

interface Topic {
  id: number
  title: string
  platform_id: number
  platform_name: string
  platform_icon: string
  category_id: number
  category_name: string
  category_icon: string
  hot_value: number
  rank: number
  url: string
  summary: string
}

const topics = ref<Topic[]>([])
const hotTopics = ref<Topic[]>([])
const platforms = ref<Platform[]>([])
const categories = ref<Category[]>([])
const searchQuery = ref('')
const selectedPlatform = ref<number | null>(null)
const selectedCategory = ref<number | null>(null)
const searchHistory = ref<string[]>([])
const showHistory = ref(false)
const router = useRouter()

// 格式化热度值
const formatHotValue = (value: number) => {
  if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
  if (value >= 1000) return (value / 1000).toFixed(0) + 'K'
  return value.toString()
}

// 加载搜索历史
const loadHistory = () => {
  const history = localStorage.getItem('topicSearchHistory')
  if (history) {
    searchHistory.value = JSON.parse(history)
  }
}

const saveHistory = (query: string) => {
  if (!query.trim()) return
  const history = [...new Set([query, ...searchHistory.value])].slice(0, 10)
  searchHistory.value = history
  localStorage.setItem('topicSearchHistory', JSON.stringify(history))
}

const clearHistory = () => {
  searchHistory.value = []
  localStorage.removeItem('topicSearchHistory')
}

const useHistory = (item: string) => {
  searchQuery.value = item
  showHistory.value = false
  searchTopics()
}

const hideHistory = () => {
  setTimeout(() => {
    showHistory.value = false
  }, 200)
}

const filteredTopics = computed(() => {
  let result = topics.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(t => t.title.toLowerCase().includes(query))
  }
  
  return result
})

const selectPlatform = (platId: number | null) => {
  selectedPlatform.value = platId
  loadTopics()
}

const selectCategory = (catId: number | null) => {
  selectedCategory.value = catId
  loadTopics()
}

const searchTopics = () => {
  if (searchQuery.value.trim()) {
    saveHistory(searchQuery.value.trim())
  }
  showHistory.value = false
}

const goToTopic = (id: number) => {
  router.push(`/topic/${id}`)
}

const loadTopics = async () => {
  try {
    const params = new URLSearchParams()
    if (selectedPlatform.value) params.append('platform', selectedPlatform.value.toString())
    if (selectedCategory.value) params.append('category', selectedCategory.value.toString())
    params.append('sort', 'hot')
    
    const res = await fetch(`/api/topics?${params}`)
    topics.value = await res.json()
  } catch (e) {
    console.error('Failed to load topics:', e)
  }
}

const loadHotTopics = async () => {
  try {
    const res = await fetch('/api/topics/hot')
    hotTopics.value = await res.json()
  } catch (e) {
    console.error('Failed to load hot topics:', e)
  }
}

const loadPlatforms = async () => {
  try {
    const res = await fetch('/api/platforms')
    platforms.value = await res.json()
  } catch (e) {
    console.error('Failed to load platforms:', e)
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
  await Promise.all([loadTopics(), loadHotTopics(), loadPlatforms(), loadCategories()])
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>