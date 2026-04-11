#!/bin/bash
# 知枢网站停止脚本

echo "========================================="
echo "知枢网站服务停止脚本"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="

# 停止服务
stop_service() {
    local port=$1
    local name=$2
    local pid=$(netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1)
    if [ -n "$pid" ] && [ "$pid" != "-" ]; then
        echo "🛑 停止 $name (PID: $pid)..."
        kill -9 $pid 2>/dev/null && echo "✅ 已停止" || echo "❌ 停止失败"
    else
        echo "⚠️  $name 未运行"
    fi
}

stop_service 3000 "前端服务"
stop_service 8000 "后端服务"
stop_service 9000 "热榜API"

echo ""
echo "✅ 所有服务已停止"