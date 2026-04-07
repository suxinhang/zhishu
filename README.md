# 知枢网站 MVP

智能体开发平台 - Vue3 + FastAPI

## 快速启动

### 后端
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```
访问 http://localhost:8000/docs 查看 API 文档

### 前端
```bash
cd frontend
npm install
npm run dev
```
访问 http://localhost:3000

## 功能
- 首页搜索 + 分类筛选
- 智能体卡片展示
- 详情页
- 模拟对话界面

## 技术栈
- 前端: Vue3 + Vite + Tailwind CSS
- 后端: FastAPI + SQLite
- API: RESTful + Swagger