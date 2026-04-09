<template>
  <div class="home">
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
            知枢是一个智能体聚合平台，让你轻松发现和使用各类 AI 助手，同时实时追踪全网热点。
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
            <h3>智能体平台</h3>
            <p>发现、体验各类 AI 智能助手</p>
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
            <h3>知枢热榜</h3>
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

<style scoped>
/* 基础 */
.home {
  min-height: 100vh;
  background: #fafafa;
  position: relative;
}

.home::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 400px;
  background: linear-gradient(180deg, #f0f4ff 0%, #fafafa 100%);
  z-index: 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 头部 */
.header {
  background: #fff;
  border-bottom: 1px solid #eee;
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
  color: #1a1a1a;
}

.logo-mark {
  color: #4F46E5;
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
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.nav-links a:hover {
  color: #1a1a1a;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-text {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.btn-text:hover {
  color: #1a1a1a;
}

.btn-primary {
  padding: 8px 20px;
  background: #1a1a1a;
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary:hover {
  background: #333;
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
  color: #1a1a1a;
  margin: 0 0 16px;
  line-height: 1.2;
}

.highlight {
  color: #4F46E5;
}

.hero-desc {
  font-size: 16px;
  color: #666;
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
  background: #1a1a1a;
  color: #fff;
}

.btn-large.btn-outline {
  border: 1px solid #ddd;
  color: #666;
}

.btn-large.btn-outline:hover {
  border-color: #1a1a1a;
  color: #1a1a1a;
}

/* Visual Card */
.visual-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #eee;
  overflow: hidden;
}

.visual-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
}

.view-all {
  font-size: 13px;
  color: #4F46E5;
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
  background: #f5f5f5;
}

.item-icon {
  width: 44px;
  height: 44px;
  background: #f5f5f5;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-name {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.item-desc {
  font-size: 12px;
  color: #999;
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
  background: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s;
}

.product-card:hover {
  border-color: #ccc;
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
  color: #666;
  margin: 0;
}

.card-arrow {
  margin-top: 16px;
  color: #ccc;
}

/* Features */
.features {
  padding: 60px 0;
  background: #fff;
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
  color: #666;
  margin: 0;
}

/* Footer */
.footer {
  padding: 40px 0;
  border-top: 1px solid #eee;
  background: #fff;
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
  color: #666;
}

.footer-slogan {
  font-size: 13px;
  color: #999;
  margin: 0 0 8px;
}

.footer-copy {
  font-size: 12px;
  color: #bbb;
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