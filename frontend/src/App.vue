<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3">
          <span class="text-2xl">🔥</span>
          <div>
            <span class="text-xl font-bold text-gray-800">知枢热榜</span>
            <span class="text-xs text-gray-400 ml-2 hidden sm:inline">全网热点聚合</span>
          </div>
        </router-link>
        
        <!-- 导航链接 -->
        <div class="flex items-center gap-6">
          <router-link 
            to="/" 
            class="text-sm text-gray-600 hover:text-gray-800 transition"
            :class="{ 'text-gray-800 font-medium': $route.path === '/' }"
          >
            首页
          </router-link>
          <router-link 
            to="/category" 
            class="text-sm text-gray-600 hover:text-gray-800 transition"
            :class="{ 'text-gray-800 font-medium': $route.path === '/category' }"
          >
            分类
          </router-link>
          <router-link 
            to="/about" 
            class="text-sm text-gray-600 hover:text-gray-800 transition"
            :class="{ 'text-gray-800 font-medium': $route.path === '/about' }"
          >
            关于
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <router-view />
    
    <!-- 页脚 -->
    <footer class="py-8 text-center text-gray-400 text-sm border-t border-gray-200 bg-white mt-12">
      <p>🔥 知枢热榜 · 全网热点，一角尽览</p>
      <p class="mt-2 text-xs text-gray-300">© 2026 zhishu.ai</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
</script>