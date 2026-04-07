<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-2xl">🧠</span>
          <span class="text-xl font-bold text-gray-800">知枢</span>
        </div>
        <div class="flex gap-6 text-gray-600">
          <router-link to="/" class="hover:text-blue-600 transition">首页</router-link>
          <router-link to="/category" class="hover:text-blue-600 transition">分类</router-link>
          <router-link to="/about" class="hover:text-blue-600 transition">关于</router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script>