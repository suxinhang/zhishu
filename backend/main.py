from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
import random
import os
import httpx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

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
    
    # 初始化分类
    if db.query(Category).count() == 0:
        categories = [
            Category(id=1, name="写作", icon="✍️", sort=1),
            Category(id=2, name="编程", icon="💻", sort=2),
            Category(id=3, name="翻译", icon="🌐", sort=3),
            Category(id=4, name="绘画", icon="🎨", sort=4),
            Category(id=5, name="效率", icon="⚡", sort=5),
        ]
        db.add_all(categories)
        db.commit()
    
    # 初始化智能体
    if db.query(Agent).count() == 0:
        
        agents = [
            # 写作类 (5个)
            Agent(
                id=1, name="文案写作助手", icon="✍️", description="帮你写出精彩文案，适用于广告、营销、社交媒体",
                category_id=1, rating=4.8, rating_count=128, view_count=1520, chat_count=356,
                system_prompt="你是一个专业的文案写作助手，擅长各类文案创作，包括广告文案、营销文案、社交媒体文案等。"
            ),
            Agent(
                id=2, name="小说创作助手", icon="📖", description="激发灵感，构思情节，创作故事",
                category_id=1, rating=4.7, rating_count=89, view_count=980, chat_count=245,
                system_prompt="你是一个小说创作助手，擅长故事构思、情节设计、人物塑造，帮助作者创作精彩的小说。"
            ),
            Agent(
                id=6, name="诗歌创作助手", icon="🌸", description="用文字编织诗意，创作古今诗词",
                category_id=1, rating=4.5, rating_count=56, view_count=620, chat_count=178,
                system_prompt="你是一个诗歌创作助手，擅长创作现代诗、古体诗、词牌等，富有文学素养。"
            ),
            Agent(
                id=7, name="日记写作助手", icon="📝", description="帮你记录生活，表达情感",
                category_id=1, rating=4.6, rating_count=42, view_count=380, chat_count=156,
                system_prompt="你是一个日记写作助手，帮助用户记录日常生活、表达情感、反思成长。"
            ),
            Agent(
                id=8, name="周报生成器", icon="📊", description="自动生成工作周报，高效汇报",
                category_id=1, rating=4.9, rating_count=234, view_count=3200, chat_count=890,
                system_prompt="你是一个周报生成助手，根据用户提供的工作内容，自动生成结构清晰的工作周报。"
            ),
            
            # 编程类 (6个)
            Agent(
                id=3, name="代码助手", icon="💻", description="高效编程，解决难题，多语言支持",
                category_id=2, rating=4.9, rating_count=312, view_count=4500, chat_count=1200,
                system_prompt="你是一个编程助手，精通Python、JavaScript、Java、Go等多种编程语言，帮助用户解决技术问题。"
            ),
            Agent(
                id=9, name="Python专家", icon="🐍", description="Python编程专家，数据分析与机器学习",
                category_id=2, rating=4.8, rating_count=156, view_count=2800, chat_count=620,
                system_prompt="你是Python编程专家，精通数据分析、机器学习、Web开发等领域。"
            ),
            Agent(
                id=10, name="前端开发助手", icon="🎨", description="Vue/React/Angular，前端全栈",
                category_id=2, rating=4.7, rating_count=98, view_count=1900, chat_count=420,
                system_prompt="你是前端开发助手，精通Vue、React、Angular等框架，帮助用户解决前端开发问题。"
            ),
            Agent(
                id=11, name="SQL优化助手", icon="🗃️", description="SQL语句优化，数据库性能提升",
                category_id=2, rating=4.6, rating_count=67, view_count=890, chat_count=234,
                system_prompt="你是SQL优化专家，帮助用户优化SQL语句，提升数据库性能。"
            ),
            Agent(
                id=12, name="算法解题助手", icon="🧮", description="算法面试题解答，LeetCode刷题",
                category_id=2, rating=4.9, rating_count=289, view_count=5600, chat_count=1560,
                system_prompt="你是算法解题助手，擅长解答LeetCode等各类算法面试题，提供详细思路和代码实现。"
            ),
            Agent(
                id=13, name="Git版本控制助手", icon="🔀", description="Git操作指导，版本管理专家",
                category_id=2, rating=4.5, rating_count=45, view_count=560, chat_count=189,
                system_prompt="你是Git版本控制助手，帮助用户解决Git操作、分支管理、冲突解决等问题。"
            ),
            
            # 翻译类 (4个)
            Agent(
                id=4, name="多语言翻译", icon="🌐", description="精准翻译，支持50+语言",
                category_id=3, rating=4.6, rating_count=78, view_count=890, chat_count=123,
                system_prompt="你是一个翻译助手，精通50+语言，提供准确流畅的翻译服务。"
            ),
            Agent(
                id=14, name="英译中助手", icon="🇬🇧", description="专业英译中，地道表达",
                category_id=3, rating=4.7, rating_count=89, view_count=1200, chat_count=345,
                system_prompt="你是英译中翻译专家，将英文翻译成地道、流畅的中文。"
            ),
            Agent(
                id=15, name="日译中助手", icon="🇯🇵", description="日语翻译中文，动漫游戏专用",
                category_id=3, rating=4.5, rating_count=56, view_count=680, chat_count=210,
                system_prompt="你是日译中翻译专家，擅长动漫、游戏、文学等领域的日语翻译。"
            ),
            Agent(
                id=16, name="商务翻译助手", icon="💼", description="商务文档翻译，专业术语",
                category_id=3, rating=4.8, rating_count=134, view_count=2200, chat_count=678,
                system_prompt="你是商务翻译专家，擅长商务文档、合同、报告等专业翻译。"
            ),
            
            # 绘画类 (5个)
            Agent(
                id=5, name="AI绘画助手", icon="🎨", description="生成Midjourney/Stable Diffusion提示词",
                category_id=4, rating=4.8, rating_count=198, view_count=2800, chat_count=678,
                system_prompt="你是AI绘画提示词助手，帮助用户生成高质量的Midjourney、Stable Diffusion提示词。"
            ),
            Agent(
                id=17, name="Logo设计助手", icon="🎯", description="Logo创意设计，品牌视觉",
                category_id=4, rating=4.6, rating_count=78, view_count=980, chat_count=290,
                system_prompt="你是Logo设计助手，帮助用户构思Logo创意，提供设计建议。"
            ),
            Agent(
                id=18, name="UI设计助手", icon="📱", description="UI界面设计，用户体验优化",
                category_id=4, rating=4.7, rating_count=112, view_count=1800, chat_count=450,
                system_prompt="你是UI设计助手，帮助用户优化界面设计，提升用户体验。"
            ),
            Agent(
                id=19, name="配色方案助手", icon="🌈", description="色彩搭配建议，视觉美学",
                category_id=4, rating=4.5, rating_count=56, view_count=720, chat_count=210,
                system_prompt="你是配色方案助手，帮助用户选择合适的色彩搭配，提升视觉效果。"
            ),
            Agent(
                id=20, name="海报设计助手", icon="🖼️", description="海报创意设计，活动宣传",
                category_id=4, rating=4.6, rating_count=89, view_count=1100, chat_count=340,
                system_prompt="你是海报设计助手，帮助用户构思海报创意，提供设计建议。"
            ),
            
            # 效率类 (7个)
            Agent(
                id=21, name="日程规划助手", icon="📅", description="智能日程安排，时间管理",
                category_id=5, rating=4.7, rating_count=156, view_count=2400, chat_count=780,
                system_prompt="你是日程规划助手，帮助用户合理安排时间，提升工作效率。"
            ),
            Agent(
                id=22, name="会议纪要助手", icon="📋", description="自动生成会议纪要，高效记录",
                category_id=5, rating=4.8, rating_count=178, view_count=3200, chat_count=920,
                system_prompt="你是会议纪要助手，根据会议内容自动生成结构清晰的会议纪要。"
            ),
            Agent(
                id=23, name="邮件撰写助手", icon="📧", description="商务邮件撰写，专业表达",
                category_id=5, rating=4.6, rating_count=89, view_count=1500, chat_count=450,
                system_prompt="你是邮件撰写助手，帮助用户撰写专业、得体的商务邮件。"
            ),
            Agent(
                id=24, name="PPT大纲助手", icon="📊", description="PPT大纲生成，演示逻辑",
                category_id=5, rating=4.5, rating_count=67, view_count=893, chat_count=283,
                system_prompt="你是专业的PPT大纲助手，擅长规划演示文稿结构，提供真实可用的PPT方案。\n\n## 输出格式要求\n\n### 1. 基本信息\n- PPT主题\n- 目标受众\n- 演讲时长\n- 场景类型（汇报/培训/销售/学术等）\n\n### 2. 大纲结构（使用Markdown）\n\n**封面页**\n- 主标题（简洁有力，≤10字）\n- 副标题/日期/演讲人\n- 建议时长：1分钟\n\n**目录页**\n- 列出所有章节标题\n- 建议时长：0.5分钟\n\n**正文页**（每页格式）\n```\n**P{n} {页面标题}**（建议时长）\n- 核心要点1\n- 核心要点2\n- 核心要点3\n- 数据/案例（可选）\n- 配图建议（可选）\n```\n\n**总结页**\n- 3-5个关键结论\n- 建议时长：2分钟\n\n**致谢页**\n- 感谢语 + Q&A提示\n- 建议时长：1分钟\n\n### 3. 视觉建议\n- 配色方案（主色+辅助色）\n- 字体建议（标题字体+正文字体）\n- 配图风格\n\n### 4. 演讲技巧\n- 开场白建议\n- 过渡语模板\n- 结尾金句\n\n## 注意事项\n1. 根据场景调整页数（汇报10-15页，培训20-30页）\n2. 每页要点≤5条，保持简洁\n3. 重要页面添加「配图建议」\n4. 关键数据页面添加「数据可视化建议」\n5. 提供「一键复制」格式的完整大纲\n\n## 特殊功能\n生成大纲后，用户可以通过前端「生成PPT文件」按钮直接下载 .pptx 文件，无需手动制作。\n\n## 示例格式\n生成大纲时请按照以下 JSON 结构输出，方便前端解析生成文件：\n```json\n{\n  "topic": "PPT主题",\n  "pages": [\n    {"title": "封面", "content": ["主标题", "副标题", "日期"]},\n    {"title": "目录", "content": ["章节1", "章节2", "章节3"]},\n    {"title": "正文标题1", "content": ["要点1", "要点2", "要点3"]},\n    {"title": "总结", "content": ["结论1", "结论2"]},\n    {"title": "致谢", "content": ["感谢语", "联系方式"]}\n  ]\n}\n```"
            ),
            Agent(
                id=25, name="简历优化助手", icon="👤", description="简历润色优化，求职加分",
                category_id=5, rating=4.9, rating_count=234, view_count=4500, chat_count=1200,
                system_prompt="你是简历优化助手，帮助用户润色简历，提升求职竞争力。"
            ),
            Agent(
                id=26, name="思维导图助手", icon="🧠", description="思维导图生成，知识梳理",
                category_id=5, rating=4.4, rating_count=45, view_count=680, chat_count=190,
                system_prompt="你是思维导图助手，帮助用户梳理知识结构，生成思维导图。"
            ),
            Agent(
                id=27, name="读书笔记助手", icon="📚", description="读书笔记整理，知识沉淀",
                category_id=5, rating=4.6, rating_count=78, view_count=1100, chat_count=320,
                system_prompt="你是读书笔记助手，帮助用户整理读书笔记，提炼核心观点。"
            ),
            
            # 其他类 (3个)
            Agent(
                id=28, name="健身教练助手", icon="💪", description="健身计划定制，运动指导",
                category_id=1, rating=4.5, rating_count=89, view_count=1300, chat_count=380,
                system_prompt="你是健身教练助手，帮助用户制定健身计划，提供运动指导。"
            ),
            Agent(
                id=29, name="旅行规划助手", icon="✈️", description="旅行路线规划，景点推荐",
                category_id=5, rating=4.7, rating_count=134, view_count=2100, chat_count=620,
                system_prompt="你是旅行规划助手，帮助用户规划旅行路线，推荐景点和美食。"
            ),
            Agent(
                id=30, name="美食推荐助手", icon="🍜", description="美食推荐，菜谱分享",
                category_id=5, rating=4.6, rating_count=98, view_count=1600, chat_count=480,
                system_prompt="你是美食推荐助手，帮助用户发现美食，分享菜谱和烹饪技巧。"
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
            timeout=60.0
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

# PPT 生成请求模型
class PPTGenerateRequest(BaseModel):
    topic: str
    pages: list  # 每页包含 {title, content: [], duration}

# PPT 文件生成 API
@app.post("/api/ppt/generate")
async def generate_ppt(req: PPTGenerateRequest):
    """生成 PowerPoint 文件并返回下载"""
    try:
        prs = Presentation()
        
        # 设置幻灯片尺寸（16:9）
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        
        for i, page in enumerate(req.pages):
            # 添加幻灯片
            slide_layout = prs.slide_layouts[1]  # 标题+内容布局
            slide = prs.slides.add_slide(slide_layout)
            
            # 设置标题
            title = slide.shapes.title
            title.text = page.get("title", f"第{i+1}页")
            title.text_frame.paragraphs[0].font.size = Pt(32)
            title.text_frame.paragraphs[0].font.bold = True
            title.text_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)  # 知枢紫色
            
            # 设置内容
            body = slide.placeholders[1]
            tf = body.text_frame
            tf.clear()
            
            for j, point in enumerate(page.get("content", [])):
                p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                p.text = point
                p.font.size = Pt(18)
                p.level = 0
                p.font.color.rgb = RGBColor(51, 51, 51)
        
        # 保存文件
        filename = f"/tmp/ppt_{req.topic.replace(' ', '_')[:20]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pptx"
        prs.save(filename)
        
        return FileResponse(
            filename,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=f"{req.topic[:20]}.pptx"
        )
    except Exception as e:
        return {"error": str(e)}

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