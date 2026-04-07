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
          />
          <button 
            @click="searchAgents"
            class="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition"
          >
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 分类筛选 -->
    <div class="flex flex-wrap gap-2 justify-center mb-8">
      <button 
        v-for="cat in categories" 
        :key="cat.id"
        @click="selectCategory(cat.id)"
        :class="[
          'px-4 py-2 rounded-full transition',
          selectedCategory === cat.id 
            ? 'bg-blue-600 text-white' 
            : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
        ]"
      >
        {{ cat.icon }} {{ cat.name }}
      </button>
    </div>

    <!-- 智能体卡片列表 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <AgentCard 
        v-for="agent in filteredAgents" 
        :key="agent.id"
        :agent="agent"
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

interface Agent {
  id: number
  name: string
  icon: string
  description: string
  category: string
}

interface Category {
  id: number
  name: string
  icon: string
}

const agents = ref<Agent[]>([])
const categories = ref<Category[]>([])
const searchQuery = ref('')
const selectedCategory = ref<number | null>(null)

const filteredAgents = computed(() => {
  let result = agents.value
  
  if (selectedCategory.value) {
    result = result.filter(a => a.category_id === selectedCategory.value)
  }
  
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
  selectedCategory.value = selectedCategory.value === catId ? null : catId
}

const searchAgents = () => {
  // 搜索已通过 filteredAgents 自动处理
}

onMounted(async () => {
  try {
    const [agentsRes, catsRes] = await Promise.all([
      fetch('/api/agents').then(r => r.json()),
      fetch('/api/categories').then(r => r.json())
    ])
    agents.value = agentsRes
    categories.value = catsRes
  } catch (e) {
    console.error('Failed to load data:', e)
  }
})
</script>