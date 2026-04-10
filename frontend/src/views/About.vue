<template>
  <div class="max-w-4xl mx-auto px-6 py-12">
    <div class="animate-fade-in">
      <!-- Hero -->
      <div class="text-center mb-12">
        <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-zhishu-800 to-zhishu-600 flex items-center justify-center text-5xl mx-auto mb-6 shadow-lg">
          🧠
        </div>
        <h1 class="text-4xl font-bold gradient-text mb-2">知枢</h1>
        <p class="text-xl text-slate-600">让智能触手可及</p>
      </div>
      
      <!-- 介绍卡片 -->
      <div class="bg-white rounded-2xl shadow-card overflow-hidden mb-8">
        <div class="h-2 bg-gradient-to-r from-zhishu-600 via-amber-400 to-zhishu-600"></div>
        
        <div class="p-8">
          <h2 class="text-2xl font-semibold text-slate-800 mb-6 flex items-center gap-2">
            <span>💡</span> 关于我们
          </h2>
          
          <p class="text-slate-600 leading-relaxed mb-6">
            知枢是知识聚合平台，识客帮你对话各领域达人，看点帮你追踪全网热点。
            我们相信，AI 不应该只是技术专家的工具，而应该成为每个人日常生活的一部分。
          </p>
          
          <p class="text-slate-600 leading-relaxed">
            在这里，你可以找到陪伴聊天、创意写作、语言翻译、艺术创作、代码编程等各种领域的识客达人。
            即开即用，无需注册，让智能真正触手可及。
          </p>
        </div>
      </div>
      
      <!-- 特点展示 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-card p-6 text-center">
          <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center text-2xl mx-auto mb-4 shadow-inner">
            ⚡
          </div>
          <h3 class="font-semibold text-slate-800 mb-2">即开即用</h3>
          <p class="text-sm text-slate-500">无需注册，直接对话</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-card p-6 text-center">
          <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-amber-50 to-amber-100 flex items-center justify-center text-2xl mx-auto mb-4 shadow-inner">
            🎯
          </div>
          <h3 class="font-semibold text-slate-800 mb-2">精准推荐</h3>
          <p class="text-sm text-slate-500">智能匹配最适合的助手</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-card p-6 text-center">
          <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-green-50 to-green-100 flex items-center justify-center text-2xl mx-auto mb-4 shadow-inner">
            🌐
          </div>
          <h3 class="font-semibold text-slate-800 mb-2">全场景覆盖</h3>
          <p class="text-sm text-slate-500">陪伴、创作、办公、学习</p>
        </div>
      </div>
      
      <!-- 技术栈 -->
      <div class="bg-white/50 rounded-xl border border-slate-200/50 p-6">
        <h3 class="font-semibold text-slate-800 mb-4 flex items-center gap-2">
          <span>🔧</span> 技术栈
        </h3>
        <div class="flex flex-wrap gap-3">
          <span class="px-3 py-1.5 bg-white rounded-lg text-slate-600 text-sm border border-slate-200">Vue 3</span>
          <span class="px-3 py-1.5 bg-white rounded-lg text-slate-600 text-sm border border-slate-200">Vite</span>
          <span class="px-3 py-1.5 bg-white rounded-lg text-slate-600 text-sm border border-slate-200">Tailwind CSS</span>
          <span class="px-3 py-1.5 bg-white rounded-lg text-slate-600 text-sm border border-slate-200">FastAPI</span>
          <span class="px-3 py-1.5 bg-white rounded-lg text-slate-600 text-sm border border-slate-200">SQLite</span>
        </div>
      </div>
      
      <!-- 版本信息 -->
      <div class="mt-8 text-center text-sm text-slate-400">
        <p>© 2026 知枢 · v2.0</p>
        <p class="mt-1">Made with 💙 by 知枢团队</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>