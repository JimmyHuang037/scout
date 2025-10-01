# 管理员API端点规范

## 概述

管理员API端点提供对学校管理系统核心数据的完全访问权限，包括学生、教师、班级、科目、考试类型和教师班级关联的完整管理功能。

## API端点

### 学生管理 (`/api/admin/students`)

#### 获取学生列表
- **URL**: `GET /api/admin/students`
- **描述**: 获取所有学生列表，支持分页
- **查询参数**:
  - `page`: 页码（默认: 1）
  - `per_page`: 每页记录数（默认: 10）
- **响应**: 学生列表数据

#### 创建学生
- **URL**: `POST /api/admin/students`
- **描述**: 创建新学生账户
- **请求体**:
  ```json
  {
    "student_id": "学生ID",
    "student_name": "学生姓名",
    "class_id": "班级ID",
    "password": "密码"
  }
  ```
- **响应**: 创建成功的学生信息

#### 获取特定学生
- **URL**: `GET /api/admin/students/<string:student_id>`
- **描述**: 获取指定学生的详细信息
- **参数**: 
  - `student_id`: 学生ID（字符串格式）
- **响应**: 学生详细信息

#### 更新学生信息
- **URL**: `PUT /api/admin/students/<string:student_id>`
- **描述**: 更新指定学生的信息
- **参数**: 
  - `student_id`: 学生ID（字符串格式）
- **请求体**: 需要更新的字段
- **响应**: 更新结果

#### 删除学生
- **URL**: `DELETE /api/admin/students/<string:student_id>`
- **描述**: 删除指定学生
- **参数**: 
  - `student_id`: 学生ID（字符串格式）
- **响应**: 删除结果

### 教师管理 (`/api/admin/teachers`)

#### 获取教师列表
- **URL**: `GET /api/admin/teachers`
- **描述**: 获取所有教师列表，支持分页
- **查询参数**:
  - `page`: 页码（默认: 1）
  - `per_page`: 每页记录数（默认: 10）
- **响应**: 教师列表数据

#### 创建教师
- **URL**: `POST /api/admin/teachers`
- **描述**: 创建新教师账户
- **请求体**:
  ```json
  {
    "teacher_name": "教师姓名",
    "subject_id": "科目ID",
    "password": "密码"
  }
  ```
- **响应**: 创建成功的教师信息

#### 获取特定教师
- **URL**: `GET /api/admin/teachers/<int:teacher_id>`
- **描述**: 获取指定教师的详细信息
- **参数**: 
  - `teacher_id`: 教师ID（整数）
- **响应**: 教师详细信息

#### 更新教师信息
- **URL**: `PUT /api/admin/teachers/<int:teacher_id>`
- **描述**: 更新指定教师的信息
- **参数**: 
  - `teacher_id`: 教师ID（整数）
- **请求体**: 需要更新的字段
- **响应**: 更新结果

#### 删除教师
- **URL**: `DELETE /api/admin/teachers/<int:teacher_id>`
- **描述**: 删除指定教师
- **参数**: 
  - `teacher_id`: 教师ID（整数）
- **响应**: 删除结果

### 班级管理 (`/api/admin/classes`)

#### 获取班级列表
- **URL**: `GET /api/admin/classes`
- **描述**: 获取所有班级列表
- **响应**: 班级列表数据

#### 创建班级
- **URL**: `POST /api/admin/classes`
- **描述**: 创建新班级
- **请求体**:
  ```json
  {
    "class_name": "班级名称",
    "grade_id": "年级ID"
  }
  ```
- **响应**: 创建成功的班级信息

#### 获取特定班级
- **URL**: `GET /api/admin/classes/<int:class_id>`
- **描述**: 获取指定班级的详细信息
- **参数**: 
  - `class_id`: 班级ID（整数）
- **响应**: 班级详细信息

#### 更新班级信息
- **URL**: `PUT /api/admin/classes/<int:class_id>`
- **描述**: 更新指定班级的信息
- **参数**: 
  - `class_id`: 班级ID（整数）
- **请求体**: 需要更新的字段
- **响应**: 更新结果

#### 删除班级
- **URL**: `DELETE /api/admin/classes/<int:class_id>`
- **描述**: 删除指定班级
- **参数**: 
  - `class_id`: 班级ID（整数）
- **响应**: 删除结果

### 科目管理 (`/api/admin/subjects`)

#### 获取科目列表
- **URL**: `GET /api/admin/subjects`
- **描述**: 获取所有科目列表，支持分页
- **查询参数**:
  - `page`: 页码（默认: 1）
  - `per_page`: 每页记录数（默认: 10）
- **响应**: 科目列表数据

#### 创建科目
- **URL**: `POST /api/admin/subjects`
- **描述**: 创建新科目
- **请求体**:
  ```json
  {
    "subject_name": "科目名称"
  }
  ```
- **响应**: 创建成功的科目信息

#### 获取特定科目
- **URL**: `GET /api/admin/subjects/<int:subject_id>`
- **描述**: 获取指定科目的详细信息
- **参数**: 
  - `subject_id`: 科目ID（整数）
- **响应**: 科目详细信息

#### 更新科目信息
- **URL**: `PUT /api/admin/subjects/<int:subject_id>`
- **描述**: 更新指定科目的信息
- **参数**: 
  - `subject_id`: 科目ID（整数）
- **请求体**: 需要更新的字段
- **响应**: 更新结果

#### 删除科目
- **URL**: `DELETE /api/admin/subjects/<int:subject_id>`
- **描述**: 删除指定科目
- **参数**: 
  - `subject_id`: 科目ID（整数）
- **响应**: 删除结果

### 考试类型管理 (`/api/admin/exam-types`)

#### 获取考试类型列表
- **URL**: `GET /api/admin/exam-types`
- **描述**: 获取所有考试类型列表，支持分页
- **查询参数**:
  - `page`: 页码（默认: 1）
  - `per_page`: 每页记录数（默认: 10）
- **响应**: 考试类型列表数据

#### 创建考试类型
- **URL**: `POST /api/admin/exam-types`
- **描述**: 创建新考试类型
- **请求体**:
  ```json
  {
    "exam_type_name": "考试类型名称"
  }
  ```
- **响应**: 创建成功的考试类型信息

#### 获取特定考试类型
- **URL**: `GET /api/admin/exam-types/<int:exam_type_id>`
- **描述**: 获取指定考试类型的详细信息
- **参数**: 
  - `exam_type_id`: 考试类型ID（整数）
- **响应**: 考试类型详细信息

#### 更新考试类型信息
- **URL**: `PUT /api/admin/exam-types/<int:exam_type_id>`
- **描述**: 更新指定考试类型的信息
- **参数**: 
  - `exam_type_id`: 考试类型ID（整数）
- **请求体**: 需要更新的字段
- **响应**: 更新结果

#### 删除考试类型
- **URL**: `DELETE /api/admin/exam-types/<int:exam_type_id>`
- **描述**: 删除指定考试类型
- **参数**: 
  - `exam_type_id`: 考试类型ID（整数）
- **响应**: 删除结果

### 教师班级关联管理 (`/api/admin/teacher-classes`)

#### 获取教师班级关联列表
- **URL**: `GET /api/admin/teacher-classes`
- **描述**: 获取所有教师班级关联列表，支持分页
- **查询参数**:
  - `page`: 页码（默认: 1）
  - `per_page`: 每页记录数（默认: 10）
- **响应**: 教师班级关联列表数据

#### 创建教师班级关联
- **URL**: `POST /api/admin/teacher-classes`
- **描述**: 创建教师与班级的关联关系
- **请求体**:
  ```json
  {
    "teacher_id": "教师ID",
    "class_id": "班级ID"
  }
  ```
- **响应**: 创建成功的关联信息

#### 获取特定教师班级关联
- **URL**: `GET /api/admin/teacher-classes/<int:teacher_id>`
- **描述**: 获取指定教师的所有班级关联信息
- **参数**: 
  - `teacher_id`: 教师ID（整数）
- **响应**: 教师班级关联信息

#### 更新教师班级关联
- **URL**: `PUT /api/admin/teacher-classes/<int:teacher_class_id>`
- **描述**: 更新教师班级关联信息
- **参数**: 
  - `teacher_class_id`: 教师班级关联ID（整数）
- **请求体**:
  ```json
  {
    "teacher_id": "新教师ID",
    "class_id": "班级ID"
  }
  ```
- **响应**: 更新结果

#### 删除教师班级关联
- **URL**: `DELETE /api/admin/teacher-classes/<int:teacher_class_id>`
- **描述**: 删除教师班级关联关系
- **参数**: 
  - `teacher_class_id`: 教师班级关联ID（整数）
- **查询参数**:
  - `class_id`: 班级ID（必需）
- **响应**: 删除结果

## 错误处理

所有管理员端点遵循统一的错误处理机制：
- 认证失败返回401状态码
- 权限不足返回403状态码
- 资源不存在返回404状态码
- 请求数据错误返回400状态码
- 服务器内部错误返回500状态码

错误响应格式:
```json
{
  "success": false,
  "message": "错误描述信息",
  "error_code": "错误代码"
}
```

## 日志记录

所有管理员操作都会被记录在系统日志中，包括：
- 操作类型（创建、读取、更新、删除）
- 操作对象（学生、教师、班级等）
- 操作结果（成功/失败）
- 操作时间
- 执行操作的管理员ID

## 安全注意事项

1. 所有管理员端点必须通过HTTPS访问
2. 敏感操作（如删除）应进行二次确认
3. 密码应使用安全的哈希算法存储
4. 定期审查管理员账户和操作日志
5. 限制管理员账户的登录尝试次数