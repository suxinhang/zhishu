# 知枢网站 Phase 4 - 真实 AI 对话需求文档

## 一、背景与目标

**当前问题：** 对话功能为模拟回复，用户体验不真实
**目标：** 接入真实 AI API，实现智能对话交互
**截止时间：** 2026-04-08 18:00（预计 2 天）

---

## 二、功能需求

### 2.1 核心功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| AI 对话 | 真实 AI API 接入，智能回复 | P0 |
| 对话历史 | 保存当前对话上下文 | P0 |
| 消息展示 | 用户/AI 消息区分显示 | P0 |
| 加载状态 | AI 思考时显示加载动画 | P1 |
| 错误处理 | API 失败时友好提示 | P1 |
| 对话清空 | 清空当前对话重新开始 | P2 |

### 2.2 API 接口设计

```
POST /api/chat
Request:
{
  "agent_id": 1,
  "message": "你好，请介绍一下你自己",
  "history": [
    {"role": "user", "content": "上一条消息"},
    {"role": "assistant", "content": "AI回复"}
  ]
}

Response:
{
  "reply": "你好！我是情感陪伴助手...",
  "success": true
}
```

### 2.3 前端改造

| 改造项 | 文件 | 说明 |
|--------|------|------|
| 移除模拟回复 | `Chat.vue` | 删除 mockResponses |
| 调用真实 API | `Chat.vue` | fetch `/api/chat` |
| 添加历史上下文 | `Chat.vue` | history 参数传递 |
| 错误提示 | `Chat.vue` | catch 异常显示提示 |
| 清空按钮 | `Chat.vue` | 新增清空对话按钮 |

---

## 三、技术方案

### 3.1 AI 服务商选择

| 服务商 | API | 优势 | 劣势 |
|--------|-----|------|------|
| OpenAI | GPT-4 | 效果最好 | 需要海外付费 |
| Claude | Claude API | 安全可靠 | 同样海外 |
| 阿里云 | 通义千问 | 国内可用 | 中文效果一般 |
| 百度 | 文心一言 | 国内可用 | 效果一般 |
| DeepSeek | DeepSeek API | 国产、性价比高 | 新服务商 |

**建议方案：** DeepSeek API（国内可用、性价比高、中文效果好）

### 3.2 后端实现

```python
# 新增依赖
import httpx

# 新增接口
@app.post("/api/chat")
async def chat(req: ChatRequest):
    # 调用 AI API
    response = await call_ai_api(req.agent_id, req.message, req.history)
    return {"reply": response, "success": True}
```

### 3.3 Agent Personality（智能体人格）

每个智能体需要配置独立的 prompt 人格：

| 智能体 | 人格 Prompt |
|--------|-------------|
| 情感陪伴助手 | 你是温暖、善解人意的陪伴助手，擅长倾听和安慰... |
| 文案写作助手 | 你是专业的文案写作专家，擅长营销文案... |
| 代码助手 | 你是资深程序员，擅长解决技术问题... |

---

## 四、数据库改造

```sql
-- 新增智能体人格表
CREATE TABLE agent_prompts (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    system_prompt TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 对话历史表（可选，后续实现）
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,  -- 暂无用户系统，可为空
    agent_id INTEGER,
    role TEXT,  -- user/assistant
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 五、验收标准

| 标准 | 说明 |
|------|------|
| ✅ 真实对话 | 用户发送消息，AI 真实回复 |
| ✅ 多轮对话 | 上下文传递，AI 能记住之前对话 |
| ✅ 人格差异 | 不同智能体回复风格不同 |
| ✅ 加载动画 | AI 思考时显示"正在思考..." |
| ✅ 错误提示 | API 失败时显示友好提示 |
| ✅ 清空对话 | 可清空当前对话重新开始 |

---

## 六、风险与应对

| 风险 | 应对方案 |
|------|----------|
| API 付费问题 | 使用免费额度或用户自行配置 API Key |
| API 响应慢 | 添加 loading 状态，超时提示 |
| API 配额限制 | 添加调用频率限制 |
| 智能体人格配置 | 预置 5 个常用智能体的 prompt |

---

## 七、排期计划

| 日期 | 任务 | 负责人 |
|------|------|--------|
| 4/7 晚 | 需求评审 + API 选型确认 | 产品 + 后端 |
| 4/8 上午 | 后端 API 实现 | 后端研发 |
| 4/8 下午 | 前端联调 + 测试 | 前端 + 测试 |
| 4/8 晚上 | UAT 验收 + 上线 | 全员 |

---

**产品经理签名：** 📝  
**时间：** 2026-04-07 18:25