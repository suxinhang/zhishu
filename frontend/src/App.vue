<template>
  <div class="min-h-screen network-bg">
    <!-- 导航栏 -->
    <nav class="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-200/50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-zhishu-800 to-zhishu-600 flex items-center justify-center shadow-lg">
            <span class="text-xl">🧠</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xl font-bold gradient-text">知枢</span>
            <span class="text-xs text-slate-400 hidden sm:inline">智能体平台</span>
          </div>
        </div>
        
        <!-- 导航链接 -->
        <div class="flex gap-1">
          <router-link 
            to="/" 
            class="px-4 py-2 rounded-lg text-slate-600 hover:text-zhishu-600 hover:bg-zhishu-50 transition-all duration-200"
            :class="{ 'bg-zhishu-50 text-zhishu-600 font-medium': $route.path === '/' }"
          >
            发现
          </router-link>
          <router-link 
            to="/category" 
            class="px-4 py-2 rounded-lg text-slate-600 hover:text-zhishu-600 hover:bg-zhishu-50 transition-all duration-200"
            :class="{ 'bg-zhishu-50 text-zhishu-600 font-medium': $route.path === '/category' }"
          >
            分类
          </router-link>
          <router-link 
            to="/about" 
            class="px-4 py-2 rounded-lg text-slate-600 hover:text-zhishu-600 hover:bg-zhishu-50 transition-all duration-200"
            :class="{ 'bg-zhishu-50 text-zhishu-600 font-medium': $route.path === '/about' }"
          >
            关于
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <router-view />
    
    <!-- 页脚 -->
    <footer class="mt-12 py-8 text-center text-slate-400 text-sm border-t border-slate-200/50 bg-white/30">
      <div class="flex items-center justify-center gap-2">
        <span class="text-lg">🧠</span>
        <span>知枢 · 让智能触手可及</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
</script>