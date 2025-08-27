#!/bin/bash

# 带身份验证的API测试脚本
# 该脚本专门用于测试需要身份验证的API端点

# 设置变量
API_BASE_URL="http://localhost:5000"
TEST_COOKIE="/tmp/test_cookie.txt"
RESULT_DIR="$API_DIR/runtime/curl_test/$(date +%Y%m%d_%H%M%S)"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$SCRIPT_DIR"
PROJECT_DIR="$SCRIPT_DIR/.."
DB_DIR="$PROJECT_DIR/db"

# 创建结果保存目录
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULT_DIR="$API_DIR/runtime/curl_test/$TIMESTAMP"
mkdir -p "$RESULT_DIR"

# 恢复数据库
echo "正在恢复数据库..."
cd "$DB_DIR"

# 使用最新的备份文件
BACKUP_FILENAME="school_management_backup_20250827_205825.sql"
echo "使用备份文件: $BACKUP_FILENAME"

# 检查备份文件是否存在
if [ ! -f "backup/$BACKUP_FILENAME" ]; then
    echo "备份文件不存在: backup/$BACKUP_FILENAME"
    exit 1
fi

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

# 登录并保存会话 (使用管理员账户)
echo "登录并保存会话..." | tee -a "$RESULT_DIR/test_results.log"
CMD0="curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"admin\", \"password\": \"admin\"}' -c /tmp/test_cookie.txt"
echo "执行命令: $CMD0" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE0=$(eval $CMD0)
echo "$RESPONSE0" | tee -a "$RESULT_DIR/test_results.log"

# 测试需要身份验证的端点
echo "=== 测试需要身份验证的端点 ===" | tee "$RESULT_DIR/test_results.log"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "1. 获取学生列表" | tee -a "$RESULT_DIR/test_results.log"
CMD1="curl -s http://localhost:5000/api/admin/students -b /tmp/test_cookie.txt"
echo "执行命令: $CMD1" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE1=$(eval $CMD1)
echo "$RESPONSE1" | jq '.' > "$RESULT_DIR/1_get_students.json" 2>/dev/null || echo "$RESPONSE1" > "$RESULT_DIR/1_get_students.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "2. 创建学生" | tee -a "$RESULT_DIR/test_results.log"
CMD2="curl -s -X POST http://localhost:5000/api/admin/students -H \"Content-Type: application/json\" -d '{\"student_id\": \"S9999\", \"student_name\": \"Test Student\", \"class_id\": 1, \"password\": \"password123\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD2" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE2=$(eval $CMD2)
echo "$RESPONSE2" | jq '.' > "$RESULT_DIR/2_create_student.json" 2>/dev/null || echo "$RESPONSE2" > "$RESULT_DIR/2_create_student.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "3. 获取特定学生" | tee -a "$RESULT_DIR/test_results.log"
CMD3="curl -s http://localhost:5000/api/admin/students/S0101 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD3" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE3=$(eval $CMD3)
echo "$RESPONSE3" | jq '.' > "$RESULT_DIR/3_get_student.json" 2>/dev/null || echo "$RESPONSE3" > "$RESULT_DIR/3_get_student.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "4. 更新学生信息" | tee -a "$RESULT_DIR/test_results.log"
CMD4="curl -s -X PUT http://localhost:5000/api/admin/students/S0101 -H \"Content-Type: application/json\" -d '{\"student_name\": \"Updated Student Name\", \"class_id\": 1, \"password\": \"password123\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD4" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE4=$(eval $CMD4)
echo "$RESPONSE4" | jq '.' > "$RESULT_DIR/4_update_student.json" 2>/dev/null || echo "$RESPONSE4" > "$RESULT_DIR/4_update_student.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "5. 删除学生" | tee -a "$RESULT_DIR/test_results.log"
CMD5="curl -s -X DELETE http://localhost:5000/api/admin/students/S9999 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD5" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE5=$(eval $CMD5)
echo "$RESPONSE5" | jq '.' > "$RESULT_DIR/5_delete_student.json" 2>/dev/null || echo "$RESPONSE5" > "$RESULT_DIR/5_delete_student.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "6. 获取教师列表" | tee -a "$RESULT_DIR/test_results.log"
CMD6="curl -s http://localhost:5000/api/admin/teachers -b /tmp/test_cookie.txt"
echo "执行命令: $CMD6" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE6=$(eval $CMD6)
echo "$RESPONSE6" | jq '.' > "$RESULT_DIR/6_get_teachers.json" 2>/dev/null || echo "$RESPONSE6" > "$RESULT_DIR/6_get_teachers.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "7. 创建教师" | tee -a "$RESULT_DIR/test_results.log"
CMD7="curl -s -X POST http://localhost:5000/api/admin/teachers -H \"Content-Type: application/json\" -d '{\"teacher_name\": \"Test Teacher\", \"teacher_id\": 999, \"subject_id\": 1, \"password\": \"password123\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD7" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE7=$(eval $CMD7)
echo "$RESPONSE7" | jq '.' > "$RESULT_DIR/7_create_teacher.json" 2>/dev/null || echo "$RESPONSE7" > "$RESULT_DIR/7_create_teacher.json"

# 添加验证响应内容
echo "$RESPONSE7" | grep -q "\"teacher_id\":" 
if [ $? -eq 0 ]; then
    echo "成功获取教师ID"
else
    echo "警告: 未在响应中找到teacher_id"
fi

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "8. 获取特定教师" | tee -a "$RESULT_DIR/test_results.log"
CMD8="curl -s http://localhost:5000/api/admin/teachers/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD8" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE8=$(eval $CMD8)
echo "$RESPONSE8" | jq '.' > "$RESULT_DIR/8_get_teacher.json" 2>/dev/null || echo "$RESPONSE8" > "$RESULT_DIR/8_get_teacher.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "9. 更新教师信息" | tee -a "$RESULT_DIR/test_results.log"
CMD9="curl -s -X PUT http://localhost:5000/api/admin/teachers/1 -H \"Content-Type: application/json\" -d '{\"teacher_name\": \"Updated Teacher Name\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD9" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE9=$(eval $CMD9)
echo "$RESPONSE9" | jq '.' > "$RESULT_DIR/9_update_teacher.json" 2>/dev/null || echo "$RESPONSE9" > "$RESULT_DIR/9_update_teacher.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "10. 删除教师" | tee -a "$RESULT_DIR/test_results.log"
CMD10="curl -s -X DELETE http://localhost:5000/api/admin/teachers/999 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD10" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE10=$(eval $CMD10)
echo "$RESPONSE10" | jq '.' > "$RESULT_DIR/10_delete_teacher.json" 2>/dev/null || echo "$RESPONSE10" > "$RESULT_DIR/10_delete_teacher.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "11. 获取班级列表" | tee -a "$RESULT_DIR/test_results.log"
CMD11="curl -s http://localhost:5000/api/admin/classes -b /tmp/test_cookie.txt"
echo "执行命令: $CMD11" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE11=$(eval $CMD11)
echo "$RESPONSE11" | jq '.' > "$RESULT_DIR/11_get_classes.json" 2>/dev/null || echo "$RESPONSE11" > "$RESULT_DIR/11_get_classes.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "12. 创建班级" | tee -a "$RESULT_DIR/test_results.log"
CMD12="curl -s -X POST http://localhost:5000/api/admin/classes -H \"Content-Type: application/json\" -d '{\"class_name\": \"Test Class\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD12" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE12=$(eval $CMD12)
echo "$RESPONSE12" | jq '.' > "$RESULT_DIR/12_create_class.json" 2>/dev/null || echo "$RESPONSE12" > "$RESULT_DIR/12_create_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "13. 获取特定班级" | tee -a "$RESULT_DIR/test_results.log"
CMD13="curl -s http://localhost:5000/api/admin/classes/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD13" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE13=$(eval $CMD13)
echo "$RESPONSE13" | jq '.' > "$RESULT_DIR/13_get_class.json" 2>/dev/null || echo "$RESPONSE13" > "$RESULT_DIR/13_get_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "14. 更新班级信息" | tee -a "$RESULT_DIR/test_results.log"
CMD14="curl -s -X PUT http://localhost:5000/api/admin/classes/1 -H \"Content-Type: application/json\" -d '{\"class_name\": \"Updated Class Name\", \"grade\": 1}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD14" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE14=$(eval $CMD14)
echo "$RESPONSE14" | jq '.' > "$RESULT_DIR/14_update_class.json" 2>/dev/null || echo "$RESPONSE14" > "$RESULT_DIR/14_update_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "15. 删除班级" | tee -a "$RESULT_DIR/test_results.log"
CMD15="curl -s -X DELETE http://localhost:5000/api/admin/classes/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD15" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE15=$(eval $CMD15)
echo "$RESPONSE15" | jq '.' > "$RESULT_DIR/15_delete_class.json" 2>/dev/null || echo "$RESPONSE15" > "$RESULT_DIR/15_delete_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "16. 获取科目列表(管理员)" | tee -a "$RESULT_DIR/test_results.log"
CMD16="curl -s http://localhost:5000/api/admin/subjects -b /tmp/test_cookie.txt"
echo "执行命令: $CMD16" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE16=$(eval $CMD16)
echo "$RESPONSE16" | jq '.' > "$RESULT_DIR/16_get_subjects.json" 2>/dev/null || echo "$RESPONSE16" > "$RESULT_DIR/16_get_subjects.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "17. 创建科目" | tee -a "$RESULT_DIR/test_results.log"
CMD17="curl -s -X POST http://localhost:5000/api/admin/subjects -H \"Content-Type: application/json\" -d '{\"subject_name\": \"Test Subject\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD17" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE17=$(eval $CMD17)
echo "$RESPONSE17" | jq '.' > "$RESULT_DIR/17_create_subject.json" 2>/dev/null || echo "$RESPONSE17" > "$RESULT_DIR/17_create_subject.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "18. 获取特定科目" | tee -a "$RESULT_DIR/test_results.log"
CMD18="curl -s http://localhost:5000/api/admin/subjects/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD18" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE18=$(eval $CMD18)
echo "$RESPONSE18" | jq '.' > "$RESULT_DIR/18_get_subject.json" 2>/dev/null || echo "$RESPONSE18" > "$RESULT_DIR/18_get_subject.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "19. 更新科目信息" | tee -a "$RESULT_DIR/test_results.log"
CMD19="curl -s -X PUT http://localhost:5000/api/admin/subjects/1 -H \"Content-Type: application/json\" -d '{\"subject_name\": \"Updated Subject Name\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD19" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE19=$(eval $CMD19)
echo "$RESPONSE19" | jq '.' > "$RESULT_DIR/19_update_subject.json" 2>/dev/null || echo "$RESPONSE19" > "$RESULT_DIR/19_update_subject.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "20. 删除科目" | tee -a "$RESULT_DIR/test_results.log"
CMD20="curl -s -X DELETE http://localhost:5000/api/admin/subjects/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD20" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE20=$(eval $CMD20)
echo "$RESPONSE20" | jq '.' > "$RESULT_DIR/20_delete_subject.json" 2>/dev/null || echo "$RESPONSE20" > "$RESULT_DIR/20_delete_subject.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "21. 获取考试类型列表(管理员)" | tee -a "$RESULT_DIR/test_results.log"
CMD21="curl -s http://localhost:5000/api/admin/exam-types -b /tmp/test_cookie.txt"
echo "执行命令: $CMD21" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE21=$(eval $CMD21)
echo "$RESPONSE21" | jq '.' > "$RESULT_DIR/21_get_exam_types.json" 2>/dev/null || echo "$RESPONSE21" > "$RESULT_DIR/21_get_exam_types.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "22. 创建考试类型" | tee -a "$RESULT_DIR/test_results.log"
CMD22="curl -s -X POST http://localhost:5000/api/admin/exam-types -H \"Content-Type: application/json\" -d '{\"exam_type_name\": \"Test Exam Type\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD22" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE22=$(eval $CMD22)
echo "$RESPONSE22" | jq '.' > "$RESULT_DIR/22_create_exam_type.json" 2>/dev/null || echo "$RESPONSE22" > "$RESULT_DIR/22_create_exam_type.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "23. 获取特定考试类型" | tee -a "$RESULT_DIR/test_results.log"
CMD23="curl -s http://localhost:5000/api/admin/exam-types/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD23" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE23=$(eval $CMD23)
echo "$RESPONSE23" | jq '.' > "$RESULT_DIR/23_get_exam_type.json" 2>/dev/null || echo "$RESPONSE23" > "$RESULT_DIR/23_get_exam_type.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "24. 更新考试类型" | tee -a "$RESULT_DIR/test_results.log"
CMD24="curl -s -X PUT http://localhost:5000/api/admin/exam-types/1 -H \"Content-Type: application/json\" -d '{\"exam_type_name\": \"Updated Exam Type\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD24" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE24=$(eval $CMD24)
echo "$RESPONSE24" | jq '.' > "$RESULT_DIR/24_update_exam_type.json" 2>/dev/null || echo "$RESPONSE24" > "$RESULT_DIR/24_update_exam_type.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "25. 删除考试类型" | tee -a "$RESULT_DIR/test_results.log"
CMD25="curl -s -X DELETE http://localhost:5000/api/admin/exam-types/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD25" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE25=$(eval $CMD25)
echo "$RESPONSE25" | jq '.' > "$RESULT_DIR/25_delete_exam_type.json" 2>/dev/null || echo "$RESPONSE25" > "$RESULT_DIR/25_delete_exam_type.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "26. 获取教师班级关系列表" | tee -a "$RESULT_DIR/test_results.log"
CMD26="curl -s http://localhost:5000/api/admin/teacher-classes -b /tmp/test_cookie.txt"
echo "执行命令: $CMD26" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE26=$(eval $CMD26)
echo "$RESPONSE26" | jq '.' > "$RESULT_DIR/26_get_teacher_classes.json" 2>/dev/null || echo "$RESPONSE26" > "$RESULT_DIR/26_get_teacher_classes.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "27. 创建教师班级关系" | tee -a "$RESULT_DIR/test_results.log"
CMD27="curl -s -X POST http://localhost:5000/api/admin/teacher-classes -H \"Content-Type: application/json\" -d '{\"teacher_id\": 1, \"class_id\": 1}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD27" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE27=$(eval $CMD27)
echo "$RESPONSE27" | jq '.' > "$RESULT_DIR/27_create_teacher_class.json" 2>/dev/null || echo "$RESPONSE27" > "$RESULT_DIR/27_create_teacher_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "28. 获取特定教师班级关系" | tee -a "$RESULT_DIR/test_results.log"
CMD28="curl -s http://localhost:5000/api/admin/teacher-classes/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD28" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE28=$(eval $CMD28)
echo "$RESPONSE28" | jq '.' > "$RESULT_DIR/28_get_teacher_class.json" 2>/dev/null || echo "$RESPONSE28" > "$RESULT_DIR/28_get_teacher_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "29. 更新教师班级关系" | tee -a "$RESULT_DIR/test_results.log"
CMD29="curl -s -X PUT http://localhost:5000/api/admin/teacher-classes/1 -H \"Content-Type: application/json\" -d '{\"teacher_id\": 2, \"class_id\": 2}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD29" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE29=$(eval $CMD29)
echo "$RESPONSE29" | jq '.' > "$RESULT_DIR/29_update_teacher_class.json" 2>/dev/null || echo "$RESPONSE29" > "$RESULT_DIR/29_update_teacher_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "30. 删除教师班级关系" | tee -a "$RESULT_DIR/test_results.log"
CMD30="curl -s -X DELETE http://localhost:5000/api/admin/teacher-classes/1 -H \"Content-Type: application/json\" -d '{\"class_id\": 2}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD30" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE30=$(eval $CMD30)
echo "$RESPONSE30" | jq '.' > "$RESULT_DIR/30_delete_teacher_class.json" 2>/dev/null || echo "$RESPONSE30" > "$RESULT_DIR/30_delete_teacher_class.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
# 登录教师账户以测试教师API
echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "登录教师账户..." | tee -a "$RESULT_DIR/test_results.log"
TEACHER_LOGIN_CMD="curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"T0101\", \"password\": \"teacher_password\"}' -c /tmp/teacher_cookie.txt"
echo "执行命令: $TEACHER_LOGIN_CMD" | tee -a "$RESULT_DIR/test_results.log"
TEACHER_LOGIN_RESPONSE=$(eval $TEACHER_LOGIN_CMD)
echo "$TEACHER_LOGIN_RESPONSE" | tee -a "$RESULT_DIR/test_results.log"

# 再次尝试使用数据库中存在的教师账户登录
echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "使用数据库中的教师账户登录..." | tee -a "$RESULT_DIR/test_results.log"
TEACHER_LOGIN_CMD2="curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"2\", \"password\": \"123456\"}' -c /tmp/teacher_cookie.txt"
echo "执行命令: $TEACHER_LOGIN_CMD2" | tee -a "$RESULT_DIR/test_results.log"
TEACHER_LOGIN_RESPONSE2=$(eval $TEACHER_LOGIN_CMD2)
echo "$TEACHER_LOGIN_RESPONSE2" | tee -a "$RESULT_DIR/test_results.log"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "31. 获取学生成绩" | tee -a "$RESULT_DIR/test_results.log"
CMD31="curl -s http://localhost:5000/api/student/scores -b /tmp/test_cookie.txt"
echo "执行命令: $CMD31" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE31=$(eval $CMD31)
echo "$RESPONSE31" | jq '.' > "$RESULT_DIR/31_get_student_scores.json" 2>/dev/null || echo "$RESPONSE31" > "$RESULT_DIR/31_get_student_scores.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "32. 获取教师管理的学生列表" | tee -a "$RESULT_DIR/test_results.log"
CMD32="curl -s http://localhost:5000/api/teacher/students -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD32" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE32=$(eval $CMD32)
echo "$RESPONSE32" | jq '.' > "$RESULT_DIR/32_get_teacher_students.json" 2>/dev/null || echo "$RESPONSE32" > "$RESULT_DIR/32_get_teacher_students.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "33. 获取考试列表" | tee -a "$RESULT_DIR/test_results.log"
CMD33="curl -s http://localhost:5000/api/teacher/exams -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD33" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE33=$(eval $CMD33)
echo "$RESPONSE33" | jq '.' > "$RESULT_DIR/33_get_exams.json" 2>/dev/null || echo "$RESPONSE33" > "$RESULT_DIR/33_get_exams.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "34. 创建考试" | tee -a "$RESULT_DIR/test_results.log"
CMD34="curl -s -X POST http://localhost:5000/api/teacher/exams -H \"Content-Type: application/json\" -d '{\"exam_name\": \"Test Exam\", \"subject_id\": 1, \"class_id\": 1, \"exam_type_id\": 1, \"exam_date\": \"2023-01-01\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD34" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE34=$(eval $CMD34)
echo "$RESPONSE34" | jq '.' > "$RESULT_DIR/34_create_exam.json" 2>/dev/null || echo "$RESPONSE34" > "$RESULT_DIR/34_create_exam.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "35. 获取特定考试" | tee -a "$RESULT_DIR/test_results.log"
CMD35="curl -s http://localhost:5000/api/teacher/exams/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD35" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE35=$(eval $CMD35)
echo "$RESPONSE35" | jq '.' > "$RESULT_DIR/35_get_exam.json" 2>/dev/null || echo "$RESPONSE35" > "$RESULT_DIR/35_get_exam.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "36. 更新考试信息" | tee -a "$RESULT_DIR/test_results.log"
CMD36="curl -s -X PUT http://localhost:5000/api/teacher/exams/1 -H \"Content-Type: application/json\" -d '{\"exam_name\": \"Updated Exam\"}' -b /tmp/test_cookie.txt"
echo "执行命令: $CMD36" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE36=$(eval $CMD36)
echo "$RESPONSE36" | jq '.' > "$RESULT_DIR/36_update_exam.json" 2>/dev/null || echo "$RESPONSE36" > "$RESULT_DIR/36_update_exam.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "37. 删除考试" | tee -a "$RESULT_DIR/test_results.log"
CMD37="curl -s -X DELETE http://localhost:5000/api/teacher/exams/1 -b /tmp/test_cookie.txt"
echo "执行命令: $CMD37" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE37=$(eval $CMD37)
echo "$RESPONSE37" | jq '.' > "$RESULT_DIR/37_delete_exam.json" 2>/dev/null || echo "$RESPONSE37" > "$RESULT_DIR/37_delete_exam.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "38. 获取成绩列表" | tee -a "$RESULT_DIR/test_results.log"
CMD38="curl -s http://localhost:5000/api/teacher/scores -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD38" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE38=$(eval $CMD38)
echo "$RESPONSE38" | jq '.' > "$RESULT_DIR/38_get_scores.json" 2>/dev/null || echo "$RESPONSE38" > "$RESULT_DIR/38_get_scores.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "39. 创建成绩" | tee -a "$RESULT_DIR/test_results.log"
CMD39="curl -s -X POST http://localhost:5000/api/teacher/scores -H \"Content-Type: application/json\" -d '{\"student_id\": \"S0101\", \"subject_id\": 1, \"exam_type_id\": 1, \"score\": 95.5}' -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD39" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE39=$(eval $CMD39)
echo "$RESPONSE39" | jq '.' > "$RESULT_DIR/39_create_score.json" 2>/dev/null || echo "$RESPONSE39" > "$RESULT_DIR/39_create_score.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "40. 获取特定成绩" | tee -a "$RESULT_DIR/test_results.log"
CMD40="curl -s http://localhost:5000/api/teacher/scores/1 -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD40" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE40=$(eval $CMD40)
echo "$RESPONSE40" | jq '.' > "$RESULT_DIR/40_get_score.json" 2>/dev/null || echo "$RESPONSE40" > "$RESULT_DIR/40_get_score.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "41. 更新成绩" | tee -a "$RESULT_DIR/test_results.log"
CMD41="curl -s -X PUT http://localhost:5000/api/teacher/scores/1 -H \"Content-Type: application/json\" -d '{\"score\": 90.0}' -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD41" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE41=$(eval $CMD41)
echo "$RESPONSE41" | jq '.' > "$RESULT_DIR/41_update_score.json" 2>/dev/null || echo "$RESPONSE41" > "$RESULT_DIR/41_update_score.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "42. 删除成绩" | tee -a "$RESULT_DIR/test_results.log"
CMD42="curl -s -X DELETE http://localhost:5000/api/teacher/scores/1 -b /tmp/teacher_cookie.txt"
echo "执行命令: $CMD42" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE42=$(eval $CMD42)
echo "$RESPONSE42" | jq '.' > "$RESULT_DIR/42_delete_score.json" 2>/dev/null || echo "$RESPONSE42" > "$RESULT_DIR/42_delete_score.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "43. 获取考试结果" | tee -a "$RESULT_DIR/test_results.log"
CMD43="curl -s http://localhost:5000/api/teacher/exam/results -b /tmp/test_cookie.txt"
echo "执行命令: $CMD43" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE43=$(eval $CMD43)
echo "$RESPONSE43" | jq '.' > "$RESULT_DIR/43_get_exam_results.json" 2>/dev/null || echo "$RESPONSE43" > "$RESULT_DIR/43_get_exam_results.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "44. 获取教学表现" | tee -a "$RESULT_DIR/test_results.log"
CMD44="curl -s http://localhost:5000/api/teacher/exam/performance -b /tmp/test_cookie.txt"
echo "执行命令: $CMD44" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE44=$(eval $CMD44)
echo "$RESPONSE44" | jq '.' > "$RESULT_DIR/44_get_teacher_performance.json" 2>/dev/null || echo "$RESPONSE44" > "$RESULT_DIR/44_get_teacher_performance.json"

echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "45. 获取考试班级" | tee -a "$RESULT_DIR/test_results.log"
CMD45="curl -s http://localhost:5000/api/teacher/exam/classes -b /tmp/test_cookie.txt"
echo "执行命令: $CMD45" | tee -a "$RESULT_DIR/test_results.log"
RESPONSE45=$(eval $CMD45)
echo "$RESPONSE45" | jq '.' > "$RESULT_DIR/45_get_exam_classes.json" 2>/dev/null || echo "$RESPONSE45" > "$RESULT_DIR/45_get_exam_classes.json"

# 清理临时文件
rm -f /tmp/test_cookie.txt

# 关闭API服务器
echo ""
echo "关闭API服务器..."
kill $SERVER_PID

echo "带身份验证的API测试完成!" | tee -a "$RESULT_DIR/test_results.log"