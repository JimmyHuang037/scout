#!/bin/bash

# 带身份验证的API测试脚本
# 该脚本专门用于测试需要身份验证的API端点

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$SCRIPT_DIR"
PROJECT_DIR="$SCRIPT_DIR/.."
DB_DIR="$PROJECT_DIR/db"

# 恢复数据库
echo "正在恢复数据库..."
cd "$DB_DIR"

# 查找最新的备份文件
BACKUP_FILE=$(ls -t backup/school_management_backup_*.sql | head -n1)
if [ -z "$BACKUP_FILE" ]; then
    echo "未找到数据库备份文件"
    exit 1
fi

BACKUP_FILENAME=$(basename "$BACKUP_FILE")
echo "使用备份文件: $BACKUP_FILENAME"

# 运行数据库恢复脚本，恢复测试数据库
echo "y" | ./restore_db.sh "$BACKUP_FILENAME" school_management > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "数据库恢复失败"
    exit 1
fi
echo "数据库恢复成功!"

# 启动API服务器 (在后台运行)
echo "启动API服务器..."
cd "$API_DIR"
# 确保日志目录存在，在api/runtime/logs下
mkdir -p "$API_DIR/runtime/logs"
# 启动服务器并将日志写入正确的路径，使用端口5000
python -m flask --app app/factory:create_app run --port 5000 > "$API_DIR/runtime/logs/test_server.log" 2>&1 &
SERVER_PID=$!

# 等待服务器启动
sleep 3

# 检查服务器是否启动成功
if ! curl -s http://localhost:5000/api/health > /dev/null; then
    echo "API服务器启动失败，请检查日志文件: runtime/logs/test_server.log"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "API服务器启动成功!"

# 登录并保存cookie (使用教师账户)
echo "登录并保存会话..."
curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "T0101", "password": "teacher_password"}' \
  -c /tmp/test_cookie.txt > /dev/null

# 测试需要身份验证的端点
echo "=== 测试需要身份验证的端点 ==="

echo "1. 获取学生列表"
curl -s http://localhost:5000/api/admin/students \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "2. 创建学生"
curl -s -X POST http://localhost:5000/api/admin/students \
  -H "Content-Type: application/json" \
  -d '{"student_id": "S9999", "student_name": "Test Student", "class_id": 1, "password": "password123"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "3. 获取特定学生"
curl -s http://localhost:5000/api/admin/students/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "4. 更新学生信息"
curl -s -X PUT http://localhost:5000/api/admin/students/1 \
  -H "Content-Type: application/json" \
  -d '{"student_name": "Updated Student Name"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "5. 删除学生"
curl -s -X DELETE http://localhost:5000/api/admin/students/S9999 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "6. 获取教师列表"
curl -s http://localhost:5000/api/admin/teachers \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "7. 创建教师"
curl -s -X POST http://localhost:5000/api/admin/teachers \
  -H "Content-Type: application/json" \
  -d '{"teacher_id": "T9999", "teacher_name": "Test Teacher", "password": "password123"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "8. 获取特定教师"
curl -s http://localhost:5000/api/admin/teachers/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "9. 更新教师信息"
curl -s -X PUT http://localhost:5000/api/admin/teachers/1 \
  -H "Content-Type: application/json" \
  -d '{"teacher_name": "Updated Teacher Name"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "10. 删除教师"
curl -s -X DELETE http://localhost:5000/api/admin/teachers/T9999 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "11. 获取班级列表"
curl -s http://localhost:5000/api/admin/classes \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "12. 创建班级"
curl -s -X POST http://localhost:5000/api/admin/classes \
  -H "Content-Type: application/json" \
  -d '{"class_name": "Test Class"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "13. 获取特定班级"
curl -s http://localhost:5000/api/admin/classes/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "14. 更新班级信息"
curl -s -X PUT http://localhost:5000/api/admin/classes/1 \
  -H "Content-Type: application/json" \
  -d '{"class_name": "Updated Class Name"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "15. 删除班级"
curl -s -X DELETE http://localhost:5000/api/admin/classes/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "16. 获取科目列表(管理员)"
curl -s http://localhost:5000/api/admin/subjects \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "17. 创建科目"
curl -s -X POST http://localhost:5000/api/admin/subjects \
  -H "Content-Type: application/json" \
  -d '{"subject_name": "Test Subject"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "18. 获取特定科目"
curl -s http://localhost:5000/api/admin/subjects/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "19. 更新科目信息"
curl -s -X PUT http://localhost:5000/api/admin/subjects/1 \
  -H "Content-Type: application/json" \
  -d '{"subject_name": "Updated Subject Name"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "20. 删除科目"
curl -s -X DELETE http://localhost:5000/api/admin/subjects/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "21. 获取考试类型列表(管理员)"
curl -s http://localhost:5000/api/admin/exam-types \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "22. 创建考试类型"
curl -s -X POST http://localhost:5000/api/admin/exam-types \
  -H "Content-Type: application/json" \
  -d '{"exam_type_name": "Test Exam Type"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "23. 获取特定考试类型"
curl -s http://localhost:5000/api/admin/exam-types/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "24. 更新考试类型"
curl -s -X PUT http://localhost:5000/api/admin/exam-types/1 \
  -H "Content-Type: application/json" \
  -d '{"type_name": "Updated Exam Type"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "25. 删除考试类型"
curl -s -X DELETE http://localhost:5000/api/admin/exam-types/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "26. 获取教师班级关系列表"
curl -s http://localhost:5000/api/admin/teacher-classes \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "27. 创建教师班级关系"
curl -s -X POST http://localhost:5000/api/admin/teacher-classes \
  -H "Content-Type: application/json" \
  -d '{"teacher_id": 2, "class_id": 2}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "28. 获取特定教师班级关系"
curl -s http://localhost:5000/api/admin/teacher-classes/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "29. 更新教师班级关系"
curl -s -X PUT http://localhost:5000/api/admin/teacher-classes/1 \
  -H "Content-Type: application/json" \
  -d '{"class_id": 6, "new_teacher_id": 1, "new_class_id": 2}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "30. 删除教师班级关系"
curl -s -X DELETE http://localhost:5000/api/admin/teacher-classes/1 \
  -H "Content-Type: application/json" \
  -d '{"class_id": 2}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "31. 获取学生成绩"
curl -s http://localhost:5000/api/student/scores \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "32. 获取教师管理的学生列表"
curl -s http://localhost:5000/api/teacher/students \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "33. 获取考试列表"
curl -s http://localhost:5000/api/teacher/exams \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "34. 创建考试"
curl -s -X POST http://localhost:5000/api/teacher/exams \
  -H "Content-Type: application/json" \
  -d '{"exam_name": "Test Exam", "subject_id": 1, "class_id": 1, "exam_type_id": 1, "exam_date": "2023-01-01"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "35. 获取特定考试"
curl -s http://localhost:5000/api/teacher/exams/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "36. 更新考试信息"
curl -s -X PUT http://localhost:5000/api/teacher/exams/1 \
  -H "Content-Type: application/json" \
  -d '{"exam_name": "Updated Exam"}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "37. 删除考试"
curl -s -X DELETE http://localhost:5000/api/teacher/exams/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "38. 获取成绩列表"
curl -s http://localhost:5000/api/teacher/scores \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "39. 创建成绩"
curl -s -X POST http://localhost:5000/api/teacher/scores \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "subject_id": 1, "exam_type_id": 1, "score": 95.5}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "40. 获取特定成绩"
curl -s http://localhost:5000/api/teacher/scores/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "41. 更新成绩"
curl -s -X PUT http://localhost:5000/api/teacher/scores/1 \
  -H "Content-Type: application/json" \
  -d '{"score": 90.0}' \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "42. 删除成绩"
curl -s -X DELETE http://localhost:5000/api/teacher/scores/1 \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "43. 获取考试结果"
curl -s http://localhost:5000/api/teacher/exam/results \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "44. 获取教学表现"
curl -s http://localhost:5000/api/teacher/exam/performance \
  -b /tmp/test_cookie.txt | jq '.'

echo ""
echo "45. 获取考试班级"
curl -s http://localhost:5000/api/teacher/exam/classes \
  -b /tmp/test_cookie.txt | jq '.'

# 清理临时文件
rm -f /tmp/test_cookie.txt

# 关闭API服务器
echo ""
echo "关闭API服务器..."
kill $SERVER_PID

echo "带身份验证的API测试完成!"