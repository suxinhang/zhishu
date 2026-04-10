from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
import random

app = FastAPI(title="糖果梦热榜 API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./tgmeng.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据模型
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    icon = Column(String(10))
    sort = Column(Integer, default=0)

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    url = Column(String(500))
    category_id = Column(Integer)
    enabled = Column(Integer, default=1)

class HotTopic(Base):
    __tablename__ = "hot_topics"
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    url = Column(String(1000))
    source = Column(String(100))
    source_id = Column(Integer)
    category_id = Column(Integer)
    score = Column(Float, default=0)
    view_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    sugar_index = Column(Float, default=0)  # 糖果指数
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# 初始化数据
def init_data():
    db = SessionLocal()
    
    if db.query(Category).count() == 0:
        categories = [
            Category(id=1, name="综合", icon="🔥", sort=1),
            Category(id=2, name="科技", icon="💻", sort=2),
            Category(id=3, name="财经", icon="💰", sort=3),
            Category(id=4, name="娱乐", icon="🎬", sort=4),
            Category(id=5, name="游戏", icon="🎮", sort=5),
            Category(id=6, name="体育", icon="⚽", sort=6),
            Category(id=7, name="汽车", icon="🚗", sort=7),
            Category(id=8, name="民生", icon="🏠", sort=8),
        ]
        db.add_all(categories)
        
        # 数据源
        sources = [
            Source(id=1, name="微博热搜", url="weibo.com", category_id=1),
            Source(id=2, name="知乎热榜", url="zhihu.com", category_id=1),
            Source(id=3, name="抖音热点", url="douyin.com", category_id=1),
            Source(id=4, name="V2EX", url="v2ex.com", category_id=2),
            Source(id=5, name="GitHub Trending", url="github.com", category_id=2),
            Source(id=6, name="财联社", url="cls.cn", category_id=3),
            Source(id=7, name="虎扑", url="hupu.com", category_id=6),
            Source(id=8, name="猫眼电影", url="maoyan.com", category_id=4),
        ]
        db.add_all(sources)
        
        # 模拟热点数据
        topics = []
        sample_titles = [
            "OpenAI 发布 GPT-5，性能提升 10 倍",
            "特斯拉新车 Model 3 降价 20%",
            "春节档电影票房突破 100 亿",
            "英伟达股价创历史新高",
            "苹果即将发布 iPhone 16",
            "字节跳动推出新 AI 产品",
            "小米汽车 SU7 正式上市",
            "阿里云大模型降价 50%",
            "华为鸿蒙系统市场份额超 30%",
            "腾讯游戏收入创新高",
        ]
        
        for i, title in enumerate(sample_titles):
            cat_id = (i % 8) + 1
            src_id = (i % 8) + 1
            topics.append(HotTopic(
                id=i+1,
                title=title,
                url=f"https://example.com/{i+1}",
                source=sources[src_id-1].name,
                source_id=src_id,
                category_id=cat_id,
                score=random.uniform(80, 100),
                view_count=random.randint(10000, 100000),
                comment_count=random.randint(100, 5000),
                sugar_index=random.uniform(60, 100)
            ))
        db.add_all(topics)
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

@app.get("/api/sources")
def get_sources(category: int = None):
    db = SessionLocal()
    query = db.query(Source).filter(Source.enabled == 1)
    if category:
        query = query.filter(Source.category_id == category)
    sources = query.all()
    db.close()
    return [{"id": s.id, "name": s.name, "url": s.url} for s in sources]

@app.get("/api/topics")
def get_topics(category: int = None, source: int = None, sort: str = None, limit: int = 50):
    db = SessionLocal()
    query = db.query(HotTopic)
    
    if category:
        query = query.filter(HotTopic.category_id == category)
    if source:
        query = query.filter(HotTopic.source_id == source)
    
    # 排序
    if sort == "hot":
        query = query.order_by(HotTopic.view_count.desc())
    elif sort == "sugar":
        query = query.order_by(HotTopic.sugar_index.desc())
    elif sort == "new":
        query = query.order_by(HotTopic.created_at.desc())
    else:
        query = query.order_by(HotTopic.score.desc())
    
    topics = query.limit(limit).all()
    
    # 获取分类名称
    cats = {c.id: c.name for c in db.query(Category).all()}
    db.close()
    
    return [{
        "id": t.id,
        "title": t.title,
        "url": t.url,
        "source": t.source,
        "category": cats.get(t.category_id, "综合"),
        "score": round(t.score, 1),
        "view_count": t.view_count,
        "comment_count": t.comment_count,
        "sugar_index": round(t.sugar_index, 1),
        "created_at": t.created_at.isoformat() if t.created_at else None
    } for t in topics]

@app.get("/api/topics/{topic_id}")
def get_topic(topic_id: int):
    db = SessionLocal()
    topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
    if not topic:
        db.close()
        return {"error": "Topic not found"}
    
    topic.view_count += 1
    db.commit()
    
    cats = {c.id: c.name for c in db.query(Category).all()}
    db.close()
    
    return {
        "id": topic.id,
        "title": topic.title,
        "url": topic.url,
        "source": topic.source,
        "category": cats.get(topic.category_id, "综合"),
        "score": round(topic.score, 1),
        "view_count": topic.view_count,
        "comment_count": topic.comment_count,
        "sugar_index": round(topic.sugar_index, 1)
    }

@app.get("/api/search")
def search_topics(q: str, category: int = None):
    db = SessionLocal()
    query = db.query(HotTopic).filter(HotTopic.title.contains(q))
    if category:
        query = query.filter(HotTopic.category_id == category)
    topics = query.limit(20).all()
    
    cats = {c.id: c.name for c in db.query(Category).all()}
    db.close()
    
    return [{
        "id": t.id,
        "title": t.title,
        "source": t.source,
        "category": cats.get(t.category_id, "综合"),
        "sugar_index": round(t.sugar_index, 1)
    } for t in topics]

# AI 热点解读接口
@app.get("/api/topics/{topic_id}/interpret")
async def interpret_topic(topic_id: int):
    """AI 解读热点事件"""
    db = SessionLocal()
    topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
    if not topic:
        db.close()
        return {"error": "Topic not found"}
    
    title = topic.title
    source = topic.source
    db.close()
    
    # 调用 DeepSeek API 生成解读
    prompt = f"""请对以下热点事件进行深度分析，以JSON格式返回：

热点标题：{title}
数据来源：{source}

请返回以下内容（纯JSON，不要markdown包裹）：
{{
  "summary": "事件摘要（2-3句话概括核心）",
  "key_points": ["观点1", "观点2", "观点3"],
  "impact": "影响分析（趋势预测和社会影响）",
  "related_topics": ["相关话题1", "相关话题2"]
}}
"""
    
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer sk-dac9fe3ee5414ff5bd8bcbecd4456617",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # 尝试解析 JSON
                import json
                try:
                    # 清理可能的 markdown 包裹
                    if content.startswith("```"):
                        content = content.split("```")[1]
                        if content.startswith("json"):
                            content = content[4:]
                    result = json.loads(content.strip())
                except:
                    # 如果解析失败，返回原始内容
                    result = {
                        "summary": content,
                        "key_points": [],
                        "impact": "",
                        "related_topics": []
                    }
                
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "API 调用失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def root():
    return {"message": "糖果梦热榜 API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)