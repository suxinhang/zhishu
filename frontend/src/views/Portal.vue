<template>
  <div class="portal-page">
    <div class="portal-bg"></div>
    
    <div class="portal-content">
      <div class="portal-header">
        <h1 class="portal-title">
          <span class="portal-emoji">🧠</span>
          <span>知枢</span>
        </h1>
        <p class="portal-subtitle">智能体聚合平台 · 让智能触手可及</p>
      </div>

      <div class="portal-cards">
        <!-- 知枢智能体 -->
        <router-link to="/agents" class="portal-card card-zhishu">
          <div class="card-icon">🧠</div>
          <h2 class="card-title">知枢智能体</h2>
          <p class="card-desc">发现、体验各类 AI 智能助手</p>
          <div class="card-tags">
            <span class="tag">陪伴</span>
            <span class="tag">写作</span>
            <span class="tag">编程</span>
            <span class="tag">翻译</span>
          </div>
          <div class="card-arrow">→</div>
        </router-link>

        <!-- 糖果梦热榜 -->
        <router-link to="/tgmeng" class="portal-card card-tgmeng">
          <div class="card-icon">🍭</div>
          <h2 class="card-title">糖果梦热榜</h2>
          <p class="card-desc">全网实时热榜聚合 · AI 深度洞察</p>
          <div class="card-tags">
            <span class="tag">微博</span>
            <span class="tag">知乎</span>
            <span class="tag">抖音</span>
            <span class="tag">V2EX</span>
          </div>
          <div class="card-arrow">→</div>
        </router-link>
      </div>

      <div class="portal-footer">
        <p>科技不该冰冷，人性不该傲慢</p>
        <p class="portal-copyright">© 2026 知枢 · Powered by Vue + FastAPI</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.portal-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.portal-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  z-index: 0;
}

.portal-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
}

.portal-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 900px;
  padding: 40px 20px;
}

.portal-header {
  text-align: center;
  margin-bottom: 48px;
}

.portal-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 48px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 12px 0;
  text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}

.portal-emoji {
  font-size: 56px;
}

.portal-subtitle {
  font-size: 18px;
  color: rgba(255,255,255,0.9);
  margin: 0;
}

.portal-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.portal-card {
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 32px;
  text-decoration: none;
  color: inherit;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.portal-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.card-title {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 8px 0;
}

.card-desc {
  font-size: 14px;
  color: #666;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  padding: 4px 12px;
  background: #F5F5F5;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.card-arrow {
  position: absolute;
  right: 24px;
  bottom: 24px;
  font-size: 24px;
  color: #CCC;
  transition: all 0.3s;
}

.portal-card:hover .card-arrow {
  color: #1890FF;
  transform: translateX(4px);
}

.card-zhishu:hover {
  border: 2px solid #667eea;
}

.card-tgmeng:hover {
  border: 2px solid #FF6B6B;
}

.portal-footer {
  text-align: center;
  color: rgba(255,255,255,0.8);
  font-size: 14px;
}

.portal-footer p {
  margin: 4px 0;
}

.portal-copyright {
  font-size: 12px;
  opacity: 0.7;
}

/* 响应式 */
@media (max-width: 768px) {
  .portal-title {
    font-size: 36px;
  }
  
  .portal-emoji {
    font-size: 42px;
  }
  
  .portal-subtitle {
    font-size: 14px;
  }
  
  .portal-card {
    padding: 24px;
  }
  
  .card-icon {
    font-size: 36px;
  }
  
  .card-title {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .portal-content {
    padding: 24px 16px;
  }
  
  .portal-header {
    margin-bottom: 32px;
  }
  
  .portal-cards {
    gap: 16px;
  }
}
</style>