<template>
  <div class="portal">
    <div class="portal-main">
      <h1 class="title">知枢</h1>
      <p class="subtitle">智能体聚合平台</p>
      
      <div class="links">
        <a href="/agents" class="link">
          <span class="link-icon">🧠</span>
          <span class="link-title">智能体</span>
          <span class="link-desc">AI 助手聚合</span>
        </a>
        <a href="/tgmeng" class="link">
          <span class="link-icon">🍭</span>
          <span class="link-title">热榜</span>
          <span class="link-desc">全网热点聚合</span>
        </a>
      </div>
    </div>
    
    <footer class="portal-footer">
      <p>知枢 · 让智能触手可及</p>
    </footer>
  </div>
</template>

<style>
.portal {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}
.portal-main {
  text-align: center;
}
.title {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px;
}
.subtitle {
  font-size: 14px;
  color: #999;
  margin: 0 0 32px;
}
.links {
  display: flex;
  gap: 16px;
}
.link {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 32px;
  background: #fff;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.link:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.link-icon {
  font-size: 32px;
  margin-bottom: 8px;
}
.link-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}
.link-desc {
  font-size: 12px;
  color: #999;
}
.portal-footer {
  margin-top: 48px;
  font-size: 12px;
  color: #bbb;
}
@media (max-width: 480px) {
  .links { flex-direction: column; }
  .link { padding: 20px 48px; }
}
</style>