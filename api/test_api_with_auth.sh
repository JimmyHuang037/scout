#!/bin/bash

# API测试脚本（带认证）
# 功能：恢复测试数据库，进行用户认证，然后测试需要认证的API端点

echo "=============================="
echo "API功能测试脚本（带认证）"
echo "=============================="

# 进入项目根目录
cd /home/jimmy/repo/scout

# 恢复测试数据库
echo ""
echo "1. 恢复测试数据库..."
echo "=============================="
echo "执行命令: ./db/restore_db.sh school_management_backup_20250825_220152.sql school_management_test"
./db/restore_db.sh school_management_backup_20250825_220152.sql school_management_test << EOF
y
EOF

if [ $? -ne 0 ]; then
    echo "数据库恢复失败，退出测试"
    exit 1
fi

# 启动API服务器（后台运行）
echo ""
echo "2. 启动API服务器..."
echo "=============================="
echo "执行命令: cd api && python app.py"
cd api
python app.py > /dev/null 2>&1 & 
API_PID=$!
echo "API服务器已在后台启动，PID: $API_PID"

# 等待服务器启动
sleep 5

# 测试不需要认证的API端点
echo ""
echo "3. 测试不需要认证的API端点..."
echo "=============================="

# 测试获取所有学生
echo "测试: 获取所有学生"
echo "命令: curl -s -X GET 'http://localhost:5000/api/admin/students' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/admin/students' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取所有教师
echo "测试: 获取所有教师"
echo "命令: curl -s -X GET 'http://localhost:5000/api/admin/teachers' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/admin/teachers' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取所有班级
echo "测试: 获取所有班级"
echo "命令: curl -s -X GET 'http://localhost:5000/api/admin/classes' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/admin/classes' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取所有科目
echo "测试: 获取所有科目"
echo "命令: curl -s -X GET 'http://localhost:5000/api/admin/subjects' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/admin/subjects' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取所有考试类型
echo "测试: 获取所有考试类型"
echo "命令: curl -s -X GET 'http://localhost:5000/api/admin/exam-types' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/admin/exam-types' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 学生认证测试
echo ""
echo "4. 学生认证测试..."
echo "=============================="

# 创建Cookie jar用于存储会话
COOKIE_JAR=$(mktemp)

# 学生登录 (使用学生ID S0101，密码pass123)
echo "学生登录测试 (学生ID: S0101)"
echo "命令: curl -s -X POST 'http://localhost:5000/api/auth/login' -H 'Content-Type: application/json' -d '{\"user_id\": \"S0101\", \"password\": \"pass123\"}' -c $COOKIE_JAR"
curl -s -X POST 'http://localhost:5000/api/auth/login' -H 'Content-Type: application/json' -d '{"user_id": "S0101", "password": "pass123"}' -c $COOKIE_JAR
echo ""
echo "------------------------------------------------------------"

# 使用认证信息测试学生API端点
echo ""
echo "5. 测试需要学生认证的API端点..."
echo "=============================="

# 测试获取学生成绩
echo "测试: 获取学生成绩"
echo "命令: curl -s -X GET 'http://localhost:5000/api/student/scores' -b $COOKIE_JAR | jq '.'"
curl -s -X GET 'http://localhost:5000/api/student/scores' -b $COOKIE_JAR | jq '.'
echo ""
echo "------------------------------------------------------------"

# 教师认证测试
echo ""
echo "6. 教师认证测试..."
echo "=============================="

# 教师登录 (使用教师ID 1，密码test123)
echo "教师登录测试 (教师ID: 1)"
echo "命令: curl -s -X POST 'http://localhost:5000/api/auth/login' -H 'Content-Type: application/json' -d '{\"user_id\": \"1\", \"password\": \"test123\"}' -c $COOKIE_JAR"
curl -s -X POST 'http://localhost:5000/api/auth/login' -H 'Content-Type: application/json' -d '{"user_id": "1", "password": "test123"}' -c $COOKIE_JAR
echo ""
echo "------------------------------------------------------------"

# 使用认证信息测试教师API端点
echo ""
echo "7. 测试需要教师认证的API端点..."
echo "=============================="

# 测试获取教师成绩
echo "测试: 获取教师成绩"
echo "命令: curl -s -X GET 'http://localhost:5000/api/teacher/scores' -b $COOKIE_JAR | jq '.'"
curl -s -X GET 'http://localhost:5000/api/teacher/scores' -b $COOKIE_JAR | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取考试结果
echo "测试: 获取考试结果"
echo "命令: curl -s -X GET 'http://localhost:5000/api/teacher/exam/results' -b $COOKIE_JAR | jq '.'"
curl -s -X GET 'http://localhost:5000/api/teacher/exam/results' -b $COOKIE_JAR | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取教学表现
echo "测试: 获取教学表现"
echo "命令: curl -s -X GET 'http://localhost:5000/api/teacher/exam/performance' -b $COOKIE_JAR | jq '.'"
curl -s -X GET 'http://localhost:5000/api/teacher/exam/performance' -b $COOKIE_JAR | jq '.'
echo ""
echo "------------------------------------------------------------"

# 清理Cookie jar
rm -f $COOKIE_JAR

# 关闭API服务器
echo ""
echo "8. 清理..."
echo "=============================="
kill $API_PID
echo "API服务器已关闭"

echo ""
echo "API测试完成！"