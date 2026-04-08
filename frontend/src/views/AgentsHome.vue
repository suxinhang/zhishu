<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 搜索区域 -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-6xl mx-auto px-6 py-8">
        <!-- Logo + 搜索 -->
        <div class="flex items-center gap-6 mb-6">
          <div class="flex items-center gap-3">
            <span class="text-3xl">🔥</span>
            <h1 class="text-2xl font-bold text-gray-800">知枢热榜</h1>
          </div>
          <div class="flex-1 max-w-xl">
            <div class="relative">
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="搜索热点..."
                class="w-full px-4 py-2.5 pl-10 bg-gray-100 rounded-full text-sm outline-none focus:bg-white focus:ring-2 focus:ring-orange-300 transition"
                @input="filterTopics"
              />
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
            </div>
          </div>
        </div>
        
        <!-- 平台标签 -->
        <div class="flex items-center gap-2 flex-wrap">
          <button 
            v-for="plat in platforms"
            :key="plat.id"
            @click="selectPlatform(plat.id)"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
              selectedPlatform === plat.id 
                ? 'bg-orange-500 text-white shadow-md' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ plat.icon }} {{ plat.name }}
          </button>
          <button 
            @click="selectPlatform(null)"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
              selectedPlatform === null 
                ? 'bg-gray-800 text-white shadow-md' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            📋 全部
          </button>
        </div>
      </div>
    </div>
    
    <!-- 热点列表 -->
    <div class="max-w-6xl mx-auto px-6 py-6">
      <!-- 分类筛选 -->
      <div class="flex items-center gap-3 mb-4 text-sm">
        <span class="text-gray-500">分类：</span>
        <button 
          v-for="cat in categories"
          :key="cat.id"
          @click="selectCategory(cat.id)"
          :class="[
            'px-3 py-1 rounded transition',
            selectedCategory === cat.id 
              ? 'bg-blue-500 text-white' 
              : 'text-gray-600 hover:text-blue-500'
          ]"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>
        <button 
          @click="selectCategory(null)"
          :class="[
            'px-3 py-1 rounded transition',
            selectedCategory === null 
              ? 'bg-blue-500 text-white' 
              : 'text-gray-600 hover:text-blue-500'
          ]"
        >
          全部
        </button>
      </div>
      
      <!-- 热点表格 -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50 text-sm text-gray-500">
            <tr>
              <th class="w-16 px-4 py-3 text-left font-medium">排名</th>
              <th class="px-4 py-3 text-left font-medium">热点</th>
              <th class="w-32 px-4 py-3 text-left font-medium">热度</th>
              <th class="w-24 px-4 py-3 text-right font-medium">来源</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(topic, idx) in filteredTopics" 
              :key="topic.id"
              @click="goToTopic(topic.id)"
              class="border-t border-gray-100 hover:bg-orange-50 cursor-pointer transition-colors group"
            >
              <!-- 排名 -->
              <td class="px-4 py-4">
                <span 
                  :class="[
                    'inline-flex items-center justify-center w-7 h-7 rounded-lg text-sm font-bold',
                    idx < 3 ? 'bg-gradient-to-br from-orange-400 to-red-500 text-white' : 'bg-gray-100 text-gray-600'
                  ]"
                >
                  {{ idx + 1 }}
                </span>
              </td>
              
              <!-- 标题 -->
              <td class="px-4 py-4">
                <span class="text-gray-800 group-hover:text-orange-600 font-medium transition">
                  {{ topic.title }}
                </span>
                <span v-if="topic.summary" class="ml-2 text-xs text-gray-400 line-clamp-1 inline-block max-w-md">
                  {{ topic.summary }}
                </span>
              </td>
              
              <!-- 热度 -->
              <td class="px-4 py-4">
                <div class="flex items-center gap-2">
                  <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-gradient-to-r from-orange-400 to-red-500 rounded-full transition-all duration-500"
                      :style="{ width: getHotPercent(topic.hot_value) + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm text-gray-500 w-16 text-right">{{ formatHotValue(topic.hot_value) }}</span>
                </div>
              </td>
              
              <!-- 来源 -->
              <td class="px-4 py-4 text-right">
                <span class="inline-flex items-center gap-1 text-sm text-gray-500">
                  <span>{{ topic.platform_icon }}</span>
                  <span>{{ topic.platform_name }}</span>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 空状态 -->
        <div v-if="filteredTopics.length === 0" class="text-center py-16 text-gray-400">
          <span class="text-4xl mb-4 block">🔍</span>
          <p>暂无匹配的热点</p>
        </div>
      </div>
      
      <!-- 底部信息 -->
      <div class="mt-6 text-center text-sm text-gray-400">
        <p>🔥 知枢热榜 · 数据每30分钟更新一次</p>
      </div>
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
const platforms = ref<Platform[]>([])
const categories = ref<Category[]>([])
const searchQuery = ref('')
const selectedPlatform = ref<number | null>(null)
const selectedCategory = ref<number | null>(null)
const maxHot = ref(0)
const router = useRouter()

const formatHotValue = (value: number) => {
  if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
  if (value >= 1000) return (value / 1000).toFixed(0) + 'K'
  return value.toString()
}

const getHotPercent = (value: number) => {
  if (maxHot.value === 0) return 0
  return Math.round((value / maxHot.value) * 100)
}

const filteredTopics = computed(() => {
  let result = topics.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(t => 
      t.title.toLowerCase().includes(query) ||
      (t.summary && t.summary.toLowerCase().includes(query))
    )
  }
  
  return result
})

const filterTopics = () => {
  // 搜索触发
}

const selectPlatform = (platId: number | null) => {
  selectedPlatform.value = platId
  loadTopics()
}

const selectCategory = (catId: number | null) => {
  selectedCategory.value = catId
  loadTopics()
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
    
    // 计算最大热度
    if (topics.value.length > 0) {
      maxHot.value = Math.max(...topics.value.map(t => t.hot_value))
    }
  } catch (e) {
    console.error('Failed to load topics:', e)
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
  await Promise.all([loadTopics(), loadPlatforms(), loadCategories()])
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>