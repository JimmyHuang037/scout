#!/bin/bash

# 带身份验证的API测试脚本
# 该脚本专门用于测试需要身份验证的API端点

# 添加命令行参数支持
TEST_CASE_NUMBER=""
TEST_BLUEPRINT=""
if [ "$#" -eq 1 ]; then
    # 检查是否为数字（特定测试用例）
    if [[ "$1" =~ ^[0-9]+$ ]]; then
        TEST_CASE_NUMBER="$1"
    # 检查是否为蓝图名称
    elif [[ "$1" =~ ^(admin|student|teacher)$ ]]; then
        TEST_BLUEPRINT="$1"
    else
        echo "错误: 参数必须是测试用例编号(数字)或蓝图名称(admin|student|teacher)"
        echo "用法: $0 [测试用例编号|蓝图名称]"
        echo "示例: $0 5 (只运行第5个测试用例)"
        echo "示例: $0 admin (运行所有admin蓝图下的测试)"
        exit 1
    fi
fi

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
BACKUP_FILENAME="school_management_backup_20250828_230726.sql"
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

# 定义不同角色的登录函数
login_admin() {
    echo "登录管理员账户..." | tee -a "$RESULT_DIR/test_results.log"
    CMD="curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"admin\", \"password\": \"admin\"}' -c /tmp/test_cookie.txt"
    echo "执行命令: $CMD" | tee -a "$RESULT_DIR/test_results.log"
    RESPONSE=$(eval $CMD)
    echo "$RESPONSE" | tee -a "$RESULT_DIR/test_results.log"
}

login_teacher() {
    echo "登录教师账户..." | tee -a "$RESULT_DIR/test_results.log"
    # 使用默认教师账户
    CMD="curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"1\", \"password\": \"test123\"}' -c /tmp/test_cookie.txt"
    echo "执行命令: $CMD" | tee -a "$RESULT_DIR/test_results.log"
    RESPONSE=$(eval $CMD)
    echo "$RESPONSE" | tee -a "$RESULT_DIR/test_results.log"
}

login_student() {
    echo "登录学生账户..." | tee -a "$RESULT_DIR/test_results.log"
    # 使用默认学生账户
    CMD="curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"S0101\", \"password\": \"pass123\"}' -c /tmp/test_cookie.txt"
    echo "执行命令: $CMD" | tee -a "$RESULT_DIR/test_results.log"
    RESPONSE=$(eval $CMD)
    echo "$RESPONSE" | tee -a "$RESULT_DIR/test_results.log"
}

# 测试需要身份验证的端点
echo "=== 测试需要身份验证的端点 ===" | tee "$RESULT_DIR/test_results.log"

# 定义测试用例执行函数
run_test_case() {
    local case_number=$1
    local case_description=$2
    local case_command=$3
    local output_file=$4
    local blueprint_type=$5
    
    # 如果指定了测试用例编号，则只运行指定的测试用例
    if [ -n "$TEST_CASE_NUMBER" ] && [ "$TEST_CASE_NUMBER" -ne "$case_number" ]; then
        return
    fi
    
    # 如果指定了蓝图类型，则只运行该蓝图下的测试用例
    if [ -n "$TEST_BLUEPRINT" ] && [ "$TEST_BLUEPRINT" != "$blueprint_type" ]; then
        return
    fi
    
    # 根据蓝图类型登录对应角色
    case "$blueprint_type" in
        "admin")
            login_admin
            ;;
        "teacher")
            login_teacher
            ;;
        "student")
            login_student
            ;;
    esac
    
    echo "" | tee -a "$RESULT_DIR/test_results.log"
    echo "$case_number. $case_description" | tee -a "$RESULT_DIR/test_results.log"
    echo "执行命令: $case_command" | tee -a "$RESULT_DIR/test_results.log"
    RESPONSE=$(eval $case_command)
    echo "$RESPONSE" | jq '.' > "$RESULT_DIR/${output_file}" 2>/dev/null || echo "$RESPONSE" > "$RESULT_DIR/${output_file}"
}

# 测试用例列表
run_test_case 1 "获取学生列表" \
    "curl -s http://localhost:5000/api/admin/students -b /tmp/test_cookie.txt" \
    "1_get_students.json" "admin"

run_test_case 2 "创建学生" \
    "curl -s -X POST http://localhost:5000/api/admin/students -H \"Content-Type: application/json\" -d '{\"student_id\": \"S9999\", \"student_name\": \"Test Student\", \"class_id\": 1, \"password\": \"password123\"}' -b /tmp/test_cookie.txt" \
    "2_create_student.json" "admin"

run_test_case 3 "获取特定学生" \
    "curl -s http://localhost:5000/api/admin/students/S0101 -b /tmp/test_cookie.txt" \
    "3_get_student.json" "admin"

run_test_case 4 "更新学生信息" \
    "curl -s -X PUT http://localhost:5000/api/admin/students/S0101 -H \"Content-Type: application/json\" -d '{\"student_name\": \"Updated Student Name\", \"class_id\": 1, \"password\": \"password123\"}' -b /tmp/test_cookie.txt" \
    "4_update_student.json" "admin"

run_test_case 5 "删除学生" \
    "curl -s -X DELETE http://localhost:5000/api/admin/students/S9999 -b /tmp/test_cookie.txt" \
    "5_delete_student.json" "admin"

run_test_case 6 "获取教师列表" \
    "curl -s http://localhost:5000/api/admin/teachers -b /tmp/test_cookie.txt" \
    "6_get_teachers.json" "admin"

run_test_case 7 "创建教师" \
    "curl -s -X POST http://localhost:5000/api/admin/teachers -H \"Content-Type: application/json\" -d '{\"teacher_name\": \"Test Teacher\", \"teacher_id\": 999, \"subject_id\": 1, \"password\": \"password123\"}' -b /tmp/test_cookie.txt" \
    "7_create_teacher.json" "admin"

run_test_case 8 "获取特定教师" \
    "curl -s http://localhost:5000/api/admin/teachers/1 -b /tmp/test_cookie.txt" \
    "8_get_teacher.json" "admin"

run_test_case 9 "更新教师信息" \
    "curl -s -X PUT http://localhost:5000/api/admin/teachers/1 -H \"Content-Type: application/json\" -d '{\"teacher_name\": \"Updated Teacher Name\"}' -b /tmp/test_cookie.txt" \
    "9_update_teacher.json" "admin"

run_test_case 10 "删除教师" \
    "curl -s -X DELETE http://localhost:5000/api/admin/teachers/999 -b /tmp/test_cookie.txt" \
    "10_delete_teacher.json" "admin"

run_test_case 11 "获取班级列表" \
    "curl -s http://localhost:5000/api/admin/classes -b /tmp/test_cookie.txt" \
    "11_get_classes.json" "admin"

run_test_case 12 "创建班级" \
    "curl -s -X POST http://localhost:5000/api/admin/classes -H \"Content-Type: application/json\" -d '{\"class_name\": \"Test Class\"}' -b /tmp/test_cookie.txt" \
    "12_create_class.json" "admin"

run_test_case 13 "获取特定班级" \
    "curl -s http://localhost:5000/api/admin/classes/1 -b /tmp/test_cookie.txt" \
    "13_get_class.json" "admin"

run_test_case 14 "更新班级信息" \
    "curl -s -X PUT http://localhost:5000/api/admin/classes/1 -H \"Content-Type: application/json\" -d '{\"class_name\": \"Updated Class Name\", \"grade\": 1}' -b /tmp/test_cookie.txt" \
    "14_update_class.json" "admin"

run_test_case 15 "删除班级" \
    "curl -s -X DELETE http://localhost:5000/api/admin/classes/1 -b /tmp/test_cookie.txt" \
    "15_delete_class.json" "admin"

run_test_case 16 "获取科目列表(管理员)" \
    "curl -s http://localhost:5000/api/admin/subjects -b /tmp/test_cookie.txt" \
    "16_get_subjects.json" "admin"

run_test_case 17 "创建科目" \
    "curl -s -X POST http://localhost:5000/api/admin/subjects -H \"Content-Type: application/json\" -d '{\"subject_name\": \"Test Subject\"}' -b /tmp/test_cookie.txt" \
    "17_create_subject.json" "admin"

run_test_case 18 "获取特定科目" \
    "curl -s http://localhost:5000/api/admin/subjects/1 -b /tmp/test_cookie.txt" \
    "18_get_subject.json" "admin"

run_test_case 19 "更新科目信息" \
    "curl -s -X PUT http://localhost:5000/api/admin/subjects/1 -H \"Content-Type: application/json\" -d '{\"subject_name\": \"Updated Subject Name\"}' -b /tmp/test_cookie.txt" \
    "19_update_subject.json" "admin"

run_test_case 20 "删除科目" \
    "curl -s -X DELETE http://localhost:5000/api/admin/subjects/1 -b /tmp/test_cookie.txt" \
    "20_delete_subject.json" "admin"

run_test_case 21 "获取考试类型列表(管理员)" \
    "curl -s http://localhost:5000/api/admin/exam-types -b /tmp/test_cookie.txt" \
    "21_get_exam_types.json" "admin"

run_test_case 22 "创建考试类型" \
    "curl -s -X POST http://localhost:5000/api/admin/exam-types -H \"Content-Type: application/json\" -d '{\"exam_type_name\": \"Test Exam Type\"}' -b /tmp/test_cookie.txt" \
    "22_create_exam_type.json" "admin"

run_test_case 23 "获取特定考试类型" \
    "curl -s http://localhost:5000/api/admin/exam-types/1 -b /tmp/test_cookie.txt" \
    "23_get_exam_type.json" "admin"

run_test_case 24 "更新考试类型" \
    "curl -s -X PUT http://localhost:5000/api/admin/exam-types/1 -H \"Content-Type: application/json\" -d '{\"exam_type_name\": \"Updated Exam Type\"}' -b /tmp/test_cookie.txt" \
    "24_update_exam_type.json" "admin"

run_test_case 25 "删除考试类型" \
    "curl -s -X DELETE http://localhost:5000/api/admin/exam-types/1 -b /tmp/test_cookie.txt" \
    "25_delete_exam_type.json" "admin"

run_test_case 26 "获取教师班级关系列表" \
    "curl -s http://localhost:5000/api/admin/teacher-classes -b /tmp/test_cookie.txt" \
    "26_get_teacher_classes.json" "admin"

run_test_case 27 "创建教师班级关系" \
    "curl -s -X POST http://localhost:5000/api/admin/teacher-classes -H \"Content-Type: application/json\" -d '{\"teacher_id\": 1, \"class_id\": 1}' -b /tmp/test_cookie.txt" \
    "27_create_teacher_class.json" "admin"

run_test_case 28 "获取特定教师班级关系" \
    "curl -s http://localhost:5000/api/admin/teacher-classes/1 -b /tmp/test_cookie.txt" \
    "28_get_teacher_class.json" "admin"

run_test_case 29 "更新教师班级关系" \
    "curl -s -X PUT http://localhost:5000/api/admin/teacher-classes/1 -H \"Content-Type: application/json\" -d '{\"teacher_id\": 2, \"class_id\": 2}' -b /tmp/test_cookie.txt" \
    "29_update_teacher_class.json" "admin"

run_test_case 30 "删除教师班级关系" \
    "curl -s -X DELETE http://localhost:5000/api/admin/teacher-classes/1 -H \"Content-Type: application/json\" -d '{\"class_id\": 2}' -b /tmp/test_cookie.txt" \
    "30_delete_teacher_class.json" "admin"

run_test_case 31 "获取学生成绩" \
    "curl -s http://localhost:5000/api/student/scores -b /tmp/test_cookie.txt" \
    "31_get_student_scores.json" "student"

run_test_case 32 "获取学生考试结果" \
    "curl -s http://localhost:5000/api/student/exam/results -b /tmp/test_cookie.txt" \
    "32_get_student_exam_results.json" "student"

run_test_case 33 "获取学生个人信息" \
    "curl -s http://localhost:5000/api/student/profile -b /tmp/test_cookie.txt" \
    "33_get_student_profile.json" "student"

run_test_case 34 "获取教师管理的学生列表" \
    "curl -s http://localhost:5000/api/teacher/students -b /tmp/test_cookie.txt" \
    "34_get_teacher_students.json" "teacher"

run_test_case 35 "获取考试列表" \
    "curl -s http://localhost:5000/api/teacher/exams -b /tmp/test_cookie.txt" \
    "35_get_exams.json" "teacher"

run_test_case 36 "创建考试" \
    "curl -s -X POST http://localhost:5000/api/teacher/exams -H \"Content-Type: application/json\" -d '{\"exam_name\": \"Test Exam\", \"subject_id\": 1, \"class_id\": 1, \"exam_type_id\": 1, \"exam_date\": \"2023-01-01\"}' -b /tmp/test_cookie.txt" \
    "36_create_exam.json" "teacher"

run_test_case 37 "获取特定考试" \
    "curl -s http://localhost:5000/api/teacher/exams/1 -b /tmp/test_cookie.txt" \
    "37_get_exam.json" "teacher"

run_test_case 38 "更新考试信息" \
    "curl -s -X PUT http://localhost:5000/api/teacher/exams/1 -H \"Content-Type: application/json\" -d '{\"exam_name\": \"Updated Exam\"}' -b /tmp/test_cookie.txt" \
    "38_update_exam.json" "teacher"

run_test_case 39 "删除考试" \
    "curl -s -X DELETE http://localhost:5000/api/teacher/exams/1 -b /tmp/test_cookie.txt" \
    "39_delete_exam.json" "teacher"

run_test_case 40 "获取成绩列表" \
    "curl -s http://localhost:5000/api/teacher/scores -b /tmp/test_cookie.txt" \
    "40_get_scores.json" "teacher"

run_test_case 41 "创建成绩" \
    "curl -s -X POST http://localhost:5000/api/teacher/scores -H \"Content-Type: application/json\" -d '{\"student_id\": \"S0101\", \"subject_id\": 1, \"exam_type_id\": 1, \"score\": 95.5}' -b /tmp/test_cookie.txt" \
    "41_create_score.json" "teacher"

run_test_case 42 "获取特定成绩" \
    "curl -s http://localhost:5000/api/teacher/scores/1 -b /tmp/test_cookie.txt" \
    "42_get_score.json" "teacher"

run_test_case 43 "更新成绩" \
    "curl -s -X PUT http://localhost:5000/api/teacher/scores/1 -H \"Content-Type: application/json\" -d '{\"score\": 90.0}' -b /tmp/test_cookie.txt" \
    "43_update_score.json" "teacher"

run_test_case 44 "删除成绩" \
    "curl -s -X DELETE http://localhost:5000/api/teacher/scores/1 -b /tmp/test_cookie.txt" \
    "44_delete_score.json" "teacher"

run_test_case 45 "获取考试结果" \
    "curl -s http://localhost:5000/api/teacher/exam/results -b /tmp/test_cookie.txt" \
    "45_get_exam_results.json" "teacher"

run_test_case 46 "获取教学表现" \
    "curl -s http://localhost:5000/api/teacher/exam/performance -b /tmp/test_cookie.txt" \
    "46_get_teacher_performance.json" "teacher"

run_test_case 47 "获取考试班级" \
    "curl -s http://localhost:5000/api/teacher/exam/classes -b /tmp/test_cookie.txt" \
    "47_get_exam_classes.json" "teacher"

# 关闭API服务器
echo "" | tee -a "$RESULT_DIR/test_results.log"
echo "关闭API服务器..." | tee -a "$RESULT_DIR/test_results.log"
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "带身份验证的API测试完成!"

# 如果指定了测试用例编号，显示测试结果
if [ -n "$TEST_CASE_NUMBER" ]; then
    echo ""
    echo "测试用例 $TEST_CASE_NUMBER 的结果:"
    test_result_file="$RESULT_DIR/${TEST_CASE_NUMBER}_*"
    if ls $test_result_file 1> /dev/null 2>&1; then
        cat $test_result_file
    else
        echo "未找到测试用例 $TEST_CASE_NUMBER 的结果文件"
    fi
# 如果指定了蓝图类型，显示该蓝图下所有测试的结果
elif [ -n "$TEST_BLUEPRINT" ]; then
    echo ""
    echo "$TEST_BLUEPRINT 蓝图下所有测试的结果:"
    blueprint_result_files="$RESULT_DIR/*_*"
    found_results=false
    for file in $blueprint_result_files; do
        filename=$(basename "$file")
        # 从文件名中提取测试编号和描述
        if [[ $filename =~ ^([0-9]+)_(.+)\.json$ ]]; then
            case_number=${BASH_REMATCH[1]}
            case_description=${BASH_REMATCH[2]}
            
            # 检查该测试用例是否属于指定的蓝图
            case_blueprint=""
            case "$case_number" in
                1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30)
                    case_blueprint="admin"
                    ;;
                31|32|33)
                    case_blueprint="student"
                    ;;
                34|35|36|37|38|39|40|41|42|43|44|45|46|47)
                    case_blueprint="teacher"
                    ;;
            esac
            
            if [ "$case_blueprint" = "$TEST_BLUEPRINT" ]; then
                echo ""
                echo "测试用例 $case_number ($case_description):"
                if [ -f "$file" ]; then
                    cat "$file"
                else
                    echo "结果文件不存在"
                fi
                found_results=true
            fi
        fi
    done
    
    if [ "$found_results" = false ]; then
        echo "未找到 $TEST_BLUEPRINT 蓝图下的测试结果"
    fi
fi