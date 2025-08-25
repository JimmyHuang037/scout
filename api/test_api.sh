#!/bin/bash

# API测试脚本
# 该脚本用于测试所有API端点，包括需要身份验证和不需要身份验证的端点

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$SCRIPT_DIR"

# 设置Python警告过滤
PYTHONWARNINGS="ignore:Unverified HTTPS request"

# 启动API服务器 (在后台运行)
echo "启动API服务器..."
cd "$API_DIR"
python -W ignore::Warning -m flask --app app/factory:create_app run --port 5001 > ../runtime/logs/test_server.log 2>&1 &
SERVER_PID=$!

# 等待服务器启动
sleep 3

# 检查服务器是否启动成功
if ! curl -s http://localhost:5001/api/health > /dev/null; then
    echo "API服务器启动失败，请检查日志文件: ../runtime/logs/test_server.log"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "API服务器启动成功!"

# 测试不需要身份验证的端点
echo "=== 测试不需要身份验证的端点 ==="

echo "1. 测试健康检查端点"
curl -s http://localhost:5001/api/health | jq '.'

echo ""
echo "2. 测试获取科目列表"
curl -s http://localhost:5001/api/subjects | jq '.'

echo ""
echo "3. 测试获取考试类型列表"
curl -s http://localhost:5001/api/exam-types | jq '.'

echo ""
echo "4. 测试用户登录"
curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "admin", "password": "admin"}' | jq '.'

# 测试需要身份验证的端点
echo ""
echo "=== 测试需要身份验证的端点 ==="

# 先登录并保存cookie
echo "5. 登录并保存会话"
curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "admin", "password": "admin"}' \
  -c /tmp/test_cookie.txt > /dev/null

echo "6. 使用会话获取学生列表"
curl -s http://localhost:5001/api/admin/students \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "7. 使用会话获取教师列表"
curl -s http://localhost:5001/api/admin/teachers \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "8. 使用会话获取班级列表"
curl -s http://localhost:5001/api/admin/classes \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "9. 使用会话获取科目列表(管理员)"
curl -s http://localhost:5001/api/admin/subjects \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "10. 使用会话获取考试类型列表(管理员)"
curl -s http://localhost:5001/api/admin/exam-types \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "11. 使用会话获取教师班级关系列表"
curl -s http://localhost:5001/api/admin/teacher-classes \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "12. 使用会话获取学生成绩"
curl -s http://localhost:5001/api/student/scores \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "13. 使用会话获取教师管理的学生列表"
curl -s http://localhost:5001/api/teacher/students \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "14. 使用会话获取考试列表"
curl -s http://localhost:5001/api/teacher/exams \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "15. 使用会话获取成绩列表"
curl -s http://localhost:5001/api/teacher/scores \
  -b /tmp/test_cookie.txt | jq '.'

# 清理临时文件
rm -f /tmp/test_cookie.txt

# 关闭API服务器
echo ""
echo "关闭API服务器..."
kill $SERVER_PID

echo "API测试完成!"