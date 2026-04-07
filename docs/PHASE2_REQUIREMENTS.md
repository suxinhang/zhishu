# 知枢网站 Phase 2 - 需求文档

## 一、目标

**截止时间：** 今晚 18:00（剩余 55 分钟）  
**交付内容：** 智能体评分 + 热门排行 + 搜索历史

---

## 二、功能需求详细设计

### 1. 智能体评分系统

#### 1.1 数据库设计
```sql
-- 智能体表添加字段
ALTER TABLE agents ADD COLUMN rating REAL DEFAULT 0;
ALTER TABLE agents ADD COLUMN rating_count INTEGER DEFAULT 0;

-- 评分记录表
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    score INTEGER CHECK(score >= 1 AND score <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 1.2 API 接口
```
POST /api/agents/{id}/rate
Body: {"score": 5}
Response: {"avg_rating": 4.8, "count": 128}

GET /api/agents?sort=rating
Response: 按评分排序的智能体列表
```

#### 1.3 前端组件
- **评分组件：** 5星评分，支持点击打分
- **显示评分：** 星星 + 分数 + 评分人数
- **位置：** 智能体卡片底部

---

### 2. 热门智能体排行

#### 2.1 数据库设计
```sql
-- 智能体表添加字段
ALTER TABLE agents ADD COLUMN view_count INTEGER DEFAULT 0;
ALTER TABLE agents ADD COLUMN chat_count INTEGER DEFAULT 0;

-- 热度计算：view_count * 1 + chat_count * 5 + rating * 100
```

#### 2.2 API 接口
```
GET /api/agents?sort=hot
Response: 按热度排序的智能体列表

GET /api/agents/hot
Response: TOP 10 热门智能体
```

#### 2.3 前端展示
- **首页热门区：** 横向滚动展示 TOP 5
- **排序按钮：** 热门 / 最新 / 评分
- **热度标签：** 🔥 HOT 标签

---

### 3. 搜索历史记录

#### 3.1 实现方式
- **前端 localStorage 存储**（快速实现，无需后端）
- 最多保存 10 条搜索记录
- 点击历史记录直接搜索

#### 3.2 前端组件
- **位置：** 搜索框下方，点击搜索框时显示
- **样式：** 标签式展示，可删除
- **交互：** 点击历史词直接搜索

---

## 三、优先级排序

| 优先级 | 功能 | 耗时估算 | 负责人 |
|---|---|---|---|
| P0 | 热门排行（后端） | 15 分钟 | 后端研发 |
| P0 | 热门排行（前端） | 15 分钟 | 前端研发 |
| P1 | 评分系统（后端） | 15 分钟 | 后端研发 |
| P1 | 评分系统（前端） | 15 分钟 | 前端研发 |
| P2 | 搜索历史（前端） | 10 分钟 | 前端研发 |

**总耗时：** 约 55 分钟

---

## 四、验收标准

### 热门排行
- ✅ 首页展示 TOP 5 热门智能体
- ✅ 支持按热度/评分/最新排序
- ✅ 热度标签显示

### 评分系统
- ✅ 智能体卡片显示评分
- ✅ 点击星星可打分
- ✅ 评分实时更新

### 搜索历史
- ✅ 搜索框聚焦显示历史记录
- ✅ 点击历史记录直接搜索
- ✅ 可删除历史记录

---

**产品经理签名：** 🦊  
**时间：** 2026-04-07 17:05