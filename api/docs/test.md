# 测试规范

1. 不需要登录的测试 (no login test)
2. 不需要会话的测试 (no session needed)
3. Student Blueprint测试端点：
   - GET /api/student/{student_id}/profile (获取学生个人资料)
   - GET /api/student/{student_id}/scores (获取学生成绩)
   - GET /api/student/{student_id}/exam_results (获取学生考试结果)
4. 测试方法：直接访问API端点，不附加任何认证信息
5. 测试命令示例：
   - curl -s http://127.0.0.1:5000/api/student/S0101/profile | jq
   - curl -s http://127.0.0.1:5000/api/student/S0101/scores | jq
   - curl -s http://127.0.0.1:5000/api/student/S0101/exam_results | jq
6. 所有curl命令测试应使用jq格式化输出，以提高可读性