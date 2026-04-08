<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <p>页面不存在</p>
      <router-link to="/">返回首页</router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #F5F5F5; }
.not-found-content { text-align: center; }
.not-found-content h1 { font-size: 72px; color: #999; margin: 0; }
.not-found-content p { font-size: 18px; color: #666; margin: 16px 0 24px; }
.not-found-content a { display: inline-block; padding: 10px 24px; background: #1890FF; color: #FFF; border-radius: 6px; text-decoration: none; }
</style>