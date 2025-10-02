# Scout成绩管理系统 API 文档

## 1. 概述

Scout成绩管理系统是一个基于Flask框架开发的成绩管理平台，支持管理员、教师和学生三种角色的用户。系统采用Python 3.8+和MySQL数据库，提供完整的成绩管理功能。

### 1.1 技术栈
- Flask 2.3.2
- Python 3.8+
- MySQL

### 1.2 项目结构
```
scout/
├── app.py              # 应用入口
├── config.py           # 配置文件
├── apps/               # 应用模块
│   ├── blueprints/     # 蓝图路由
│   ├── services/       # 业务逻辑层
│   └── utils/          # 工具类
├── docs/               # 文档目录
├── logs/               # 日志目录
└── tests/              # 测试目录
```

## 2. 基础信息

### 2.1 服务地址
- 本地开发: `http://localhost:5000`
- API前缀: `/api`

### 2.2 认证方式
- 使用Session进行用户认证
- 登录后服务端会设置session cookie
- 后续请求需携带该cookie进行身份验证

### 2.3 数据格式
- 请求体: JSON格式
- 响应体: JSON格式
- 字符编码: UTF-8

## 3. 公共接口

### 3.1 首页
```
GET /
```
返回欢迎信息和系统版本

### 3.2 健康检查
```
GET /health
```
检查服务运行状态

### 3.3 错误测试
```
GET /test_error
```
用于测试错误处理机制

## 4. 认证接口

### 4.1 用户登录
```
POST /api/auth/login
```
请求体:
```json
{
  "user_id": "用户ID",
  "password": "密码"
}
```

### 4.2 获取当前用户信息
```
GET /api/auth/me
```
需要认证，返回当前登录用户的信息

### 4.3 用户登出
```
POST /api/auth/logout
```
需要认证，清除用户session

## 5. 学生接口

### 5.1 获取学生个人资料
```
GET /api/student/{student_id}/profile
```

### 5.2 获取学生成绩
```
GET /api/student/{student_id}/scores
```

### 5.3 获取学生考试结果
```
GET /api/student/{student_id}/exam_results
```

## 6. 教师接口

### 6.1 获取教师个人资料
```
GET /api/teacher/{teacher_id}/profile
```

### 6.2 管理学生成绩
```
GET /api/teacher/{teacher_id}/scores
PUT /api/teacher/{teacher_id}/scores
```

### 6.3 管理班级
```
GET /api/teacher/{teacher_id}/classes
```

### 6.4 管理学生
```
GET /api/teacher/{teacher_id}/students
```

## 7. 管理员接口

### 7.1 学生管理
```
GET /api/admin/students/          # 获取学生列表
POST /api/admin/students/         # 创建学生
GET /api/admin/students/{id}      # 获取特定学生
PUT /api/admin/students/{id}      # 更新学生信息
DELETE /api/admin/students/{id}   # 删除学生
```

### 7.2 教师管理
```
GET /api/admin/teachers/          # 获取教师列表
POST /api/admin/teachers/         # 创建教师
GET /api/admin/teachers/{id}      # 获取特定教师
PUT /api/admin/teachers/{id}      # 更新教师信息
DELETE /api/admin/teachers/{id}   # 删除教师
```

### 7.3 班级管理
```
GET /api/admin/classes/           # 获取班级列表
POST /api/admin/classes/          # 创建班级
GET /api/admin/classes/{id}       # 获取特定班级
PUT /api/admin/classes/{id}       # 更新班级信息
DELETE /api/admin/classes/{id}    # 删除班级
```

### 7.4 科目管理
```
GET /api/admin/subjects/          # 获取科目列表
POST /api/admin/subjects/         # 创建科目
GET /api/admin/subjects/{id}      # 获取特定科目
PUT /api/admin/subjects/{id}      # 更新科目信息
DELETE /api/admin/subjects/{id}   # 删除科目
```

### 7.5 考试类型管理
```
GET /api/admin/exam_types/        # 获取考试类型列表
POST /api/admin/exam_types/       # 创建考试类型
GET /api/admin/exam_types/{id}    # 获取特定考试类型
PUT /api/admin/exam_types/{id}    # 更新考试类型信息
DELETE /api/admin/exam_types/{id} # 删除考试类型
```

### 7.6 教师班级关联管理
```
GET /api/admin/teacher_classes/           # 获取教师班级关联列表
POST /api/admin/teacher_classes/          # 创建教师班级关联
GET /api/admin/teacher_classes/{id}       # 获取特定教师班级关联
PUT /api/admin/teacher_classes/{id}       # 更新教师班级关联信息
DELETE /api/admin/teacher_classes/{id}    # 删除教师班级关联
```

## 8. 错误处理

系统使用标准HTTP状态码表示请求结果状态：

- 200: 请求成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误

## 9. 使用示例

### 9.1 用户登录
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "T0101", "password": "123456"}' \
  -c cookie.txt
```

### 9.2 获取当前用户信息
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -b cookie.txt
```

### 9.3 获取学生列表(管理员)
```bash
curl -X GET http://localhost:5000/api/admin/students/ \
  -b cookie.txt
```

### 9.4 创建学生(管理员)
```bash
curl -X POST http://localhost:5000/api/admin/students/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": "S0201", "name": "张三", "class_id": "C01"}' \
  -b cookie.txt
```

### 9.5 获取教师个人资料
```bash
curl -X GET http://localhost:5000/api/teacher/T0101/profile \
  -b cookie.txt
```

### 9.6 获取学生成绩
```bash
curl -X GET http://localhost:5000/api/student/S0101/scores \
  -b cookie.txt
```