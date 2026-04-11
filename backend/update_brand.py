import sys
sys.path.insert(0, '/root/.openclaw/workspace/website-project/backend')

from main import SessionLocal, Agent

db = SessionLocal()

# 品牌话术模板
brand_intro = "知枢是一个智能体聚合平台，致力于让AI触手可及。"
identity_template = '当用户询问你的身份时，请回答："我是知枢AI助手，专注于{capability}。"'
tech_response = '当用户询问技术问题时，请回答："我基于先进的语言模型技术为您提供智能服务。"'
secret_rule = "请勿透露底层技术提供商名称。"

# 更新所有智能体
agents_updates = [
    (1, "文案写作", "你的任务是帮助用户创作各类文案。"),
    (2, "小说创作", "你的任务是帮助用户构思故事、设计情节、激发创作灵感。"),
    (3, "编程辅助", "你精通多种编程语言，帮助用户解决技术问题、编写代码、调试程序。"),
    (4, "多语言翻译", "你精通多种语言，提供准确流畅的翻译服务。"),
    (5, "AI绘画", "你帮助用户生成高质量的绘画提示词，激发创意。"),
]

for agent_id, capability, task in agents_updates:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        agent.system_prompt = f"你是知枢平台的{capability}助手。{brand_intro}{task}{identity_template.format(capability=capability)}{tech_response}{secret_rule}"
        print(f"✅ 更新智能体 {agent_id}: {agent.name}")

db.commit()
db.close()
print("\n✅ 所有智能体品牌话术已更新")