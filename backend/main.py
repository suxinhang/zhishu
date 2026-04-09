from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
import random
import os
import httpx

app = FastAPI(title="知枢 API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./zhishu.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DeepSeek 配置 - V3.2 模型
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-dac9fe3ee5414ff5bd8bcbecd4456617")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# 数据模型
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    icon = Column(String(10))
    sort = Column(Integer, default=0)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    icon = Column(String(10))
    description = Column(String(500))
    category_id = Column(Integer)
    sort = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    chat_count = Column(Integer, default=0)
    system_prompt = Column(String(2000), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# 初始化数据
def init_data():
    db = SessionLocal()
    
    if db.query(Category).count() == 0:
        categories = [
            Category(id=1, name="写作", icon="✍️", sort=1),
            Category(id=2, name="编程", icon="💻", sort=2),
            Category(id=3, name="翻译", icon="🌐", sort=3),
            Category(id=4, name="绘画", icon="🎨", sort=4),
            Category(id=5, name="效率", icon="⚡", sort=5),
        ]
        db.add_all(categories)
        
        agents = [
            Agent(
                id=1, name="文案写作助手", icon="✍️", description="帮你写出精彩文案",
                category_id=1, rating=4.8, rating_count=128, view_count=1520, chat_count=356,
                system_prompt="你是一个专业的文案写作助手，擅长各类文案创作。"
            ),
            Agent(
                id=2, name="小说创作助手", icon="📖", description="激发灵感，创作故事",
                category_id=1, rating=4.7, rating_count=89, view_count=980, chat_count=245,
                system_prompt="你是一个小说创作助手，擅长故事构思和情节设计。"
            ),
            Agent(
                id=3, name="代码助手", icon="💻", description="高效编程，解决难题",
                category_id=2, rating=4.9, rating_count=312, view_count=4500, chat_count=1200,
                system_prompt="你是一个编程助手，精通多种编程语言，帮助用户解决技术问题。"
            ),
            Agent(
                id=4, name="多语言翻译", icon="🌐", description="精准翻译，跨越障碍",
                category_id=3, rating=4.6, rating_count=78, view_count=890, chat_count=123,
                system_prompt="你是一个翻译助手，精通多种语言，提供准确流畅的翻译。"
            ),
            Agent(
                id=5, name="AI绘画助手", icon="🎨", description="创意无限，描绘想象",
                category_id=4, rating=4.8, rating_count=198, view_count=2800, chat_count=678,
                system_prompt="你是一个AI绘画提示词助手，帮助用户生成高质量的绘画提示词。"
            ),
        ]
        db.add_all(agents)
        db.commit()
    
    db.close()

init_data()

# Pydantic 模型
class ChatRequest(BaseModel):
    message: str
    agent_id: int

# DeepSeek 对话接口
async def chat_with_deepseek(system_prompt: str, user_message: str) -> str:
    """调用 DeepSeek API 进行对话"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"抱歉，我暂时无法回答。请稍后再试。"

# API 接口
@app.get("/api/categories")
def get_categories():
    db = SessionLocal()
    cats = db.query(Category).order_by(Category.sort).all()
    db.close()
    return [{"id": c.id, "name": c.name, "icon": c.icon} for c in cats]

@app.get("/api/agents")
def get_agents(category: int = None):
    db = SessionLocal()
    query = db.query(Agent)
    if category:
        query = query.filter(Agent.category_id == category)
    agents = query.order_by(Agent.sort).all()
    
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

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: int):
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        db.close()
        return {"error": "Agent not found"}
    
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
        "chat_count": agent.chat_count,
        "system_prompt": agent.system_prompt
    }

@app.post("/api/chat")
async def chat(req: ChatRequest):
    """与智能体对话（使用 DeepSeek V3.2）"""
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == req.agent_id).first()
    if not agent:
        db.close()
        return {"error": "Agent not found"}
    
    # 在 session 关闭前获取数据
    system_prompt = agent.system_prompt or "你是一个智能助手"
    
    agent.chat_count += 1
    db.commit()
    db.close()
    
    # 调用 DeepSeek API
    response = await chat_with_deepseek(system_prompt, req.message)
    
    return {"response": response}

@app.get("/")
def root():
    return {"message": "知枢 API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)