<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">分类</h1>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div 
        v-for="cat in categories" 
        :key="cat.id"
        class="bg-white rounded-xl shadow-md p-6 text-center hover:shadow-lg transition cursor-pointer"
        @click="goCategory(cat.id)"
      >
        <div class="text-4xl mb-2">{{ cat.icon }}</div>
        <h3 class="text-lg font-semibold text-gray-800">{{ cat.name }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ getAgentCount(cat.id) }} 个智能体</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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