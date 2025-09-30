# 测试规范

1. 不需要登录的测试 (no login test)
2. 不需要会话的测试 (no session needed)
3. Student Blueprint测试端点：
   - GET /api/student/profile (获取学生个人资料)
   - GET /api/student/scores (获取学生成绩)
   - GET /api/student/exam/results (获取学生考试结果)
4. 测试方法：直接访问API端点，不附加任何认证信息