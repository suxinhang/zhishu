from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
import json
import httpx
import os

app = FastAPI(title="知枢 API", docs_url="/docs", redoc_url="/redoc")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库（使用 SQLite 简化 MVP）
DATABASE_URL = "sqlite:///./zhishu.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 模型定义
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    icon = Column(String(10))
    sort = Column(Integer, default=0)

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    icon = Column(String(20))
    url = Column(String(200))
    sort = Column(Integer, default=0)

class HotTopic(Base):
    __tablename__ = "hot_topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    platform_id = Column(Integer)
    category_id = Column(Integer)
    hot_value = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    url = Column(String(500))
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    icon = Column(String(10))
    description = Column(String(500))
    category_id = Column(Integer)
    sort = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    chat_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentPrompt(Base):
    __tablename__ = "agent_prompts"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer)
    system_prompt = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# 创建表
Base.metadata.create_all(bind=engine)

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 初始化数据
def init_data():
    db = SessionLocal()
    
    # 初始化平台
    if db.query(Platform).count() == 0:
        platforms = [
            Platform(id=1, name="微博", icon="📱", url="https://s.weibo.com/top/summary", sort=1),
            Platform(id=2, name="知乎", icon="🔵", url="https://www.zhihu.com/hot", sort=2),
            Platform(id=3, name="抖音", icon="🎬", url="https://www.douyin.com/hot", sort=3),
            Platform(id=4, name="百度", icon="🔍", url="https://top.baidu.com", sort=4),
            Platform(id=5, name="今日头条", icon="📰", url="https://www.toutiao.com", sort=5),
            Platform(id=6, name="虎扑", icon="🏀", url="https://www.hupu.com", sort=6),
            Platform(id=7, name="豆瓣", icon="🎬", url="https://www.douban.com", sort=7),
            Platform(id=8, name="B站", icon="📺", url="https://www.bilibili.com/v/popular/rank/all", sort=8),
        ]
        db.add_all(platforms)
    
    # 初始化热点分类
    if db.query(Category).count() == 0:
        categories = [
            Category(id=1, name="科技", icon="💻", sort=1),
            Category(id=2, name="财经", icon="💰", sort=2),
            Category(id=3, name="娱乐", icon="🎭", sort=3),
            Category(id=4, name="游戏", icon="🎮", sort=4),
            Category(id=5, name="社会", icon="🌍", sort=5),
            Category(id=6, name="体育", icon="⚽", sort=6),
            Category(id=7, name="其他", icon="📋", sort=7),
        ]
        db.add_all(categories)
    
    # 初始化热点数据
    if db.query(HotTopic).count() == 0:
        topics = [
            HotTopic(id=1, title="OpenAI发布GPT-5", platform_id=1, category_id=1, hot_value=1000000, rank=1, url="https://weibo.com/example1", summary="OpenAI发布了最新的GPT-5模型，性能大幅提升"),
            HotTopic(id=2, title="苹果股价创新高", platform_id=2, category_id=2, hot_value=850000, rank=1, url="https://zhihu.com/example2", summary="苹果公司股价突破历史新高"),
            HotTopic(id=3, title="某明星官宣结婚", platform_id=3, category_id=3, hot_value=720000, rank=1, url="https://douyin.com/example3", summary="知名演员官宣结婚消息"),
            HotTopic(id=4, title="《黑神话》销量破千万", platform_id=4, category_id=4, hot_value=680000, rank=2, url="https://baidu.com/example4", summary="国产游戏《黑神话：悟空》销量突破千万"),
            HotTopic(id=5, title="新能源补贴政策", platform_id=5, category_id=5, hot_value=560000, rank=3, url="https://toutiao.com/example5", summary="国家发布新能源汽车补贴新政策"),
            HotTopic(id=6, title="CBA季后赛直播", platform_id=6, category_id=6, hot_value=450000, rank=2, url="https://hupu.com/example6", summary="CBA季后赛精彩对决"),
            HotTopic(id=7, title="豆瓣年度榜单发布", platform_id=7, category_id=3, hot_value=380000, rank=4, url="https://douban.com/example7", summary="豆瓣发布年度电影榜单"),
            HotTopic(id=8, title="B站UP主百万粉丝", platform_id=8, category_id=4, hot_value=320000, rank=5, url="https://bilibili.com/example8", summary="多位UP主粉丝突破百万"),
            HotTopic(id=9, title="小米新品发布会", platform_id=1, category_id=1, hot_value=950000, rank=2, url="https://weibo.com/example9", summary="小米发布新款手机和智能家居产品"),
            HotTopic(id=10, title="特斯拉降价风波", platform_id=2, category_id=2, hot_value=780000, rank=2, url="https://zhihu.com/example10", summary="特斯拉再次降价引发热议"),
            HotTopic(id=11, title="综艺节目热播", platform_id=3, category_id=3, hot_value=620000, rank=2, url="https://douyin.com/example11", summary="热门综艺节目收视率创新高"),
            HotTopic(id=12, title="Steam新品发售", platform_id=4, category_id=4, hot_value=520000, rank=4, url="https://baidu.com/example12", summary="Steam平台多款新游戏发售"),
        ]
        db.add_all(topics)
    
    # 智能体相关数据（保留原有）
    if db.query(Agent).count() == 0:
        agents = [
            Agent(id=1, name="热点分析助手", icon="🔥", description="智能分析热点趋势", category_id=1, sort=1, rating=4.8, rating_count=128, view_count=1520, chat_count=356),
            Agent(id=2, name="财经解读助手", icon="💰", description="解读财经热点新闻", category_id=2, sort=2, rating=4.6, rating_count=89, view_count=980, chat_count=245),
            Agent(id=3, name="娱乐八卦助手", icon="🎭", description="了解娱乐圈动态", category_id=3, sort=1, rating=4.9, rating_count=256, view_count=3200, chat_count=890),
            Agent(id=4, name="游戏资讯助手", icon="🎮", description="游戏圈最新消息", category_id=4, sort=2, rating=4.7, rating_count=167, view_count=2100, chat_count=567),
        ]
        db.add_all(agents)
        
        prompts = [
            AgentPrompt(agent_id=1, system_prompt="你是热点分析助手，擅长分析各平台热点话题的趋势和背景。"),
            AgentPrompt(agent_id=2, system_prompt="你是财经解读助手，擅长解读财经新闻、股市动态。"),
            AgentPrompt(agent_id=3, system_prompt="你是娱乐八卦助手，了解娱乐圈最新动态，分享有趣八卦。"),
            AgentPrompt(agent_id=4, system_prompt="你是游戏资讯助手，了解游戏圈最新消息、游戏攻略。"),
        ]
        db.add_all(prompts)
    
    db.commit()
    db.close()

init_data()

# Pydantic 模型
class RatingRequest(BaseModel):
    score: int

class ChatRequest(BaseModel):
    agent_id: int
    message: str
    history: list = []

class ChatHistory(BaseModel):
    role: str
    content: str

# API 接口

# ===== 热点聚合 API =====

@app.get("/api/platforms")
def get_platforms():
    db = SessionLocal()
    platforms = db.query(Platform).order_by(Platform.sort).all()
    db.close()
    return [{"id": p.id, "name": p.name, "icon": p.icon, "url": p.url} for p in platforms]

@app.get("/api/topics")
def get_topics(platform: int = None, category: int = None, sort: str = None):
    db = SessionLocal()
    query = db.query(HotTopic)
    
    if platform:
        query = query.filter(HotTopic.platform_id == platform)
    if category:
        query = query.filter(HotTopic.category_id == category)
    
    # 排序
    if sort == "hot":
        query = query.order_by(HotTopic.hot_value.desc())
    else:
        query = query.order_by(HotTopic.rank)
    
    topics = query.all()
    
    # 获取平台和分类名称
    platforms = {p.id: {"name": p.name, "icon": p.icon} for p in db.query(Platform).all()}
    categories = {c.id: {"name": c.name, "icon": c.icon} for c in db.query(Category).all()}
    db.close()
    
    return [{
        "id": t.id,
        "title": t.title,
        "platform_id": t.platform_id,
        "platform_name": platforms.get(t.platform_id, {}).get("name", "未知"),
        "platform_icon": platforms.get(t.platform_id, {}).get("icon", "📱"),
        "category_id": t.category_id,
        "category_name": categories.get(t.category_id, {}).get("name", "其他"),
        "category_icon": categories.get(t.category_id, {}).get("icon", "📋"),
        "hot_value": t.hot_value,
        "rank": t.rank,
        "url": t.url,
        "summary": t.summary
    } for t in topics]

@app.get("/api/topics/hot")
def get_hot_topics():
    db = SessionLocal()
    topics = db.query(HotTopic).order_by(HotTopic.hot_value.desc()).limit(10).all()
    
    platforms = {p.id: {"name": p.name, "icon": p.icon} for p in db.query(Platform).all()}
    db.close()
    
    return [{
        "id": t.id,
        "title": t.title,
        "platform_name": platforms.get(t.platform_id, {}).get("name", "未知"),
        "platform_icon": platforms.get(t.platform_id, {}).get("icon", "📱"),
        "hot_value": t.hot_value,
        "rank": t.rank,
        "url": t.url
    } for t in topics]

@app.get("/api/topics/{topic_id}")
def get_topic(topic_id: int):
    db = SessionLocal()
    topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
    if not topic:
        db.close()
        return {"error": "Topic not found"}
    
    platform = db.query(Platform).filter(Platform.id == topic.platform_id).first()
    category = db.query(Category).filter(Category.id == topic.category_id).first()
    db.close()
    
    return {
        "id": topic.id,
        "title": topic.title,
        "platform_id": topic.platform_id,
        "platform_name": platform.name if platform else "未知",
        "platform_icon": platform.icon if platform else "📱",
        "category_id": topic.category_id,
        "category_name": category.name if category else "其他",
        "hot_value": topic.hot_value,
        "rank": topic.rank,
        "url": topic.url,
        "summary": topic.summary,
        "created_at": topic.created_at.isoformat() if topic.created_at else None
    }

# ===== 原有智能体 API =====

@app.get("/api/categories")
def get_categories():
    db = SessionLocal()
    cats = db.query(Category).order_by(Category.sort).all()
    db.close()
    return [{"id": c.id, "name": c.name, "icon": c.icon} for c in cats]

@app.get("/api/agents")
def get_agents(category: int = None, sort: str = None):
    db = SessionLocal()
    query = db.query(Agent)
    
    if category:
        query = query.filter(Agent.category_id == category)
    
    # 排序
    if sort == "rating":
        query = query.order_by(Agent.rating.desc())
    elif sort == "hot":
        # 热度 = 浏览量 + 对话量*5 + 评分*100
        query = query.order_by(
            (Agent.view_count + Agent.chat_count * 5 + Agent.rating * 100).desc()
        )
    else:
        query = query.order_by(Agent.sort)
    
    agents = query.all()
    
    # 获取分类名称
    cats = {c.id: c.name for c in db.query(Category).all()}
    db.close()
    
    return [{
        "id": a.id,
        "name": a.name,
        "icon": a.icon,
        "description": a.description,
        "category_id": a.category_id,
        "category_name": cats.get(a.category_id, "其他"),
        "rating": round(a.rating, 1),
        "rating_count": a.rating_count,
        "view_count": a.view_count,
        "chat_count": a.chat_count
    } for a in agents]

@app.get("/api/agents/hot")
def get_hot_agents():
    db = SessionLocal()
    agents = db.query(Agent).order_by(
        (Agent.view_count + Agent.chat_count * 5 + Agent.rating * 100).desc()
    ).limit(5).all()
    
    cats = {c.id: c.name for c in db.query(Category).all()}
    db.close()
    
    return [{
        "id": a.id,
        "name": a.name,
        "icon": a.icon,
        "description": a.description,
        "category_name": cats.get(a.category_id, "其他"),
        "rating": round(a.rating, 1),
        "rating_count": a.rating_count,
        "hot_score": a.view_count + a.chat_count * 5 + int(a.rating * 100)
    } for a in agents]

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: int):
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        db.close()
        return {"error": "Agent not found"}
    
    # 增加浏览量
    agent.view_count += 1
    db.commit()
    
    cat = db.query(Category).filter(Category.id == agent.category_id).first()
    db.close()
    
    return {
        "id": agent.id,
        "name": agent.name,
        "icon": agent.icon,
        "description": agent.description,
        "category_id": agent.category_id,
        "category_name": cat.name if cat else "其他",
        "rating": round(agent.rating, 1),
        "rating_count": agent.rating_count,
        "view_count": agent.view_count,
        "chat_count": agent.chat_count
    }

@app.post("/api/agents/{agent_id}/rate")
def rate_agent(agent_id: int, req: RatingRequest):
    db = SessionLocal()
    
    # 保存评分
    rating = Rating(agent_id=agent_id, score=req.score)
    db.add(rating)
    
    # 更新智能体平均评分
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        agent.rating_count += 1
        # 计算新平均分
        ratings = db.query(Rating).filter(Rating.agent_id == agent_id).all()
        if len(ratings) > 0:
            total_score = sum(r.score for r in ratings)
            agent.rating = total_score / len(ratings)
    
    db.commit()
    avg_rating = round(agent.rating, 1) if agent and len(ratings) > 0 else req.score
    count = agent.rating_count if agent else 1
    db.close()
    
    return {"success": True, "avg_rating": avg_rating, "count": count}

@app.post("/api/agents/{agent_id}/chat")
def record_chat(agent_id: int):
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        agent.chat_count += 1
        db.commit()
    db.close()
    return {"success": True}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    db = SessionLocal()
    
    # 获取智能体人格
    prompt = db.query(AgentPrompt).filter(AgentPrompt.agent_id == req.agent_id).first()
    agent = db.query(Agent).filter(Agent.id == req.agent_id).first()
    
    # 增加对话计数
    if agent:
        agent.chat_count += 1
        db.commit()
    
    db.close()
    
    system_prompt = prompt.system_prompt if prompt else "你是知枢的智能助手，请友好、有帮助地回答用户问题。"
    
    # 构建消息
    messages = [{"role": "system", "content": system_prompt}]
    for h in req.history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": req.message})
    
    # 调用 DeepSeek API（如果没有 API Key，使用模拟回复）
    if DEEPSEEK_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    DEEPSEEK_API_URL,
                    headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                    json={
                        "model": "deepseek-chat",
                        "messages": messages,
                        "max_tokens": 500
                    }
                )
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                return {"reply": reply, "success": True}
        except Exception as e:
            # API 调用失败，使用备用回复
            return {"reply": f"抱歉，AI服务暂时不可用。请稍后再试。", "success": False, "error": str(e)}
    else:
        # 模拟回复（开发环境）
        mock_responses = [
            "这是一个很有趣的问题，让我想想...",
            "根据我的经验，这个问题可以这样解决。",
            "我很乐意帮助你！请告诉我更多细节。",
            "好的，我来帮你分析一下。",
            "这个话题很有意思，我们可以深入讨论。",
            "你的想法很有创意！我建议...",
        ]
        import random
        reply = random.choice(mock_responses)
        return {"reply": reply, "success": True, "mock": True}

@app.get("/")
def root():
    return {"message": "知枢 API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)