from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
import json

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

# 创建表
Base.metadata.create_all(bind=engine)

# 初始化数据
def init_data():
    db = SessionLocal()
    
    if db.query(Category).count() == 0:
        categories = [
            Category(id=1, name="陪伴", icon="❤️", sort=1),
            Category(id=2, name="写作", icon="✏️", sort=2),
            Category(id=3, name="翻译", icon="🌐", sort=3),
            Category(id=4, name="绘画", icon="🎨", sort=4),
            Category(id=5, name="编程", icon="💻", sort=5),
            Category(id=6, name="产品", icon="📊", sort=6),
            Category(id=7, name="其他", icon="🔧", sort=7),
        ]
        db.add_all(categories)
        
        agents = [
            Agent(id=1, name="情感陪伴助手", icon="❤️", description="温暖陪伴，倾听你的心事", category_id=1, sort=1, rating=4.8, rating_count=128, view_count=1520, chat_count=356),
            Agent(id=2, name="心理咨询助手", icon="🧠", description="专业心理支持，帮你排解困扰", category_id=1, sort=2, rating=4.6, rating_count=89, view_count=980, chat_count=245),
            Agent(id=3, name="文案写作助手", icon="✏️", description="写出打动人心的文案", category_id=2, sort=1, rating=4.9, rating_count=256, view_count=3200, chat_count=890),
            Agent(id=4, name="小说创作助手", icon="📖", description="激发灵感，创作精彩故事", category_id=2, sort=2, rating=4.7, rating_count=167, view_count=2100, chat_count=567),
            Agent(id=5, name="多语言翻译助手", icon="🌐", description="精准翻译，跨越语言障碍", category_id=3, sort=1, rating=4.5, rating_count=78, view_count=890, chat_count=123),
            Agent(id=6, name="AI绘画助手", icon="🎨", description="创意无限，描绘你的想象", category_id=4, sort=1, rating=4.8, rating_count=198, view_count=2800, chat_count=678),
            Agent(id=7, name="代码助手", icon="💻", description="高效编程，解决技术难题", category_id=5, sort=1, rating=4.9, rating_count=312, view_count=4500, chat_count=1200),
            Agent(id=8, name="Debug助手", icon="🔍", description="快速定位问题，优化代码", category_id=5, sort=2, rating=4.7, rating_count=145, view_count=1900, chat_count=456),
            Agent(id=9, name="产品经理助手", icon="📊", description="产品规划，需求分析专家", category_id=6, sort=1, rating=4.6, rating_count=89, view_count=1200, chat_count=234),
            Agent(id=10, name="通用助手", icon="🔧", description="全能帮手，解答各类问题", category_id=7, sort=1, rating=4.4, rating_count=56, view_count=670, chat_count=89),
            Agent(id=11, name="学习助手", icon="📚", description="知识学习，答疑解惑", category_id=7, sort=2, rating=4.5, rating_count=134, view_count=1560, chat_count=345),
            Agent(id=12, name="生活助手", icon="🌟", description="日常建议，提升生活质量", category_id=7, sort=3, rating=4.3, rating_count=45, view_count=450, chat_count=67),
        ]
        db.add_all(agents)
        db.commit()
    
    db.close()

init_data()

# Pydantic 模型
class RatingRequest(BaseModel):
    score: int

# API 接口
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

@app.get("/")
def root():
    return {"message": "知枢 API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)