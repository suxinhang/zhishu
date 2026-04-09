<template>
  <div class="agents-page">
    <!-- 头部 -->
    <header class="header">
      <div class="container">
        <div class="nav">
          <a href="/" class="logo">
            <img src="/logo.svg" alt="知枢" height="28" />
          </a>
          <div class="nav-tabs">
            <span class="active">智能体</span>
            <a href="/tgmeng">热榜</a>
          </div>
        </div>
      </div>
    </header>

    <!-- 搜索区 -->
    <section class="search-section">
      <div class="container">
        <div class="search-box">
          <div class="search-icon">🔍</div>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="搜索智能体能力、场景..."
            @input="doSearch"
          />
          <div class="search-hot">
            <span>热门：</span>
            <button @click="searchQuery = '写作'">写作</button>
            <button @click="searchQuery = '编程'">编程</button>
            <button @click="searchQuery = '翻译'">翻译</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 分类区 -->
    <section class="categories">
      <div class="container">
        <div class="category-scroll">
          <button 
            @click="selectCategory(null)"
            :class="['cat-btn', { active: !selectedCategory }]"
          >
            全部
          </button>
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectCategory(cat.id)"
            :class="['cat-btn', { active: selectedCategory === cat.id }]"
          >
            {{ cat.icon }} {{ cat.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- 推荐区 -->
    <section class="featured" v-if="!searchQuery && featuredAgents.length > 0">
      <div class="container">
        <div class="section-header">
          <h2>🔥 热门推荐</h2>
          <p>最受欢迎的智能体</p>
        </div>
        <div class="featured-grid">
          <div 
            v-for="agent in featuredAgents" 
            :key="agent.id"
            class="featured-card"
            @click="goToChat(agent)"
          >
            <div class="featured-icon">{{ agent.icon }}</div>
            <div class="featured-info">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
              <div class="featured-meta">
                <span class="rating">⭐ {{ agent.rating }}</span>
                <span class="users">👥 {{ formatNum(agent.users) }} 人使用</span>
              </div>
            </div>
            <div class="featured-arrow">→</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 智能体列表 -->
    <section class="agents-list">
      <div class="container">
        <div class="section-header">
          <h2>{{ searchQuery ? '搜索结果' : '全部智能体' }}</h2>
          <div class="sort-btns">
            <button @click="sortBy('hot')" :class="{ active: sort === 'hot' }">最热</button>
            <button @click="sortBy('rating')" :class="{ active: sort === 'rating' }">评分</button>
            <button @click="sortBy('new')" :class="{ active: sort === 'new' }">最新</button>
          </div>
        </div>
        
        <div class="agents-grid">
          <div 
            v-for="agent in filteredAgents" 
            :key="agent.id"
            class="agent-card"
            @click="goToDetail(agent)"
          >
            <div class="card-header">
              <div class="agent-icon">{{ agent.icon }}</div>
              <div class="agent-badge" v-if="agent.isNew">NEW</div>
            </div>
            <div class="card-body">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
              <div class="card-tags">
                <span class="tag">{{ agent.category }}</span>
                <span class="tag">{{ agent.scenario }}</span>
              </div>
            </div>
            <div class="card-footer">
              <div class="card-stats">
                <span>⭐ {{ agent.rating }}</span>
                <span>{{ formatNum(agent.users) }}人</span>
              </div>
              <button class="chat-btn" @click.stop="goToChat(agent)">对话</button>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="filteredAgents.length === 0" class="empty">
          <div class="empty-icon">🔍</div>
          <p>未找到相关智能体</p>
          <button @click="searchQuery = ''">查看全部</button>
        </div>
      </div>
    </section>

    <!-- 能力说明 -->
    <section class="capabilities">
      <div class="container">
        <h2>💡 智能体能力</h2>
        <div class="cap-grid">
          <div class="cap-card">
            <div class="cap-icon">✍️</div>
            <h3>内容创作</h3>
            <p>文案写作、小说创作、公文写作、营销策划</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">💻</div>
            <h3>编程开发</h3>
            <p>代码生成、Bug修复、架构设计、代码审查</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">🌐</div>
            <h3>语言翻译</h3>
            <p>多语言互译、文档翻译、口语对话</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">🎨</div>
            <h3>创意设计</h3>
            <p>UI设计、海报生成、Logo设计、插画创作</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">📊</div>
            <h3>数据分析</h3>
            <p>数据可视化、报表生成、趋势分析</p>
          </div>
          <div class="cap-card">
            <div class="cap-icon">🎯</div>
            <h3>学习辅导</h3>
            <p>知识问答、作业辅导、考试备考</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>🧠 知枢 · 让智能触手可及</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 模拟数据
const categories = ref([
  { id: 1, name: '写作', icon: '✍️' },
  { id: 2, name: '编程', icon: '💻' },
  { id: 3, name: '翻译', icon: '🌐' },
  { id: 4, name: '设计', icon: '🎨' },
  { id: 5, name: '学习', icon: '📚' },
  { id: 6, name: '效率', icon: '⚡' },
  { id: 7, name: '娱乐', icon: '🎮' },
])

const agents = ref([
  { id: 1, name: '文案大师', icon: '✍️', description: '专业文案创作，一键生成营销文案', category: '写作', scenario: '营销', rating: 4.9, users: 12580, isNew: true },
  { id: 2, name: '代码助手', icon: '💻', description: '智能编程助手，代码生成与优化', category: '编程', scenario: '开发', rating: 4.8, users: 8960, isNew: false },
  { id: 3, name: '翻译官', icon: '🌐', description: '支持100+语言精准翻译', category: '翻译', scenario: '多语言', rating: 4.7, users: 15320, isNew: false },
  { id: 4, name: '设计精灵', icon: '🎨', description: 'AI设计助手，快速生成设计稿', category: '设计', scenario: 'UI设计', rating: 4.6, users: 6740, isNew: true },
  { id: 5, name: '论文帮手', icon: '📚', description: '学术写作辅助，论文润色优化', category: '学习', scenario: '学术', rating: 4.8, users: 9850, isNew: false },
  { id: 6, name: 'PPT大师', icon: '📊', description: '一键生成精美PPT演示文稿', category: '效率', scenario: '办公', rating: 4.5, users: 11200, isNew: false },
  { id: 7, name: '情感陪伴', icon: '❤️', description: '温暖陪伴，倾听你的心事', category: '娱乐', scenario: '陪伴', rating: 4.9, users: 18900, isNew: false },
  { id: 8, name: '简历优化师', icon: '📄', description: '专业简历优化，提升求职竞争力', category: '效率', scenario: '求职', rating: 4.7, users: 7650, isNew: true },
  { id: 9, name: '小说创作', icon: '📖', description: '创意故事生成，小说情节设计', category: '写作', scenario: '创作', rating: 4.6, users: 5430, isNew: false },
  { id: 10, name: 'SQL专家', icon: '🗄️', description: 'SQL语句生成与优化', category: '编程', scenario: '数据库', rating: 4.8, users: 4320, isNew: false },
  { id: 11, name: '口语教练', icon: '🗣️', description: '英语口语练习与纠正', category: '学习', scenario: '语言', rating: 4.5, users: 8900, isNew: false },
  { id: 12, name: '公文写作', icon: '📝', description: '政府公文、商务文档生成', category: '写作', scenario: '公文', rating: 4.7, users: 6780, isNew: false },
])

const searchQuery = ref('')
const selectedCategory = ref(null)
const sort = ref('hot')

const featuredAgents = computed(() => {
  return [...agents.value]
    .sort((a, b) => b.users - a.users)
    .slice(0, 3)
})

const filteredAgents = computed(() => {
  let result = agents.value
  
  if (selectedCategory.value) {
    result = result.filter(a => a.category === categories.value.find(c => c.id === selectedCategory.value)?.name)
  }
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(a => 
      a.name.toLowerCase().includes(q) ||
      a.description.toLowerCase().includes(q) ||
      a.category.toLowerCase().includes(q) ||
      a.scenario.toLowerCase().includes(q)
    )
  }
  
  if (sort.value === 'hot') {
    result = [...result].sort((a, b) => b.users - a.users)
  } else if (sort.value === 'rating') {
    result = [...result].sort((a, b) => b.rating - a.rating)
  }
  
  return result
})

const formatNum = n => n >= 10000 ? (n/10000).toFixed(1) + 'w' : n >= 1000 ? (n/1000).toFixed(1) + 'k' : n

const selectCategory = id => {
  selectedCategory.value = selectedCategory.value === id ? null : id
}

const sortBy = s => {
  sort.value = s
}

const doSearch = () => {}

const goToDetail = agent => {
  window.location.href = `/agents/${agent.id}`
}

const goToChat = agent => {
  window.location.href = `/chat/${agent.id}`
}
</script>

<style scoped>
.agents-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
.header {
  background: #fff;
  border-bottom: 1px solid #eee;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}

.nav-tabs {
  display: flex;
  gap: 24px;
}

.nav-tabs a, .nav-tabs span {
  color: #666;
  text-decoration: none;
  font-size: 14px;
  cursor: pointer;
}

.nav-tabs .active {
  color: #667eea;
  font-weight: 500;
}

/* Search */
.search-section {
  padding: 40px 0 20px;
  background: linear-gradient(180deg, #fff 0%, #f8f9fa 100%);
}

.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-box input {
  width: 100%;
  padding: 16px 20px 16px 50px;
  border: 2px solid #eee;
  border-radius: 12px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s;
}

.search-box input:focus {
  border-color: #667eea;
}

.search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
}

.search-hot {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #999;
}

.search-hot button {
  padding: 4px 10px;
  background: #f0f0f0;
  border: none;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
}

.search-hot button:hover {
  background: #667eea;
  color: #fff;
}

/* Categories */
.categories {
  padding: 20px 0;
  background: #f8f9fa;
}

.category-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.cat-btn {
  padding: 8px 20px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 20px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.cat-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.cat-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border-color: transparent;
}

/* Featured */
.featured {
  padding: 40px 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 20px;
  margin: 0;
}

.section-header p {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.featured-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.featured-card:hover {
  box-shadow: 0 4px 20px rgba(102,126,234,0.15);
}

.featured-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #f0f2ff, #f8f0ff);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.featured-info {
  flex: 1;
}

.featured-info h3 {
  margin: 0 0 4px;
  font-size: 16px;
}

.featured-info p {
  margin: 0;
  font-size: 13px;
  color: #666;
}

.featured-meta {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.featured-meta .rating {
  color: #f5a623;
}

.featured-arrow {
  color: #ccc;
  font-size: 18px;
}

/* Agents Grid */
.agents-list {
  padding: 40px 0;
}

.sort-btns {
  display: flex;
  gap: 8px;
}

.sort-btns button {
  padding: 6px 14px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
}

.sort-btns button.active {
  background: #667eea;
  color: #fff;
  border-color: #667eea;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.agent-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.agent-card:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.card-header {
  padding: 20px 16px 12px;
  display: flex;
  justify-content: space-between;
}

.agent-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f0f2ff, #f8f0ff);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.agent-badge {
  padding: 2px 8px;
  background: #ff6b6b;
  color: #fff;
  font-size: 10px;
  border-radius: 8px;
}

.card-body {
  padding: 0 16px 12px;
}

.card-body h3 {
  margin: 0 0 6px;
  font-size: 15px;
}

.card-body p {
  margin: 0;
  font-size: 12px;
  color: #666;
  line-height: 1.4;
}

.card-tags {
  margin-top: 10px;
  display: flex;
  gap: 6px;
}

.tag {
  padding: 3px 8px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 11px;
  color: #666;
}

.card-footer {
  padding: 12px 16px;
  border-top: 1px solid #f5f5f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-stats {
  font-size: 12px;
  color: #999;
}

.card-stats span {
  margin-right: 12px;
}

.chat-btn {
  padding: 6px 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border: none;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
}

/* Empty */
.empty {
  text-align: center;
  padding: 60px 0;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty p {
  color: #999;
  margin: 0 0 16px;
}

.empty button {
  padding: 10px 24px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* Capabilities */
.capabilities {
  padding: 40px 0;
  background: #fff;
}

.capabilities h2 {
  text-align: center;
  margin: 0 0 32px;
  font-size: 24px;
}

.cap-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.cap-card {
  text-align: center;
  padding: 24px 16px;
  background: #f8f9fa;
  border-radius: 12px;
}

.cap-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.cap-card h3 {
  margin: 0 0 8px;
  font-size: 14px;
}

.cap-card p {
  margin: 0;
  font-size: 12px;
  color: #666;
  line-height: 1.4;
}

/* Footer */
.footer {
  padding: 32px 0;
  text-align: center;
  color: #999;
  font-size: 13px;
}

/* Responsive */
@media (max-width: 900px) {
  .featured-grid {
    grid-template-columns: 1fr;
  }
  
  .agents-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cap-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .search-hot { display: none; }
  
  .agents-grid {
    grid-template-columns: 1fr;
  }
  
  .cap-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>