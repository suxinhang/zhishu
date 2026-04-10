<template>
  <div class="max-w-7xl mx-auto px-6 py-8">
    <!-- 页面标题 -->
    <div class="text-center mb-12 animate-fade-in">
      <div class="flex items-center justify-center gap-2 mb-4">
        <span class="text-3xl">🏷️</span>
        <h1 class="text-3xl font-bold gradient-text">匠人分类</h1>
      </div>
      <p class="text-slate-500">按场景选择最适合你的匠人</p>
    </div>
    
    <!-- 分类网格 -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div 
        v-for="cat in categories" 
        :key="cat.id"
        class="bg-white rounded-xl shadow-card card-glow text-center cursor-pointer overflow-hidden animate-fade-in"
        @click="goCategory(cat.id)"
      >
        <!-- 顶部装饰线 -->
        <div class="h-1 bg-gradient-to-r from-zhishu-600 via-amber-400 to-zhishu-600 opacity-30"></div>
        
        <!-- 图标区域 -->
        <div class="py-8">
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-zhishu-100 to-zhishu-50 flex items-center justify-center text-4xl mx-auto shadow-inner mb-4">
            {{ cat.icon }}
          </div>
          <h3 class="text-lg font-semibold text-slate-800">{{ cat.name }}</h3>
          <p class="text-sm text-slate-500 mt-2 flex items-center justify-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            {{ getAgentCount(cat.id) }} 位匠人
          </p>
        </div>
        
        <!-- 查看按钮 -->
        <div class="px-4 pb-4">
          <button class="w-full py-2.5 btn-secondary text-sm flex items-center justify-center gap-1">
            <span>浏览</span>
            <span>→</span>
          </button>
        </div>
        
        <!-- 底部装饰 -->
        <div class="flex justify-center gap-2 py-2 opacity-40">
          <div class="w-2 h-2 rounded-full bg-zhishu-300"></div>
          <div class="w-2 h-2 rounded-full bg-amber-300"></div>
          <div class="w-2 h-2 rounded-full bg-zhishu-300"></div>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-if="categories.length === 0" class="text-center py-16">
      <div class="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mx-auto mb-4">
        🏷️
      </div>
      <p class="text-slate-400">暂无分类</p>
    </div>
    
    <!-- 统计信息 -->
    <div class="mt-12 p-6 bg-white/50 rounded-xl border border-slate-200/50">
      <div class="flex items-center justify-around text-center">
        <div>
          <p class="text-3xl font-bold text-zhishu-600">{{ categories.length }}</p>
          <p class="text-sm text-slate-500 mt-1">分类总数</p>
        </div>
        <div class="w-px h-12 bg-slate-200"></div>
        <div>
          <p class="text-3xl font-bold text-amber-500">{{ agents.length }}</p>
          <p class="text-sm text-slate-500 mt-1">匠人总数</p>
        </div>
        <div class="w-px h-12 bg-slate-200"></div>
        <div>
          <p class="text-3xl font-bold text-slate-700">{{ onlineCount }}</p>
          <p class="text-sm text-slate-500 mt-1">在线可用</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Category {
  id: number
  name: string
  icon: string
}

interface Agent {
  id: number
  category_id: number
}

const categories = ref<Category[]>([])
const agents = ref<Agent[]>([])
const router = useRouter()

const getAgentCount = (catId: number) => {
  return agents.value.filter(a => a.category_id === catId).length
}

const onlineCount = computed(() => {
  // 假设所有智能体都在线
  return agents.value.length
})

const goCategory = (catId: number) => {
  router.push({ path: '/', query: { category: catId } })
}

onMounted(async () => {
  try {
    const [catsRes, agentsRes] = await Promise.all([
      fetch('/api/categories').then(r => r.json()),
      fetch('/api/agents').then(r => r.json())
    ])
    categories.value = catsRes
    agents.value = agentsRes
  } catch (e) {
    console.error('Failed to load data:', e)
  }
})
</script>