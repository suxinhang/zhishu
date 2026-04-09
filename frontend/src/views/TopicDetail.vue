<template>
  <div class="topic-detail">
    <header class="header">
      <div class="header-inner">
        <a href="/tgmeng" class="logo">
          <span class="logo-icon">🍭</span>
          <span class="logo-text">糖果梦热榜</span>
        </a>
      </div>
    </header>
    <main class="main">
      <div class="container">
        <h1>热点详情</h1>
      </div>
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.topic-detail { min-height: 100vh; background: #f5f5f5; }
.header { background: #fff; border-bottom: 1px solid #eee; }
.header-inner { max-width: 1000px; margin: 0 auto; padding: 0 20px; height: 50px; display: flex; align-items: center; }
.logo { display: flex; align-items: center; gap: 6px; text-decoration: none; color: #333; }
.logo-icon { font-size: 20px; }
.logo-text { font-size: 16px; font-weight: 600; }
.main { padding: 20px; }
.container { max-width: 1000px; margin: 0 auto; }
h1 { font-size: 20px; }
</style>