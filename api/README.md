# 学生成绩管理系统 API

## 项目概述

学生成绩管理系统是一个基于Web的应用程序，旨在帮助学校高效地管理学生信息和成绩数据。该系统提供三个不同的用户角色：管理员、教师和学生，每个角色都有特定的权限和功能。

## 技术架构

### 后端技术栈
- **框架**: Flask 2.3.2
- **数据库**: MySQL 8.4.6
- **数据库连接**: PyMySQL 1.1.0
- **ORM**: SQLAlchemy 2.0.15
- **跨域支持**: Flask-CORS 4.0.0
- **会话管理**: Flask-Session 0.5.0
- **日志管理**: Python logging模块
- **测试框架**: pytest 7.4.0
- **环境变量管理**: python-dotenv 1.0.0

### 项目结构

```
api/
├── app.py                    # Flask应用入口点
├── config.py                 # 应用配置文件
├── requirements.txt         # Python依赖包
├── pytest.ini              # pytest配置
├── README.md               # 项目文档（本文件）
├── apps/                   # 应用核心模块
│   ├── blueprints/         # Flask蓝图（路由）
│   │   ├── auth/          # 认证相关API
│   │   ├── admin/         # 管理员API
│   │   ├── teacher/       # 教师API
│   │   ├── student/       # 学生API
│   │   └── common/        # 通用API
│   ├── services/          # 业务逻辑层
│   │   ├── student_service.py      # 学生管理服务
│   │   ├── teacher_service.py      # 教师管理服务
│   │   ├── score_service.py        # 成绩管理服务
│   │   ├── class_service.py        # 班级管理服务
│   │   ├── subject_service.py      # 科目管理服务
│   │   ├── exam_type_service.py    # 考试类型管理服务
│   │   └── teacher_class_service.py # 教师班级关联服务
│   └── utils/             # 工具模块
│       ├── database_service.py    # 数据库连接和操作封装
│       ├── auth.py               # 认证相关功能
│       └── helpers.py            # 通用工具函数
├── tests/                  # 测试文件
│   ├── conftest.py         # 测试配置
│   ├── test_curl_base.py   # 基础测试类
│   ├── test_admin_endpoints.py    # 管理员端点测试
│   ├── test_teacher_endpoints.py  # 教师端点测试
│   └── test_student_endpoints.py  # 学生端点测试
├── docs/                   # 文档目录
│   ├── language.md        # 语言相关文档
│   ├── refactor.md        # 重构相关文档
│   └── test.md           # 测试相关文档
├── logs/                  # 日志文件
│   ├── app.log           # 应用日志
│   └── test/             # 测试结果和curl命令日志
├── .venv/                # Python虚拟环境
├── .pytest_cache/        # pytest缓存
└── .vscode/             # VS Code配置
```

## 数据库配置

### 连接信息
- **主机**: localhost
- **用户**: root
- **密码**: Newuser1
- **数据库**: school_management
- **字符集**: utf8mb4

### 数据库结构
系统包含7个基础表和多个视图：
- **Classes**: 班级信息表
- **ExamTypes**: 考试类型表
- **Scores**: 成绩表
- **Students**: 学生信息表
- **Subjects**: 科目表
- **TeacherClasses**: 教师班级关联表
- **Teachers**: 教师信息表

## 默认用户信息

系统包含以下默认用户账户用于测试：

| 用户ID  | 用户名     | 角色   | 密码             |
|---------|------------|--------|------------------|
| admin   | 管理员     | admin  | admin            |
| T0101   | 谷雪       | teacher| teacher_password |
| T0102   | 植波明     | teacher| teacher_password |
| T0103   | 董龙铭     | teacher| teacher_password |
| S0101   | 薛磊       | student| student_password |
| S0102   | 易敏       | student| student_password |

## API端点

### 认证API (`/api/auth`)
- `POST /login` - 用户登录
- `POST /logout` - 用户登出
- `GET /health` - 健康检查

### 管理员API (`/api/admin`)
- `GET /students` - 获取学生列表
- `POST /students` - 添加学生
- `PUT /students/{student_id}` - 更新学生信息
- `DELETE /students/{student_id}` - 删除学生
- `GET /teachers` - 获取教师列表
- `POST /teachers` - 添加教师
- `PUT /teachers/{teacher_id}` - 更新教师信息
- `DELETE /teachers/{teacher_id}` - 删除教师
- `GET /classes` - 获取班级列表
- `POST /classes` - 添加班级
- `PUT /classes/{class_id}` - 更新班级信息
- `DELETE /classes/{class_id}` - 删除班级
- `GET /subjects` - 获取科目列表
- `POST /subjects` - 添加科目
- `PUT /subjects/{subject_id}` - 更新科目信息
- `DELETE /subjects/{subject_id}` - 删除科目
- `GET /exam-types` - 获取考试类型列表
- `POST /exam-types` - 添加考试类型
- `PUT /exam-types/{exam_type_id}` - 更新考试类型信息
- `DELETE /exam-types/{exam_type_id}` - 删除考试类型
- `GET /teacher-classes` - 获取教师班级关联列表
- `POST /teacher-classes` - 添加教师班级关联
- `DELETE /teacher-classes/{teacher_id}/{class_id}` - 删除教师班级关联

### 教师API (`/api/teacher`)
- `GET /scores` - 获取成绩列表
- `POST /scores` - 添加成绩
- `PUT /scores/{score_id}` - 更新成绩
- `DELETE /scores/{score_id}` - 删除成绩
- `GET /exams` - 获取考试列表
- `POST /exams` - 添加考试
- `PUT /exams/{exam_id}` - 更新考试
- `DELETE /exams/{exam_id}` - 删除考试
- `GET /students` - 获取教师所教学生列表
- `GET /exam/results` - 获取考试结果
- `GET /exam/performance` - 获取教师表现统计
- `GET /exam/classes` - 获取教师所教班级

### 学生API (`/api/student`)
- `GET /{student_id}/profile` - 获取学生个人资料
- `GET /{student_id}/scores` - 获取学生成绩
- `GET /{student_id}/exam_results` - 获取学生考试结果

## 用户角色和权限

### 管理员 (admin)
- 管理所有基础数据（学生、教师、班级、科目、考试类型）
- 分配教师到班级和科目
- 系统配置和维护
- 查看所有统计数据

### 教师 (teacher)
- 查看所教班级学生成绩
- 录入和修改成绩
- 查看统计信息和分析报告
- 管理考试信息
- 查看教学表现统计

### 学生 (student)
- 查看个人信息
- 查看个人成绩
- 查看考试结果

## 安装和运行

### 环境要求
- Python 3.8+
- MySQL 8.0+
- pip包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd scout/api
```

2. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库设置**
```bash
# 进入数据库目录
cd ../db

# 恢复数据库（使用最新备份）
./restore_db.sh --auto --latest

# 或恢复到测试数据库
./restore_db.sh --latest school_management_test --auto
```

5. **运行应用**
```bash
# 返回API目录
cd ../api

# 运行Flask应用
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_student_endpoints.py

# 运行测试并生成覆盖率报告
pytest --cov=apps tests/
```

### 测试结果
测试结果和curl命令将保存在 `logs/test/` 目录中：
- `student_curl_commands.log` - 学生API测试命令
- `teacher_curl_commands.log` - 教师API测试命令
- 各种JSON文件包含API响应结果

## 日志管理

### 日志配置
- **日志文件**: `logs/app.log`
- **日志级别**: DEBUG
- **日志格式**: `%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]`

### 日志轮转
建议在生产环境中配置日志轮转以避免日志文件过大。

## 开发指南

### 代码结构
- **应用工厂模式**: 使用 `AppFactory` 类创建Flask应用实例
- **蓝图架构**: 按功能模块划分API路由
- **服务层模式**: 业务逻辑与路由分离
- **依赖注入**: 通过构造函数注入服务依赖

### 添加新功能
1. 在 `apps/services/` 中添加新的服务类
2. 在 `apps/blueprints/` 中添加新的蓝图或扩展现有蓝图
3. 在 `tests/` 中添加相应的测试用例
4. 更新文档和API端点说明

### 代码规范
- 遵循PEP 8代码风格
- 使用类型注解
- 编写单元测试
- 添加适当的日志记录

## 部署

### 环境变量
可以通过环境变量覆盖配置：
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=school_management
export FLASK_ENV=production
```

### 生产环境配置
1. 设置 `DEBUG=False`
2. 配置适当的日志级别
3. 使用生产数据库
4. 配置反向代理（如Nginx）
5. 使用WSGI服务器（如Gunicorn）

## 故障排除

### 常见问题
1. **数据库连接失败**: 检查MySQL服务是否运行，连接参数是否正确
2. **端口占用**: 更改 `config.py` 中的PORT设置
3. **权限问题**: 确保数据库用户有适当权限
4. **依赖问题**: 确保所有依赖包正确安装

### 调试模式
在 `config.py` 中设置 `DEBUG=True` 以启用调试模式，获取详细的错误信息。

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。

## 最后更新

2025年6月23日 - 基于API文件夹扫描结果更新文档