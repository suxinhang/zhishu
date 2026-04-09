<template>
  <div class="home">
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <div class="nav">
          <div class="logo">
            <img src="/logo.svg" alt="知枢" height="32" />
          </div>
          <div class="nav-links">
            <a href="#products">产品</a>
            <a href="#features">特性</a>
            <a href="#about">关于</a>
          </div>
          <div class="nav-actions">
            <a href="/agents" class="btn-outline">智能体</a>
            <a href="/tgmeng" class="btn-primary">热榜</a>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero 区域 -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <div class="hero-badge">让智能触手可及</div>
          <h1 class="hero-title">
            知枢
            <span class="gradient-text">智能体聚合平台</span>
          </h1>
          <p class="hero-desc">
            发现、体验各类 AI 智能助手，实时追踪全网热点
          </p>
          <div class="hero-actions">
            <a href="/agents" class="btn-large btn-primary">
              <span>🤖</span> 探索智能体
            </a>
            <a href="/tgmeng" class="btn-large btn-outline">
              <span>🔥</span> 查看热榜
            </a>
          </div>
          <div class="hero-stats">
            <div class="stat">
              <div class="stat-num">45+</div>
              <div class="stat-label">数据源</div>
            </div>
            <div class="stat">
              <div class="stat-num">实时</div>
              <div class="stat-label">热榜更新</div>
            </div>
            <div class="stat">
              <div class="stat-num">AI</div>
              <div class="stat-label">智能对话</div>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="visual-card">
            <div class="visual-header">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
            </div>
            <div class="visual-content">
              <div class="code-line"><span class="keyword">const</span> 知枢 = {</div>
              <div class="code-line indent"><span class="string">智能体</span>: <span class="number">∞</span>,</div>
              <div class="code-line indent"><span class="string">热榜</span>: <span class="string">'实时'</span>,</div>
              <div class="code-line indent"><span class="string">AI</span>: <span class="keyword">true</span></div>
              <div class="code-line">}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 产品区域 -->
    <section id="products" class="products">
      <div class="container">
        <h2 class="section-title">我们的产品</h2>
        <div class="products-grid">
          <a href="/agents" class="product-card">
            <div class="product-icon">🤖</div>
            <h3>智能体平台</h3>
            <p>发现、体验各类 AI 智能助手，覆盖陪伴、写作、编程、翻译等场景</p>
            <span class="product-arrow">→</span>
          </a>
          <a href="/tgmeng" class="product-card">
            <div class="product-icon">🔥</div>
            <h3>全网热榜</h3>
            <p>实时聚合微博、知乎、抖音等 45+ 平台热点，AI 深度洞察</p>
            <span class="product-arrow">→</span>
          </a>
        </div>
      </div>
    </section>

    <!-- 特性区域 -->
    <section id="features" class="features">
      <div class="container">
        <h2 class="section-title">为什么选择知枢</h2>
        <div class="features-grid">
          <div class="feature">
            <div class="feature-icon">⚡</div>
            <h3>实时更新</h3>
            <p>热榜每分钟自动更新，智能体随时待命</p>
          </div>
          <div class="feature">
            <div class="feature-icon">🎯</div>
            <h3>精准聚合</h3>
            <p>45+ 平台数据源，多维度分类筛选</p>
          </div>
          <div class="feature">
            <div class="feature-icon">🧠</div>
            <h3>AI 增强</h3>
            <p>智能对话、深度分析、趋势预测</p>
          </div>
          <div class="feature">
            <div class="feature-icon">📱</div>
            <h3>多端适配</h3>
            <p>响应式设计，手机、平板、PC 都好用</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <img src="/logo.svg" alt="知枢" height="24" />
            <p>让智能触手可及</p>
          </div>
          <div class="footer-links">
            <a href="/agents">智能体</a>
            <a href="/tgmeng">热榜</a>
            <a href="#features">特性</a>
          </div>
          <div class="footer-copyright">
            © 2026 知枢 · Powered by Vue + FastAPI
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* 全局 */
.home {
  min-height: 100vh;
  background: #fafafa;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 头部 */
.header {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
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
  color: #333;
}

.nav-actions {
  display: flex;
  gap: 12px;
}

.btn-outline {
  padding: 8px 20px;
  border: 1px solid #ddd;
  border-radius: 6px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.btn-outline:hover {
  border-color: #667eea;
  color: #667eea;
}

.btn-primary {
  padding: 8px 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary:hover {
  opacity: 0.9;
}

/* Hero */
.hero {
  padding: 80px 0;
}

.hero .container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-badge {
  display: inline-block;
  padding: 6px 16px;
  background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
  color: #667eea;
  border-radius: 20px;
  font-size: 13px;
  margin-bottom: 20px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 20px;
  line-height: 1.2;
}

.gradient-text {
  display: block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-desc {
  font-size: 18px;
  color: #666;
  margin: 0 0 32px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
}

.btn-large {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
}

.hero-stats {
  display: flex;
  gap: 48px;
}

.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

/* Visual */
.visual-card {
  background: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.visual-header {
  padding: 12px 16px;
  background: #2a2a2a;
  display: flex;
  gap: 8px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27ca40; }

.visual-content {
  padding: 24px;
  font-family: 'SF Mono', Monaco, monospace;
  font-size: 14px;
  line-height: 1.8;
  color: #e0e0e0;
}

.code-line {}
.indent { padding-left: 24px; }
.keyword { color: #c792ea; }
.string { color: #c3e88d; }
.number { color: #f78c6c; }

/* Products */
.products {
  padding: 80px 0;
}

.section-title {
  font-size: 32px;
  font-weight: 600;
  text-align: center;
  margin: 0 0 48px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.product-card {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  text-decoration: none;
  color: inherit;
  border: 1px solid #eee;
  transition: all 0.3s;
}

.product-card:hover {
  border-color: #667eea;
  box-shadow: 0 8px 30px rgba(102,126,234,0.1);
}

.product-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.product-card h3 {
  font-size: 20px;
  margin: 0 0 12px;
}

.product-card p {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

.product-arrow {
  display: inline-block;
  margin-top: 16px;
  color: #667eea;
  font-size: 18px;
}

/* Features */
.features {
  padding: 80px 0;
  background: #fff;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}

.feature {
  text-align: center;
}

.feature-icon {
  font-size: 32px;
  margin-bottom: 16px;
}

.feature h3 {
  font-size: 16px;
  margin: 0 0 8px;
}

.feature p {
  font-size: 13px;
  color: #666;
  margin: 0;
}

/* Footer */
.footer {
  padding: 48px 0;
  border-top: 1px solid #eee;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-brand p {
  font-size: 12px;
  color: #999;
  margin: 8px 0 0;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-links a {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.footer-links a:hover {
  color: #333;
}

.footer-copyright {
  font-size: 12px;
  color: #bbb;
}

/* 响应式 */
@media (max-width: 768px) {
  .nav-links { display: none; }
  
  .hero .container {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-title { font-size: 36px; }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .hero-visual { display: none; }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .footer-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
  }
}
</style>