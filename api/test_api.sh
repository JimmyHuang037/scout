#!/bin/bash

# API测试脚本
# 功能：恢复测试数据库并测试API端点

echo "=============================="
echo "API功能测试脚本"
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

# 测试API端点
echo ""
echo "3. 测试API端点..."
echo "=============================="

# 测试管理员API端点
echo ""
echo "3.1 测试管理员API端点"
echo "------------------------"

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

# 测试教师API端点
echo ""
echo "3.2 测试教师API端点"
echo "------------------------"

# 测试获取成绩
echo "测试: 获取所有成绩"
echo "命令: curl -s -X GET 'http://localhost:5000/api/teacher/scores' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/teacher/scores' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取考试结果
echo "测试: 获取考试结果"
echo "命令: curl -s -X GET 'http://localhost:5000/api/teacher/exam/results' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/teacher/exam/results' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试获取教学表现
echo "测试: 获取教学表现"
echo "命令: curl -s -X GET 'http://localhost:5000/api/teacher/exam/performance' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/teacher/exam/performance' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 测试学生API端点
echo ""
echo "3.3 测试学生API端点"
echo "------------------------"

# 测试获取成绩
echo "测试: 获取学生成绩"
echo "命令: curl -s -X GET 'http://localhost:5000/api/student/scores' | jq '.'"
curl -s -X GET 'http://localhost:5000/api/student/scores' | jq '.'
echo ""
echo "------------------------------------------------------------"

# 关闭API服务器
echo ""
echo "4. 清理..."
echo "=============================="
kill $API_PID
echo "API服务器已关闭"

echo ""
echo "API测试完成！"