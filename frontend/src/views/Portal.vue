<template>
  <div class="home">
    <!-- 科技感背景 -->
    <div class="tech-bg">
      <div class="grid-lines"></div>
      <div class="particles">
        <div v-for="i in 20" :key="i" class="particle" :style="{ left: Math.random() * 100 + '%', animationDelay: Math.random() * 5 + 's' }"></div>
      </div>
      <div class="scan-line"></div>
    </div>
    
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <div class="nav">
          <a href="/" class="logo">
            <svg class="logo-mark" viewBox="0 0 32 32" width="28" height="28">
              <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/>
              <circle cx="16" cy="12" r="3" fill="currentColor"/>
              <circle cx="10" cy="20" r="2" fill="currentColor"/>
              <circle cx="22" cy="20" r="2" fill="currentColor"/>
              <path d="M12 15 Q16 17 20 15" fill="none" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            <span class="logo-text">知枢</span>
          </a>
          <div class="nav-links">
            <a href="#products">产品</a>
            <a href="#features">特性</a>
          </div>
          <div class="nav-actions">
            <button @click="toggleDark" class="dark-toggle" :title="isDark ? '切换亮色模式' : '切换暗黑模式'">
              <svg v-if="isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
              </svg>
            </button>
            <a href="/agents" class="btn-text">智能体</a>
            <a href="/tgmeng" class="btn-primary">热榜</a>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">
            发现智能
            <span class="highlight">新可能</span>
          </h1>
          <p class="hero-desc">
            知枢是知识聚合平台，匠人帮你对话各领域专家，看点帮你追踪全网热点。
          </p>
          <div class="hero-actions">
            <a href="/agents" class="btn-large btn-primary">
              开始探索
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </a>
            <a href="/tgmeng" class="btn-large btn-outline">浏览热榜</a>
          </div>
        </div>
        
        <div class="hero-visual">
          <div class="visual-card">
            <div class="visual-header">
              <div class="card-title">热门智能体</div>
              <a href="/agents" class="view-all">查看全部 →</a>
            </div>
            <div class="visual-list">
              <div class="visual-item">
                <div class="item-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#4F46E5" stroke-width="2">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                    <circle cx="9" cy="9" r="1" fill="#4F46E5"/>
                    <circle cx="15" cy="9" r="1" fill="#4F46E5"/>
                  </svg>
                </div>
                <div class="item-info">
                  <div class="item-name">写作助手</div>
                  <div class="item-desc">智能创作，文案生成</div>
                </div>
              </div>
              <div class="visual-item">
                <div class="item-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#059669" stroke-width="2">
                    <polyline points="16 18 22 12 16 6"/>
                    <polyline points="8 6 2 12 8 18"/>
                  </svg>
                </div>
                <div class="item-info">
                  <div class="item-name">编程助手</div>
                  <div class="item-desc">代码生成与优化</div>
                </div>
              </div>
              <div class="visual-item">
                <div class="item-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#DC2626" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="2" y1="12" x2="22" y2="12"/>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                  </svg>
                </div>
                <div class="item-info">
                  <div class="item-name">翻译助手</div>
                  <div class="item-desc">多语言精准翻译</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 产品 -->
    <section id="products" class="products">
      <div class="container">
        <h2 class="section-title">我们的产品</h2>
        <div class="products-grid">
          <a href="/agents" class="product-card">
            <div class="product-icon">
              <svg viewBox="0 0 48 48" width="48" height="48" fill="none">
                <rect x="6" y="6" width="36" height="36" rx="8" fill="#EEF2FF"/>
                <circle cx="24" cy="20" r="6" stroke="#4F46E5" stroke-width="2"/>
                <path d="M14 34c0-4 4-7 10-7s10 3 10 7" stroke="#4F46E5" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <h3>知枢·匠人 🛠️</h3>
            <p>发现、对话各领域知识达人</p>
            <div class="card-arrow">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7 5L12 10L7 15" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </div>
          </a>
          <a href="/tgmeng" class="product-card">
            <div class="product-icon">
              <svg viewBox="0 0 48 48" width="48" height="48" fill="none">
                <rect x="6" y="6" width="36" height="36" rx="8" fill="#FEF3C7"/>
                <path d="M24 14v10l6 4" stroke="#D97706" stroke-width="2" stroke-linecap="round"/>
                <circle cx="24" cy="24" r="14" stroke="#D97706" stroke-width="2"/>
              </svg>
            </div>
            <h3>知枢·看点</h3>
            <p>实时聚合全网热点资讯</p>
            <div class="card-arrow">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7 5L12 10L7 15" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- 特性 -->
    <section id="features" class="features">
      <div class="container">
        <h2 class="section-title">为什么选择知枢</h2>
        <div class="features-grid">
          <div class="feature">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#4F46E5" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <h3>实时更新</h3>
            <p>热榜每分钟自动刷新</p>
          </div>
          <div class="feature">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#4F46E5" stroke-width="2">
                <rect x="3" y="3" width="7" height="7" rx="1"/>
                <rect x="14" y="3" width="7" height="7" rx="1"/>
                <rect x="3" y="14" width="7" height="7" rx="1"/>
                <rect x="14" y="14" width="7" height="7" rx="1"/>
              </svg>
            </div>
            <h3>多源聚合</h3>
            <p>45+ 平台数据整合</p>
          </div>
          <div class="feature">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#4F46E5" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <h3>智能对话</h3>
            <p>与 AI 助手实时交流</p>
          </div>
          <div class="feature">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#4F46E5" stroke-width="2">
                <rect x="5" y="2" width="14" height="20" rx="2"/>
                <line x1="12" y1="18" x2="12" y2="18"/>
              </svg>
            </div>
            <h3>多端适配</h3>
            <p>手机、平板、电脑都能用</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <svg class="logo-mark" viewBox="0 0 32 32" width="20" height="20">
              <circle cx="16" cy="16" r="14" fill="none" stroke="#999" stroke-width="1.5"/>
              <circle cx="16" cy="12" r="2.5" fill="#999"/>
              <circle cx="10" cy="20" r="1.5" fill="#999"/>
              <circle cx="22" cy="20" r="1.5" fill="#999"/>
            </svg>
            <span>知枢</span>
          </div>
          <p class="footer-slogan">让智能触手可及</p>
          <p class="footer-copy">© 2026 知枢</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// 暗黑模式
const isDark = ref(false)

// 函数定义必须在使用前
const updateTheme = () => {
  localStorage.setItem('darkMode', isDark.value)
  document.documentElement.classList.toggle('dark', isDark.value)
}

const toggleDark = () => {
  isDark.value = !isDark.value
}

onMounted(() => {
  const saved = localStorage.getItem('darkMode')
  if (saved) {
    isDark.value = saved === 'true'
  } else {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  updateTheme()
})

watch(isDark, updateTheme)
</script>

<style scoped>
/* 科技感背景 */
.tech-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.grid-lines {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(var(--primary) 1px, transparent 1px),
    linear-gradient(90deg, var(--primary) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.05;
  animation: grid-move 20s linear infinite;
}

@keyframes grid-move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.particles {
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--primary);
  border-radius: 50%;
  opacity: 0.6;
  animation: float-up 8s ease-in-out infinite;
  box-shadow: 0 0 10px var(--primary), 0 0 20px var(--primary);
}

@keyframes float-up {
  0%, 100% { 
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100px) scale(1);
    opacity: 0;
  }
}

.scan-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%,
    var(--primary) 50%,
    transparent 100%
  );
  opacity: 0.3;
  animation: scan 4s linear infinite;
  box-shadow: 0 0 15px var(--primary);
}

@keyframes scan {
  0% { top: -2px; }
  100% { top: 100%; }
}

/* 基础 */
.home {
  min-height: 100vh;
  background: var(--bg);
  position: relative;
  color: var(--text);
}

.home::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 400px;
  background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg) 100%);
  z-index: 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 头部 */
.header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text);
}

.logo-mark {
  color: var(--primary);
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 32px;
}

.nav-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
}

.nav-links a:hover {
  color: var(--text);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.dark-toggle {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: background 0.2s;
}

.dark-toggle:hover {
  background: var(--border);
}

.dark-toggle svg {
  width: 18px;
  height: 18px;
}

.btn-text {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
}

.btn-text:hover {
  color: var(--text);
}

.btn-primary {
  padding: 8px 20px;
  background: var(--text);
  color: var(--bg-card);
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary:hover {
  background: var(--primary);
}

/* Hero */
.hero {
  padding: 60px 0;
  position: relative;
  z-index: 1;
}

.hero .container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}

.hero-title {
  font-size: 42px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 16px;
  line-height: 1.2;
  position: relative;
}

.hero-title::after {
  content: ''; 
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), transparent);
  border-radius: 2px;
}

.highlight {
  color: var(--primary);
  text-shadow: 0 0 20px rgba(79, 70, 229, 0.5);
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from { text-shadow: 0 0 20px rgba(79, 70, 229, 0.5); }
  to { text-shadow: 0 0 30px rgba(79, 70, 229, 0.8), 0 0 40px rgba(79, 70, 229, 0.4); }
}

.hero-desc {
  font-size: 16px;
  color: var(--text-muted);
  line-height: 1.6;
  margin: 0 0 28px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.btn-large {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.btn-large.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, #6366f1 100%);
  color: #fff;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
}

.btn-large.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.btn-large.btn-primary:hover::before {
  left: 100%;
}

.btn-large.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
}

.btn-large.btn-outline {
  border: 1px solid var(--border);
  color: var(--text-muted);
}

.btn-large.btn-outline:hover {
  border-color: var(--text);
  color: var(--text);
}

/* Visual Card */
.visual-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  position: relative;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.1);
}

.visual-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 40%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 60%
  );
  animation: shine 3s linear infinite;
}

@keyframes shine {
  0% { transform: translateX(-100%) translateY(-100%); }
  100% { transform: translateX(100%) translateY(100%); }
}

.visual-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}

.view-all {
  font-size: 13px;
  color: var(--primary);
  text-decoration: none;
}

.visual-list {
  padding: 8px;
}

.visual-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
}

.visual-item:hover {
  background: var(--border);
}

.item-icon {
  width: 44px;
  height: 44px;
  background: var(--border);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 2px;
}

.item-desc {
  font-size: 12px;
  color: var(--text-muted);
}

/* Products */
.products {
  padding: 60px 0;
  position: relative;
  z-index: 1;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  text-align: center;
  margin: 0 0 40px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.product-card {
  display: block;
  padding: 28px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.product-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent, rgba(255,255,255,0.1));
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: xor;
  -webkit-mask-composite: xor;
  pointer-events: none;
}

.product-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary);
  box-shadow: 0 10px 40px rgba(79, 70, 229, 0.3), 0 0 20px rgba(79, 70, 229, 0.2);
}

.product-card:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(79, 70, 229, 0.1), transparent);
  animation: card-shine 0.5s ease;
}

@keyframes card-shine {
  0% { left: -100%; }
  100% { left: 100%; }
}

.product-icon {
  margin-bottom: 16px;
}

.product-card h3 {
  font-size: 17px;
  margin: 0 0 8px;
}

.product-card p {
  font-size: 14px;
  color: var(--text-muted);
  margin: 0;
}

.card-arrow {
  margin-top: 16px;
  color: var(--text-muted);
}

/* Features */
.features {
  padding: 60px 0;
  background: var(--bg-card);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.feature {
  text-align: center;
}

.feature-icon {
  width: 56px;
  height: 56px;
  background: #F5F3FF;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}

.feature h3 {
  font-size: 15px;
  margin: 0 0 6px;
}

.feature p {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
}

/* Footer */
.footer {
  padding: 40px 0;
  border-top: 1px solid var(--border);
  background: var(--bg-card);
  position: relative;
  z-index: 1;
}

.footer-content {
  text-align: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 8px;
}

.footer-brand span {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-muted);
}

.footer-slogan {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0 0 8px;
}

.footer-copy {
  font-size: 12px;
  color: var(--text-muted);
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links { display: none; }
  
  .hero .container {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-title { font-size: 32px; }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-visual { display: none; }
  
  .products-grid { grid-template-columns: 1fr; }
  
  .features-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>