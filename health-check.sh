#!/bin/bash
# 知枢网站健康检查脚本
# 用于监控服务是否在线

# 服务配置
SERVICES=(
    "8000:后端服务:/api/categories"
    "9000:热榜API:/weibo"
    "3000:前端服务:/"
)

ALERT_FILE="/tmp/zhishu-health-alert"

echo "========================================="
echo "知枢网站健康检查"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="

FAILED=0

for service in "${SERVICES[@]}"; do
    IFS=':' read -r port name endpoint <<< "$service"
    
    # 检查端口
    if netstat -tlnp 2>/dev/null | grep -q ":$port " || ss -tlnp 2>/dev/null | grep -q ":$port "; then
        # 检查HTTP响应
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port$endpoint" 2>/dev/null || echo "000")
        
        if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
            echo "✅ $name: 健康 (HTTP $HTTP_CODE)"
        else
            echo "⚠️  $name: 端口开放但HTTP异常 (HTTP $HTTP_CODE)"
            FAILED=1
        fi
    else
        echo "❌ $name: 离线"
        FAILED=1
    fi
done

# 检查Nginx
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx: 运行中"
else
    echo "❌ Nginx: 未运行"
    FAILED=1
fi

echo "========================================="

if [ $FAILED -eq 1 ]; then
    echo "⚠️  服务异常，需要重启"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 服务异常" > $ALERT_FILE
    exit 1
else
    echo "✅ 所有服务正常"
    rm -f $ALERT_FILE
    exit 0
fi