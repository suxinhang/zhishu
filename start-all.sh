#!/bin/bash
# 知枢网站完整启动脚本
# 确保所有服务7x24小时在线

set -e

echo "========================================="
echo "知枢网站服务启动脚本"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="

# 项目目录
PROJECT_DIR="/root/.openclaw/workspace/website-project"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR/backend"
HOTAPI_DIR="/root/.openclaw/workspace/DailyHotApi"

# 日志目录
LOG_DIR="/var/log/zhishu"
mkdir -p $LOG_DIR

# 检查端口是否被占用
check_port() {
    local port=$1
    if netstat -tlnp 2>/dev/null | grep -q ":$port " || ss -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "⚠️  端口 $port 已被占用，跳过..."
        return 1
    fi
    return 0
}

# 杀掉旧进程
kill_old_process() {
    local port=$1
    local name=$2
    local pid=$(netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1)
    if [ -n "$pid" ] && [ "$pid" != "-" ]; then
        echo "🔄 停止旧的 $name 进程 (PID: $pid)..."
        kill -9 $pid 2>/dev/null || true
        sleep 1
    fi
}

# =========================================
# 1. 后端服务 (FastAPI - 8000)
# =========================================
echo ""
echo "📦 启动后端服务 (FastAPI)..."
kill_old_process 8000 "后端"
cd $BACKEND_DIR
if [ ! -d "venv" ]; then
    echo "❌ 后端虚拟环境不存在，请先初始化"
    exit 1
fi
./venv/bin/python main.py > $LOG_DIR/backend.log 2>&1 &
echo "✅ 后端服务启动 (端口: 8000)"
sleep 2

# =========================================
# 2. 热榜API服务 (DailyHotApi - 9000)
# =========================================
echo ""
echo "📦 启动热榜API服务 (DailyHotApi)..."
kill_old_process 9000 "热榜API"
cd $HOTAPI_DIR
if [ ! -d "node_modules" ]; then
    echo "❌ 热榜API依赖未安装，请先运行 npm install"
    exit 1
fi
npm start > $LOG_DIR/hotapi.log 2>&1 &
echo "✅ 热榜API启动 (端口: 9000)"
sleep 2

# =========================================
# 3. 前端服务 (Vite - 3000)
# =========================================
echo ""
echo "📦 启动前端服务 (Vite)..."
kill_old_process 3000 "前端"
cd $FRONTEND_DIR
if [ ! -d "node_modules" ]; then
    echo "❌ 前端依赖未安装，请先运行 npm install"
    exit 1
fi
npm run dev > $LOG_DIR/frontend.log 2>&1 &
echo "✅ 前端服务启动 (端口: 3000)"
sleep 2

# =========================================
# 4. 检查服务状态
# =========================================
echo ""
echo "========================================="
echo "🔍 服务状态检查..."
echo "========================================="

check_service() {
    local port=$1
    local name=$2
    if netstat -tlnp 2>/dev/null | grep -q ":$port " || ss -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "✅ $name: 运行中 (端口 $port)"
        return 0
    else
        echo "❌ $name: 未启动 (端口 $port)"
        return 1
    fi
}

FAILED=0
check_service 8000 "后端服务" || FAILED=1
check_service 9000 "热榜API" || FAILED=1
check_service 3000 "前端服务" || FAILED=1

# =========================================
# 5. Nginx状态
# =========================================
echo ""
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx: 运行中 (端口 8080)"
else
    echo "⚠️  Nginx: 未运行"
    systemctl start nginx 2>/dev/null && echo "✅ Nginx 已启动" || echo "❌ Nginx 启动失败"
fi

# =========================================
# 6. 访问地址
# =========================================
echo ""
echo "========================================="
echo "🌐 访问地址"
echo "========================================="
echo "主站:      http://82.156.81.117:8080/"
echo "智能体:    http://82.156.81.117:8080/agents"
echo "热榜:      http://82.156.81.117:8080/tgmeng"
echo "API文档:   http://82.156.81.117:8080/docs"
echo ""
echo "日志目录: $LOG_DIR"
echo "========================================="

if [ $FAILED -eq 1 ]; then
    echo "⚠️  部分服务启动失败，请检查日志"
    exit 1
else
    echo "✅ 所有服务启动成功！"
    exit 0
fi