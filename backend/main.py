from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
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
            Agent(id=1, name="情感陪伴助手", icon="❤️", description="温暖陪伴，倾听你的心事", category_id=1, sort=1),
            Agent(id=2, name="心理咨询助手", icon="🧠", description="专业心理支持，帮你排解困扰", category_id=1, sort=2),
            Agent(id=3, name="文案写作助手", icon="✏️", description="写出打动人心的文案", category_id=2, sort=1),
            Agent(id=4, name="小说创作助手", icon="📖", description="激发灵感，创作精彩故事", category_id=2, sort=2),
            Agent(id=5, name="多语言翻译助手", icon="🌐", description="精准翻译，跨越语言障碍", category_id=3, sort=1),
            Agent(id=6, name="AI绘画助手", icon="🎨", description="创意无限，描绘你的想象", category_id=4, sort=1),
            Agent(id=7, name="代码助手", icon="💻", description="高效编程，解决技术难题", category_id=5, sort=1),
            Agent(id=8, name="Debug助手", icon="🔍", description="快速定位问题，优化代码", category_id=5, sort=2),
            Agent(id=9, name="产品经理助手", icon="📊", description="产品规划，需求分析专家", category_id=6, sort=1),
            Agent(id=10, name="通用助手", icon="🔧", description="全能帮手，解答各类问题", category_id=7, sort=1),
            Agent(id=11, name="学习助手", icon="📚", description="知识学习，答疑解惑", category_id=7, sort=2),
            Agent(id=12, name="生活助手", icon="🌟", description="日常建议，提升生活质量", category_id=7, sort=3),
        ]
        db.add_all(agents)
        db.commit()
    
    db.close()

init_data()

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
    query = db.query(Agent).order_by(Agent.sort)
    if category:
        query = query.filter(Agent.category_id == category)
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
        "category_name": cats.get(a.category_id, "其他")
    } for a in agents]

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: int):
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        db.close()
        return {"error": "Agent not found"}
    
    cat = db.query(Category).filter(Category.id == agent.category_id).first()
    db.close()
    
    return {
        "id": agent.id,
        "name": agent.name,
        "icon": agent.icon,
        "description": agent.description,
        "category_id": agent.category_id,
        "category_name": cat.name if cat else "其他"
    }

@app.get("/")
def root():
    return {"message": "知枢 API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)