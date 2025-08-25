# 学生成绩管理系统

## 项目概述

学生成绩管理系统是一个基于Web的应用程序，旨在帮助学校高效地管理学生信息和成绩数据。该系统提供三个不同的用户角色：管理员、教师和学生，每个角色都有特定的权限和功能。

## 技术架构

### 前端 (Web)
- **框架**: Angular 18
- **UI组件库**: Angular Material
- **响应式设计**: 支持多种设备屏幕尺寸
- **路由管理**: Angular Router
- **状态管理**: 使用Angular服务进行组件间数据共享

### 后端 (API)
- **框架**: Flask (Python)
- **数据库**: MySQL
- **会话管理**: Flask-Session
- **跨域支持**: Flask-CORS
- **日志管理**: Python logging模块
- **测试框架**: pytest

### 数据库
- **数据库系统**: MySQL
- **表结构**: 7个基础表 + 多个视图
- **数据完整性**: 外键约束和数据验证

## 项目结构

```
scout/
├── db/                 # 数据库相关文件
│   ├── backup/         # 数据库备份文件
│   ├── backup_db.sh    # 数据库备份脚本
│   └── restore_db.sh   # 数据库恢复脚本
├── api/                # Flask后端API
│   ├── app/            # 应用核心模块
│   ├── blueprints/     # Flask蓝图（路由）
│   ├── config/         # 配置文件
│   ├── runtime/        # 运行时文件（日志、会话等）
│   ├── services/       # 业务逻辑层
│   ├── utils/          # 工具模块
│   ├── tests/          # 测试文件
│   ├── requirements.txt # Python依赖
│   └── curl_test.sh    # API测试脚本
└── web/                # Angular前端
```

## API架构

### 核心组件

1. **应用工厂** ([app/factory.py](file:///home/jimmy/repo/scout/api/app/factory.py))
   - 使用Flask应用工厂模式创建应用实例
   - 配置CORS支持
   - 初始化Flask-Session
   - 注册蓝图和异常处理器

2. **配置管理** ([config/config.py](file:///home/jimmy/repo/scout/api/config/config.py))
   - 支持多种环境配置（开发、生产、测试）
   - 通过环境变量加载敏感配置
   - 数据库连接配置
   - Session配置

3. **运行时目录** ([runtime/](file:///home/jimmy/repo/scout/api/runtime/))
   - **会话存储** ([flask_session/](file:///home/jimmy/repo/scout/api/runtime/flask_session/)): Flask会话文件存储
   - **日志文件** ([logs/](file:///home/jimmy/repo/scout/api/runtime/logs/)): 应用日志文件

4. **工具模块** ([utils/](file:///home/jimmy/repo/scout/api/utils/))
   - **数据库工具** ([database_service.py](file:///home/jimmy/repo/scout/api/utils/database_service.py)): 数据库连接和操作封装
   - **日志工具** ([logger.py](file:///home/jimmy/repo/scout/api/utils/logger.py)): 统一日志记录
   - **助手函数** ([helpers.py](file:///home/jimmy/repo/scout/api/utils/helpers.py)): 通用工具函数，包括认证装饰器
   - **认证模块** ([auth.py](file:///home/jimmy/repo/scout/api/utils/auth.py)): 认证相关功能

5. **服务层** ([services/](file:///home/jimmy/repo/scout/api/services/))
   - **学生服务** ([student_service.py](file:///home/jimmy/repo/scout/api/services/student_service.py)): 学生信息管理
   - **教师服务** ([teacher_service.py](file:///home/jimmy/repo/scout/api/services/teacher_service.py)): 教师信息管理
   - **成绩服务** ([score_service.py](file:///home/jimmy/repo/scout/api/services/score_service.py)): 成绩数据管理
   - **班级服务** ([class_service.py](file:///home/jimmy/repo/scout/api/services/class_service.py)): 班级信息管理
   - **科目服务** ([subject_service.py](file:///home/jimmy/repo/scout/api/services/subject_service.py)): 科目信息管理
   - **考试类型服务** ([exam_type_service.py](file:///home/jimmy/repo/scout/api/services/exam_type_service.py)): 考试类型管理
   - **教师班级服务** ([teacher_class_service.py](file:///home/jimmy/repo/scout/api/services/teacher_class_service.py)): 教师班级关联管理

6. **蓝图路由** ([blueprints/](file:///home/jimmy/repo/scout/api/blueprints/))
   - **认证蓝图** ([auth/](file:///home/jimmy/repo/scout/api/blueprints/auth/)): 用户认证相关API
   - **管理员蓝图** ([admin/](file:///home/jimmy/repo/scout/api/blueprints/admin/)): 管理员相关API
   - **教师蓝图** ([teacher/](file:///home/jimmy/repo/scout/api/blueprints/teacher/)): 教师相关API
   - **学生蓝图** ([student/](file:///home/jimmy/repo/scout/api/blueprints/student/)): 学生相关API

### API端点

#### 认证API (`/api/auth`)
- 用户登录: `POST /login`
- 用户登出: `POST /logout`
- 健康检查: `GET /health`

#### 管理员API (`/api/admin`)
- 学生管理: `/students`
- 教师管理: `/teachers`
- 班级管理: `/classes`
- 科目管理: `/subjects`
- 考试类型管理: `/exam-types`
- 教师班级关联管理: `/teacher-classes`

#### 教师API (`/api/teacher`)
- 学生成绩管理: `/scores`
- 考试管理: `/exams`
- 学生管理: `/students`
- 考试结果: `/exam/results`
- 教师表现: `/exam/performance`
- 班级管理: `/exam/classes`

#### 学生API (`/api/student`)
- 成绩查询: `/scores`

### 数据库设计

#### 基础表
1. **Classes**: 班级信息表
2. **ExamTypes**: 考试类型表
3. **Scores**: 成绩表
4. **Students**: 学生信息表
5. **Subjects**: 科目表
6. **TeacherClasses**: 教师班级关联表
7. **Teachers**: 教师信息表

#### 视图
- 多个用于数据分析和报告的视图

### 用户角色和权限

#### 管理员
- 管理所有基础数据（学生、教师、班级、科目、考试类型）
- 分配教师到班级和科目
- 系统配置和维护

#### 教师
- 查看所教班级学生成绩
- 录入和修改成绩
- 查看统计信息和分析报告
- 管理考试信息

#### 学生
- 查看个人信息
- 查看个人成绩

## 功能模块

### 考试成绩等级分布页面
展示各科目考试成绩的等级分布情况，帮助分析教学效果。

### 考试结果页面
展示详细的学生考试成绩，支持多种筛选和排序方式。

### 教师表现统计页面
展示教师教学表现的统计数据，包括平均分、及格率等指标。

## 安装和运行

### 数据库设置
```bash
# 进入数据库目录
cd db

# 恢复数据库（使用最新备份）
./restore_db.sh

# 或指定特定备份文件
./restore_db.sh school_management_backup_20250823_233411.sql
```

### 后端API
```bash
# 进入API目录
cd api

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

### 前端Web
```bash
# 进入Web目录
cd web

# 安装依赖
npm install

# 运行开发服务器
ng serve
```

## 测试

### 运行测试
```bash
# 进入API目录
cd api

# 运行所有测试
python -m pytest tests/

# 运行API测试脚本（带身份验证的API测试）
./curl_test.sh

# 运行不带身份验证的API测试
./test_api.sh
```

### 测试结构
- **服务层测试**: 测试业务逻辑
- **工具函数测试**: 测试通用工具函数
- **应用核心测试**: 测试应用配置和基本功能
- **路由测试**: 测试API端点

## 部署

### 生产环境配置
1. 设置环境变量
2. 配置数据库连接
3. 配置Web服务器（Nginx/Apache）
4. 配置应用服务器（Gunicorn/uWSGI）

### 安全考虑
- 使用HTTPS
- 设置强密码策略
- 定期备份数据库
- 限制访问权限