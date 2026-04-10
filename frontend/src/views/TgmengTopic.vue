<template>
  <div class="tgmeng-app">
    <header class="tgmeng-header">
      <div class="tgmeng-container">
        <div class="tgmeng-header-inner">
          <router-link to="/tgmeng" class="tgmeng-logo">
            <span class="tgmeng-logo-icon">🍭</span>
            <span class="logo-text">知枢热榜</span>
          </router-link>
          <div class="tgmeng-back">
            <router-link to="/tgmeng">← 返回首页</router-link>
          </div>
        </div>
      </div>
    </header>

    <main class="tgmeng-main">
      <div class="tgmeng-container">
        <div v-if="topic" class="tgmeng-topic-detail">
          <div class="tgmeng-topic-header">
            <div class="tgmeng-topic-rank">TOP {{ rank }}</div>
            <h1 class="tgmeng-topic-title">{{ topic.title }}</h1>
            <div class="tgmeng-topic-meta">
              <span class="tgmeng-source">{{ topic.source }}</span>
              <span class="tgmeng-category">{{ topic.category }}</span>
            </div>
          </div>
          
          <div class="tgmeng-topic-stats">
            <div class="tgmeng-stat-item">
              <div class="tgmeng-stat-value">{{ topic.sugar_index }}</div>
              <div class="tgmeng-stat-label">糖果指数</div>
            </div>
            <div class="tgmeng-stat-item">
              <div class="tgmeng-stat-value">{{ formatNumber(topic.view_count) }}</div>
              <div class="tgmeng-stat-label">浏览量</div>
            </div>
            <div class="tgmeng-stat-item">
              <div class="tgmeng-stat-value">{{ topic.comment_count }}</div>
              <div class="tgmeng-stat-label">评论数</div>
            </div>
          </div>
          
          <!-- AI 解读卡片 -->
          <div class="ai-interpretation">
            <div class="ai-header">
              <span class="ai-icon">🤖</span>
              <span class="ai-title">AI 解读</span>
              <button @click="loadInterpretation" :disabled="loadingInterpret" class="refresh-btn">
                {{ loadingInterpret ? '解读中...' : '重新生成' }}
              </button>
            </div>
            
            <div v-if="loadingInterpret" class="ai-loading">
              <div class="loading-spinner"></div>
              <span>正在分析热点...</span>
            </div>
            
            <div v-else-if="interpretation" class="ai-content">
              <div class="ai-section" v-if="interpretation.summary">
                <div class="ai-section-title">📋 事件摘要</div>
                <p>{{ interpretation.summary }}</p>
              </div>
              
              <div class="ai-section" v-if="interpretation.key_points?.length">
                <div class="ai-section-title">💡 关键观点</div>
                <ul>
                  <li v-for="(point, idx) in interpretation.key_points" :key="idx">{{ point }}</li>
                </ul>
              </div>
              
              <div class="ai-section" v-if="interpretation.impact">
                <div class="ai-section-title">📊 影响分析</div>
                <p>{{ interpretation.impact }}</p>
              </div>
              
              <div class="ai-section" v-if="interpretation.related_topics?.length">
                <div class="ai-section-title">🔗 相关话题</div>
                <div class="related-tags">
                  <span v-for="(tag, idx) in interpretation.related_topics" :key="idx" class="tag">{{ tag }}</span>
                </div>
              </div>
            </div>
            
            <div v-else-if="interpretError" class="ai-error">
              <span>⚠️ {{ interpretError }}</span>
              <button @click="loadInterpretation" class="retry-btn">重试</button>
            </div>
          </div>
          
          <a :href="topic.url" target="_blank" class="tgmeng-topic-link">查看原文 →</a>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const topic = ref<any>(null)
const rank = ref(0)
const interpretation = ref<any>(null)
const loadingInterpret = ref(false)
const interpretError = ref('')

const formatNumber = (num: number) => num >= 10000 ? (num / 10000).toFixed(1) + 'w' : num

const loadInterpretation = async () => {
  if (!topic.value) return
  loadingInterpret.value = true
  interpretError.value = ''
  
  try {
    const res = await fetch(`/api/topics/${topic.value.id}/interpret`)
    const data = await res.json()
    if (data.success) {
      interpretation.value = data.data
    } else {
      interpretError.value = data.error || '解读失败'
    }
  } catch (e) {
    interpretError.value = '网络错误'
  }
  
  loadingInterpret.value = false
}

onMounted(async () => {
  topic.value = await (await fetch(`/api/topics/${route.params.id}`)).json()
  // 自动加载解读
  loadInterpretation()
})
</script>

<style scoped>
.tgmeng-app {
  min-height: 100vh;
  background: var(--bg);
}
.tgmeng-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}
.tgmeng-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.tgmeng-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
}
.tgmeng-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text);
}
.tgmeng-logo-icon { font-size: 20px; }
.logo-text { font-size: 15px; font-weight: 600; }
.tgmeng-back a { color: #666; text-decoration: none; }
.tgmeng-back a:hover { color: var(--primary); }
.tgmeng-topic-detail { background: var(--bg-card); border-radius: 12px; padding: 32px; color: var(--text); }
.tgmeng-topic-header { margin-bottom: 24px; }
.tgmeng-topic-rank { display: inline-block; padding: 4px 12px; background: #FF6B6B; color: #FFF; border-radius: 4px; font-size: 12px; margin-bottom: 12px; }
.tgmeng-topic-title { font-size: 24px; font-weight: 600; margin: 0 0 12px 0; color: var(--text); }
.tgmeng-topic-meta { display: flex; gap: 8px; }
.tgmeng-topic-stats { display: flex; gap: 32px; padding: 24px 0; border-top: 1px solid var(--border-light); border-bottom: 1px solid var(--border-light); margin: 24px 0; }
.tgmeng-stat-item { text-align: center; }
.tgmeng-stat-value { font-size: 24px; font-weight: 600; color: #FF6B6B; }
.tgmeng-stat-label { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.tgmeng-topic-link { display: inline-block; padding: 12px 24px; background: var(--primary); color: #FFF; border-radius: 6px; text-decoration: none; }

/* AI 解读卡片 */
.ai-interpretation {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
  border: 1px solid rgba(79, 70, 229, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin: 24px 0;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.ai-icon { font-size: 20px; }
.ai-title { font-weight: 600; color: var(--text); flex: 1; }

.refresh-btn {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 12px;
  color: var(--text-muted);
  cursor: pointer;
}

.refresh-btn:hover { border-color: var(--primary); color: var(--primary); }
.refresh-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.ai-loading {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-muted);
  padding: 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.ai-content { display: flex; flex-direction: column; gap: 16px; }

.ai-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 12px;
}

.ai-section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.ai-section p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-muted);
  margin: 0;
}

.ai-section ul {
  margin: 0;
  padding-left: 20px;
}

.ai-section li {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-muted);
}

.related-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 10px;
  background: rgba(79, 70, 229, 0.1);
  border-radius: 12px;
  font-size: 12px;
  color: var(--primary);
}

.ai-error {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ef4444;
  padding: 12px;
}

.retry-btn {
  padding: 6px 12px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}
</style>