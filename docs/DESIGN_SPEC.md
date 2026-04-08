# 糖果梦热榜 - 精确设计规范

## 一、设计理念

**核心理念：** "科技不该冰冷，人性不该傲慢"
**设计风格：** 简洁、清爽、高效、实用

---

## 二、配色方案

### 主色调
```
主背景：#FFFFFF（白色）
次背景：#F5F5F5（浅灰）
边框色：#E5E5E5（灰色边框）
```

### 文字颜色
```
主标题：#1A1A1A（深黑）
副标题：#666666（灰色）
辅助文字：#999999（浅灰）
链接文字：#1890FF（蓝色）
```

### 强调色
```
主强调：#FF6B6B（糖果红）
次强调：#4ECDC4（薄荷绿）
成功色：#52C41A（绿色）
警告色：#FAAD14（黄色）
```

---

## 三、字体规范

```css
/* 主字体 */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* 字号 */
标题 H1: 20px font-weight: 600
标题 H2: 16px font-weight: 600
正文: 14px
辅助文字: 12px
小字: 10px

/* 行高 */
行高: 1.5
```

---

## 四、布局规范

### 整体布局
```
最大宽度：1200px
内边距：16px（移动端），24px（PC端）
卡片间距：16px
```

### 导航栏
```
高度：56px
背景：#FFFFFF
底部边框：1px solid #E5E5E5
Logo区：左侧，包含图标+文字
分类区：中间，药丸式标签
搜索区：右侧，圆角输入框
```

### 热点列表
```
每项高度：64px
左侧：排名徽章（24px 圆形）
中间：标题 + 来源/分类标签
右侧：数据统计 + 糖果指数
底部边框：1px solid #F0F0F0
```

---

## 五、组件规范

### 排名徽章
```css
/* TOP 1-3 特殊样式 */
.rank-1 {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #8B4513;
  font-weight: 600;
}

.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
  color: #333;
}

.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #8B4513);
  color: #FFF;
}

/* 普通排名 */
.rank-normal {
  color: #999;
  font-size: 14px;
}
```

### 来源标签
```css
.source-tag {
  padding: 2px 8px;
  border-radius: 4px;
  background: #F5F5F5;
  color: #666;
  font-size: 12px;
}
```

### 糖果指数
```css
.sugar-index {
  font-size: 16px;
  font-weight: 600;
  color: #FF6B6B;
}

.sugar-label {
  font-size: 10px;
  color: #CCC;
}
```

---

## 六、交互规范

### Hover 效果
```css
/* 列表项 hover */
.list-item:hover {
  background: #FAFAFA;
}

/* 标题 hover */
.title:hover {
  color: #1890FF;
}
```

### 过渡动画
```css
transition: all 0.2s ease;
```

---

## 七、响应式设计

```
/* PC 端 */
> 768px: 显示完整导航，3列布局

/* 移动端 */
< 768px: 隐藏部分导航，单列布局，分类横向滚动
```

---

## 八、设计差异化（保持）

1. **糖果指数** - 独特的评分体系展示
2. **AI 模式** - 紫色渐变简报卡片
3. **模式切换** - 药丸式按钮
4. **核心理念** - "科技不该冰冷，人性不该傲慢"

---

**设计师签名：** 🦊  
**时间：** 2026-04-08 15:12