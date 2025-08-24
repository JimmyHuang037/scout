# 学生成绩管理系统

本项目是一个学生成绩管理系统，包含数据库设计、Flask API 和 Angular Web 前端三个主要部分。

项目结构如下：
```
.
├── api/              # Flask API 后端代码
├── db/               # 数据库相关文件和脚本
│   ├── backup/       # 数据库备份文件
│   ├── backup_db.sh  # 数据库备份脚本
│   ├── export_school_data.py  # 数据导出脚本
│   ├── import_school_data.py  # 数据导入脚本
│   ├── restore_db.sh # 数据库恢复脚本
│   ├── school_management.xlsx # 基础表数据文件
│   └── school_management_views.xlsx # 视图数据文件
├── web/              # Angular Web 前端代码
├── README.md         # 项目说明文档
└── .gitignore        # Git 忽略文件配置
```

## Flask API 开发规范

为确保 Flask API 代码质量和可维护性，制定以下开发规范：

### 项目结构规范
1. **使用Blueprint组织API路由**：
   - 按用户角色创建独立的蓝图文件（admin.py、teacher.py、student.py等）
   - 所有蓝图文件应放在 `api/blueprints/` 目录下
   - 每个蓝图应有统一的URL前缀（如 `/api/admin`、`/api/teacher`、`/api/student`）

2. **配置管理**：
   - 创建独立的配置模块 `api/config/config.py`
   - 使用类结构组织配置（Config基类和环境特定子类）
   - 通过环境变量管理敏感信息和环境特定配置

3. **数据库访问**：
   - 使用 `api/database.py` 模块统一管理数据库连接
   - 实现连接池和自动关闭机制
   - 遵循Flask应用上下文最佳实践

### API设计规范
1. **RESTful设计原则**：
   - 使用标准HTTP方法（GET、POST、PUT、DELETE）
   - 合理设计资源URL
   - 正确使用HTTP状态码

2. **统一响应格式**：
   ```json
   {
     "success": true/false,
     "data": {...},       // 成功时返回数据
     "error": "..."       // 失败时返回错误信息
   }
   ```

3. **错误处理**：
   - 实现全局异常处理
   - 提供有意义的错误信息
   - 正确设置HTTP状态码

4. **数据验证**：
   - 对所有输入数据进行验证
   - 提供清晰的验证错误信息

5. **安全性**：
   - 实现身份验证和授权机制
   - 敏感操作需要权限验证
   - 防止SQL注入等安全问题

### 代码质量规范
1. **代码组织**：
   - 遵循PEP8代码风格
   - 合理划分模块和函数
   - 添加必要的注释和文档字符串

2. **依赖管理**：
   - 使用 `requirements.txt` 管理依赖
   - 定期更新依赖版本
   - 避免不必要的依赖

3. **测试**：
   - 编写单元测试和集成测试
   - 使用测试驱动开发（TDD）方法
   - 确保测试覆盖率

## 前后端需求概览（精简版）

### 用户角色
系统包含三种用户角色，每种角色有不同的功能权限：

1. **管理员 (Admin)**
   - 管理学生、教师、班级、科目、考试类型等基础数据
   - 可进行增删改查操作

2. **教师 (Teacher)**
   - 查看所教班级学生成绩和信息
   - 录入和修改学生成绩
   - 查看班级成绩分布、考试结果、教学表现等统计信息

3. **学生 (Student)**
   - 查看个人信息和成绩
   - 查看个人考试结果和排名

### 核心功能页面
前端需要实现以下几个核心功能页面，后端提供相应API支持：

1. **考试成绩等级分布页面 (exam_class)**
   - 展示各班级在不同考试中的成绩等级分布（A/B/C/D）
   - 支持按考试类型和班级筛选

2. **考试结果页面 (exam_result)**
   - 展示学生考试成绩和排名
   - 支持按考试类型和班级筛选

3. **教师表现页面 (teacher_performance)**
   - 展示教师教学表现统计数据
   - 支持按考试类型和教师筛选

### 数据实体操作
根据不同实体特性，前后端采用不同的处理方式：

1. **可直接CRUD的视图**：scores、teachers、students
2. **需操作基础表的实体**：classes、subjects、exam_types、teacher_classes
3. **只读视图**：exam_class、exam_results、teacher_performance、teacher_counts

## 1. 数据库部分 (db)

### 数据库连接信息

使用以下命令连接到MySQL数据库：

```bash
mysql -u root -p Newuser1
```

默认数据库为 `school_management`。

### 数据库结构

`school_management` 数据库包含以下七个表及其结构：

1. **Classes 表**：
   - class_id (int, 主键, 自增)
   - class_name (varchar(255), 非空)
   
   示例数据：
   ```
   +----------+------------+
   | class_id | class_name |
   +----------+------------+
   |        1 | 高三1班    |
   |        2 | 高三2班    |
   |        3 | 高三3班    |
   |        4 | 高三4班    |
   +----------+------------+
   ```

2. **Teachers 表**：
   - teacher_id (int, 主键, 自增)
   - teacher_name (varchar(255), 非空)
   - subject_id (int, 非空, 外键引用Subjects.subject_id)
   - password (varchar(255), 可为空)
   
   示例数据：
   ```
   +------------+-------------+------------+----------+
   | teacher_id | teacher_name| subject_id | password |
   +------------+-------------+------------+----------+
   |          1 | 王老师      |          1 | NULL     |
   |          2 | 李老师      |          2 | NULL     |
   |          3 | 张老师      |          3 | NULL     |
   |          1 | 胡老师      |          4 | NULL     |
   |          5 | 赵老师      |          5 | NULL     |
   +------------+-------------+------------+----------+
   ```

3. **TeacherClasses 表**：
   - teacher_id (int, 主键的一部分, 外键引用Teachers.teacher_id)
   - class_id (int, 主键的一部分, 外键引用Classes.class_id)
   
   示例数据：
   ```
   +------------+----------+
   | teacher_id | class_id |
   +------------+----------+
   |          1 |        1 |
   |          2 |        1 |
   |          3 |        1 |
   |          1 |        2 |
   |          2 |        2 |
   +------------+----------+
   ```

4. **Students 表**：
   - student_id (varchar(255), 主键)
   - student_name (varchar(255), 非空)
   - class_id (int, 非空, 外键引用Classes.class_id)
   - password (varchar(255), 可为空)
   
   示例数据：
   ```
   +------------+-------------+----------+----------+
   | student_id | student_name| class_id | password |
   +------------+-------------+----------+----------+
   | S1001      | 尤丽        |        3 | pass123  |
   | S1002      | 卫桂英      |        2 | pass123  |
   | S1003      | 郑娟        |        1 | pass123  |
   | S1004      | 杨敏        |        4 | pass123  |
   | S1005      | 秦敏        |        4 | pass123  |
   +------------+-------------+----------+----------+
   ```

5. **Scores 表**：
   - score_id (int, 主键, 自增)
   - student_id (varchar(255), 非空, 外键引用Students.student_id)
   - subject_id (int, 非空, 外键引用Subjects.subject_id)
   - exam_type_id (int, 非空, 外键引用ExamTypes.type_id)
   - score (int, 可为空)
   
   示例数据：
   ```
   +----------+------------+------------+---------------+-------+
   | score_id | student_id | subject_id | exam_type_id  | score |
   +----------+------------+------------+---------------+-------+
   |        1 | S1001      |          1 |             1 |    85 |
   |        2 | S1001      |          2 |             1 |    69 |
   |        3 | S1001      |          3 |             1 |    76 |
   |        4 | S1001      |          4 |             1 |    87 |
   |        5 | S1001      |          5 |             1 |    60 |
   +----------+------------+------------+---------------+-------+
   ```

6. **ExamTypes 表**：
   - type_id (int, 主键, 自增)
   - exam_type_name (varchar(255), 非空)
   
   示例数据：
   ```
   +-------------+-----------------+
   | type_id     | exam_type_name  |
   +-------------+-----------------+
   |       1     | 第一次月考      |
   |       2     | 期中考          |
   |       3     | 第二次月考      |
   |       4     | 期末考          |
   +-------------+-----------------+
   ```

7. **Subjects 表**：
   - subject_id (int, 主键)
   - subject_name (varchar(255), 非空)
   
   示例数据：
   ```
   +------------+-------------+
   | subject_id | subject_name|
   +------------+-------------+
   |          1 | 语文        |
   |          2 | 数学        |
   |          3 | 英语        |
   |          4 | 物理        |
   |          5 | 化学        |
   +------------+-------------+
   ```

### 数据库结构更新规则

为确保数据库文档与实际结构保持同步，制定以下规则：

1. 当数据库表结构发生任何变更时，必须同步更新 [DATABASE_SCHEMA.md](file:///home/jimmy/repo/scout/DATABASE_SCHEMA.md) 文件
2. 所有字段命名应保持语义清晰且一致：
   - 学生相关字段使用 `student_` 前缀（如 student_name, student_id）
   - 教师相关字段使用 `teacher_` 前缀（如 teacher_name, teacher_id）
   - 科目相关字段使用 `subject_` 前缀（如 subject_name, subject_id）
   - 考试类型相关字段使用 `exam_type_` 前缀（如 exam_type_name, exam_type_id）
   - 班级相关字段使用 `class_` 前缀（如 class_name, class_id）
3. 所有表名和字段名应使用下划线分隔的命名方式，不使用驼峰命名
4. 每个表的主键应明确标识，并在文档中说明
5. 所有外键关系应在文档中明确说明
6. 当字段结构发生变化时，应同时更新本 README.md 中的示例数据

### 数据库视图命名规范

为保持数据库视图命名的一致性和可读性，制定以下规范：

1. 所有视图名称应使用小写字母
2. 多个单词之间使用下划线分隔，如 `student_scores`、`teacher_classes`
3. 视图名称应语义清晰，能够直观表达其包含的数据内容和主要用途
4. 在保持语义清晰的前提下，视图名称应尽量简洁
5. 视图名称应优先使用单个有意义的名词，如 `students`、`scores`、`teachers`
6. 当需要多个词组合时，应使用下划线分隔，如 `teacher_classes`、`class_counts`
7. 不使用任何前缀（如 `V_` 或 `vw_`）
8. 所有视图字段命名应与业务含义保持一致
9. 字段命名应使用中文，与业务含义保持一致
10. 相同语义的字段在不同视图中应保持相同命名
11. 使用 `_name` 后缀表示名称字段（如 `student_name`、`teacher_name`）
12. 使用 `_id` 后缀表示主键或外键字段
13. 使用 `_value` 后缀表示数值型字段
14. 使用 `_type` 或 `_type_name` 表示类型字段

### 数据导入

系统中的数据来自 [db/school_management.xlsx](file:///home/jimmy/repo/scout/db/school_management.xlsx) 文件，包含以下7个工作表：

1. **Classes** - 班级信息
2. **Teachers** - 教师信息
3. **TeacherClasses** - 教师班级关联信息
4. **Students** - 学生信息
5. **Scores** - 学生成绩信息
6. **ExamTypes** - 考试类型信息
7. **Subjects** - 科目信息

使用以下脚本将Excel数据导入到数据库：

```bash
cd db
python3 import_school_data.py
```

导入脚本会自动在db目录下查找 `school_management.xlsx` 文件，并将数据导入到数据库中。

也可以使用以下脚本将数据库数据导出到Excel文件：

```bash
cd db
python3 export_school_data.py
```

导出的Excel文件将保存在 `db` 目录下，包含两个文件：
- `school_management.xlsx` - 包含所有基础表数据
- `school_management_views.xlsx` - 包含所有视图数据

导入完成后，数据库中的数据量如下：
- Classes 表: 12 条记录
- Students 表: 360 条记录
- Teachers 表: 20 条记录
- Subjects 表: 6 条记录
- Scores 表: 8640 条记录
- ExamTypes 表: 4 条记录
- TeacherClasses 表: 72 条记录

### 数据分析结果

基于数据库中的数据，我们进行了以下分析：

#### 总体统计
- 数据库中共有7个表
- Scores表数据量最大，共31680条记录
- 总体平均分: 80.8分
- 分数范围: 60-100分

#### 各科目统计
| 科目 | 最低分 | 最高分 | 平均分 | 记录数 |
|------|--------|--------|--------|--------|
| 语文 | 60 | 100 | 80.72 | 2400 |
| 数学 | 60 | 100 | 80.86 | 2400 |
| 英语 | 60 | 100 | 81.23 | 2400 |
| 物理 | 60 | 100 | 80.85 | 2400 |
| 化学 | 60 | 100 | 79.82 | 2400 |
| 政治 | 60 | 100 | 81.34 | 2400 |

#### 各次考试统计
| 考试类型 | 最低分 | 最高分 | 平均分 | 记录数 |
|----------|--------|--------|--------|--------|
| 第一次月考 | 60 | 100 | 81.16 | 3600 |
| 期中考 | 60 | 100 | 79.94 | 3600 |
| 第二次月考 | 60 | 100 | 79.70 | 3600 |
| 期末考 | 70 | 95 | 82.43 | 3600 |

#### 班级人数分布
- 高三1班: 98人
- 高三2班: 56人
- 高三3班: 38人
- 高三4班: 50人

#### 教师任课情况
共有12名教师，每位教师教授2个班级，每位教师负责一个科目。

### 数据库视图

系统中创建了以下视图，用于数据分析和报告：

1. **exam_class** - 考试成绩等级分布
   - class_name: 班级名称
   - exam_type: 考试类型
   - A: A等级学生数量（年级前25%）
   - B: B等级学生数量（年级25%-50%）
   - C: C等级学生数量（年级50%-75%）
   - D: D等级学生数量（年级后25%）

2. **exam_results** - 考试结果
   - exam_type: 考试类型
   - student_name: 学生姓名
   - chinese: 语文成绩
   - math: 数学成绩
   - english: 英语成绩
   - physics: 物理成绩
   - chemistry: 化学成绩
   - politics: 政治成绩
   - total_score: 总分（该学生在该次考试中所有科目的分数总和）
   - ranking: 排名（在该次考试中的排名）

3. **teacher_performance** - 教师教学表现
   - teacher_name: 教师姓名
   - subject: 科目名称
   - class: 班级名称
   - average_score: 该教师在该班级该科目的平均分（去除最高分和最低分后计算）
   - highest_score: 该教师在该班级该科目的最高分
   - lowest_score: 该教师在该班级该科目的最低分
   - ranking: 该班级在该科目中的排名（按平均分排序，共12个班级）

4. **students** - 学生信息及班级
   - student_id: 学生ID
   - student_name: 学生姓名
   - class_name: 班级名称
   - password: 密码

5. **teachers** - 教师信息及科目
   - teacher_id: 教师ID
   - teacher_name: 教师姓名
   - subject_name: 科目名称
   - password: 密码

6. **scores** - 成绩详情
   - score_id: 成绩ID
   - student_name: 学生姓名
   - subject_name: 科目名称
   - exam_type_name: 考试类型名称
   - score_value: 分数

7. **teacher_classes** - 教师班级关系
   - teacher_name: 教师姓名
   - class_name: 班级名称

8. **teacher_counts** - 教师任课班级统计
   - teacher_name: 教师姓名
   - subject_name: 科目名称
   - class_count: 任课班级数量

这些视图基于基础表的数据进行计算，可以用于生成各类分析报告。

### 数据库备份

为了确保数据安全，建议定期备份整个数据库。备份文件存储在 `db/backup` 目录中。

#### 手动备份

使用以下命令创建数据库备份：

```bash
mkdir -p db/backup
mysqldump -u root -pNewuser1 school_management > db/backup/school_management_backup_$(date +"%Y%m%d_%H%M%S").sql
```

#### 使用备份脚本

项目提供了自动备份脚本，可以更方便地创建备份：

```bash
cd db
./backup_db.sh
```

该脚本会自动在 `db/backup` 目录中创建一个带有时间戳的备份文件。

你也可以指定备份文件名：

```bash
cd db
./backup_db.sh my_backup.sql
```

### 数据库恢复

当需要从备份文件恢复数据库时，可以使用以下方法：

#### 使用恢复脚本（推荐）

项目提供了自动恢复脚本，可以更方便地从备份恢复数据库：

```bash
cd db
./restore_db.sh
```

该脚本会列出 `db/backup` 目录中的所有备份文件，并让你选择要恢复的文件。

你也可以直接指定要恢复的备份文件：

```bash
cd db
./restore_db.sh school_management_backup_20250823_041033.sql
```

#### 手动恢复

使用以下命令从备份文件恢复数据库：

```bash
mysql -u root -pNewuser1 school_management < db/backup/school_management_backup_YYYYMMDD_HHMMSS.sql
```

**注意**：恢复操作会覆盖当前数据库中的所有数据，请谨慎操作。

## 2. Flask API 部分

在开发 Flask API 时，对于不同的数据实体，应根据其特性和可更新性选择使用基础表或视图。API 需要支持三种不同的用户角色：管理员、教师和学生，并为每种角色提供相应的权限和功能。

### 用户角色和权限

1. **管理员角色 (Admin)**
   - 管理学生信息（增删改查 students 表）
   - 管理教师信息（增删改查 teachers 表）
   - 管理班级信息（增删改查 classes 表）
   - 管理科目信息（增删改查 subjects 表）
   - 管理考试类型（增删改查 exam_types 表）
   - 管理教师班级关联关系（增删改查 teacher_classes 表）

2. **教师角色 (Teacher)**
   - 查看所教班级学生信息（读取 students 视图）
   - 导入和管理学生成绩（操作 scores 表和 scores 视图）
   - 查看班级成绩等级分布（读取 exam_class 视图）
   - 查看考试结果（读取 exam_results 视图）
   - 查看教学表现统计（读取 teacher_performance 视图）
   - 查看教师任课班级统计（读取 teacher_counts 视图）

3. **学生角色 (Student)**
   - 查看个人信息（读取 students 视图中的一条记录）
   - 查看个人成绩（读取 scores 视图中的一条记录）
   - 查看个人考试结果（读取 exam_results 视图中的一条记录）

### 前端页面对应 API 需求

根据前端页面设计，需要提供以下专门的 API 接口：

1. **考试成绩等级分布页面 (exam_class)**
   - `GET /api/exam-class` - 获取班级成绩等级分布数据
     - 支持查询参数：exam_type_id（考试类型）、class_id（班级）
     - 返回 exam_class 视图中的数据
   - `GET /api/exam-types` - 获取所有考试类型列表（用于下拉选择）
   - `GET /api/classes` - 获取所有班级列表（用于下拉选择）

2. **考试结果页面 (exam_result)**
   - `GET /api/exam-results` - 获取考试结果数据
     - 支持查询参数：exam_type_id（考试类型）、class_id（班级）
     - 返回 exam_results 视图中的数据
   - `GET /api/exam-types` - 获取所有考试类型列表（用于下拉选择）
   - `GET /api/classes` - 获取所有班级列表（用于下拉选择）

3. **教师表现页面 (teacher_performance)**
   - `GET /api/teacher-performance` - 获取教师教学表现数据
     - 支持查询参数：exam_type_id（考试类型）、teacher_id（教师）
     - 返回 teacher_performance 视图中的数据
   - `GET /api/exam-types` - 获取所有考试类型列表（用于下拉选择）
   - `GET /api/teachers` - 获取所有教师列表（用于下拉选择）

4. **管理员修改功能**
   - 需要完整的 CRUD API 接口来管理学生、教师、班级、科目、考试类型等基础数据
   - 包括 POST、GET、PUT、DELETE 等操作

5. **教师查看功能**
   - 需要只读 API 接口来获取教师所教班级的相关数据
   - 包括 GET 操作，但限制只能访问教师所教班级的数据

### 可直接使用视图进行 CRUD 操作的实体：

1. **scores 视图**
   - **可更新性**：是，已验证
   - **优点**：提供描述性字段名 (student_name, subject_name, exam_type_name, score_value)
   - **适用场景**：成绩管理的完整 CRUD 操作

2. **teachers 视图**
   - **可更新性**：部分，基础字段可更新
   - **优点**：提供 teacher_name 和 subject_name 而不是 ID
   - **适用场景**：教师信息查询和基本更新

3. **students 视图**
   - **可更新性**：部分，基础字段可更新
   - **优点**：提供 student_name 和 class_name 而不是 ID
   - **适用场景**：学生信息查询和基本更新

### 必须使用基础表进行 CRUD 操作的实体：

1. **Classes 表**
   - **原因**：对应的 students 视图包含多表连接，无法直接更新
   - **适用场景**：班级信息的完整 CRUD 操作

2. **Students 表**
   - **原因**：虽然 students 视图可部分更新，但复杂操作需要使用基础表
   - **适用场景**：学生信息的完整 CRUD 操作，特别是涉及 class_id 的操作

3. **Teachers 表**
   - **原因**：虽然 teachers 视图可部分更新，但复杂操作需要使用基础表
   - **适用场景**：教师信息的完整 CRUD 操作，特别是涉及 subject_id 的操作

4. **Subjects 表**
   - **原因**：没有对应的可更新视图
   - **适用场景**：科目信息的完整 CRUD 操作

5. **ExamTypes 表**
   - **原因**：没有对应的可更新视图
   - **适用场景**：考试类型信息的完整 CRUD 操作

6. **TeacherClasses 表**
   - **原因**：对应的 teacher_classes 视图无法更新
   - **适用场景**：教师和班级关联关系的完整 CRUD 操作

7. **Scores 表**
   - **原因**：虽然 scores 视图可更新，但在某些复杂场景下直接操作基础表更可靠
   - **适用场景**：作为 scores 视图的备选方案

### 只能用于查询的视图（包含聚合或复杂计算）：

1. **exam_class** - 包含聚合函数和复杂计算
2. **exam_results** - 包含聚合函数和复杂计算
3. **teacher_counts** - 包含聚合函数
4. **teacher_performance** - 包含聚合函数和复杂计算
5. **users** - 包含 UNION 操作

这些视图仅适用于查询和报告场景，不能用于更新操作。

### 建议的 Flask API 设计策略：

1. **对于 scores**：优先使用 scores 视图进行所有 CRUD 操作
2. **对于 teachers 和 students**：查询使用视图，创建/更新操作可选择使用视图或基础表
3. **对于 teacher_classes 关联**：查询使用 teacher_classes 视图，创建/删除使用 TeacherClasses 基础表
4. **对于其他实体**：使用基础表进行 CRUD 操作
5. **对于分析报告类视图**：仅用于查询操作

### API 路由规划

- **认证相关**
  - `POST /api/auth/login` - 用户登录
  - `POST /api/auth/logout` - 用户登出
  - `GET /api/auth/profile` - 获取当前用户信息

- **管理员专用**
  - `GET /api/admin/students` - 获取所有学生信息
  - `POST /api/admin/students` - 创建学生
  - `PUT /api/admin/students/<id>` - 更新学生信息
  - `DELETE /api/admin/students/<id>` - 删除学生
  - `GET /api/admin/teachers` - 获取所有教师信息
  - `POST /api/admin/teachers` - 创建教师
  - `PUT /api/admin/teachers/<id>` - 更新教师信息
  - `DELETE /api/admin/teachers/<id>` - 删除教师

- **教师专用**
  - `GET /api/teacher/students` - 获取所教班级的学生信息
  - `GET /api/teacher/scores` - 获取所教班级的成绩
  - `POST /api/teacher/scores` - 录入成绩
  - `PUT /api/teacher/scores/<id>` - 更新成绩
  - `GET /api/teacher/exam-class` - 获取班级成绩等级分布
  - `GET /api/teacher/exam-results` - 获取考试结果
  - `GET /api/teacher/performance` - 获取教学表现统计

- **学生专用**
  - `GET /api/student/profile` - 获取个人信息
  - `GET /api/student/scores` - 获取个人成绩
  - `GET /api/student/exam-results` - 获取个人考试结果

- **通用查询**
  - `GET /api/classes` - 获取班级列表
  - `GET /api/subjects` - 获取科目列表
  - `GET /api/exam-types` - 获取考试类型列表

## 3. Web 前端部分

Web 前端部分将使用 Angular 框架开发，采用 Angular Material 组件库构建用户界面，提供现代化、响应式的用户交互体验。

### 技术栈

- Angular (版本待定)
- Angular Material UI 组件库
- TypeScript
- HTML5/CSS3
- RxJS（用于响应式编程）

### 功能规划

前端将实现以下功能模块，按照不同用户角色划分：

1. **管理员角色 (Admin)**
   - 管理学生信息（增删改查）
   - 管理教师信息（增删改查）
   - 管理班级信息
   - 管理科目和考试类型
   - 数据导入/导出功能
   - 系统配置管理

2. **教师角色 (Teacher)**
   - 查看所教班级学生信息
   - 导入和管理学生成绩（操作 scores 表）
   - 查看班级成绩等级分布（exam_class 视图）
   - 查看考试结果（exam_results 视图）
   - 查看教学表现统计（teacher_performance 视图）
   - 查看教师任课班级统计（teacher_counts 视图）
   - 导出成绩报表

3. **学生角色 (Student)**
   - 查看个人信息（students 视图中的一条记录）
   - 查看个人成绩（scores 视图中的一条记录）
   - 查看个人考试结果（exam_results 视图中的一条记录）
   - 查看个人排名信息

### Angular Material 控件使用规划

前端将广泛使用 Angular Material 组件来构建用户界面，主要控件包括：

1. **导航组件**
   - MatToolbar - 页面顶部工具栏
   - MatSidenav - 侧边导航栏，用于角色功能菜单
   - MatMenu - 下拉菜单，用于用户操作选项

2. **表单控件**
   - MatSelect - 下拉选择框，用于考试类型、班级、教师等筛选
   - MatInputModule - 输入框，用于登录和数据录入
   - MatDatepicker - 日期选择器，用于时间相关筛选
   - MatCheckbox - 复选框，用于多选操作
   - MatRadioGroup - 单选按钮组，用于选项选择

3. **数据展示组件**
   - MatTable - 表格组件，用于展示成绩、学生、教师等数据
   - MatPaginator - 分页器，用于处理大量数据的分页显示
   - MatSort - 排序功能，用于表格列排序
   - MatCard - 卡片组件，用于信息展示区域

4. **反馈组件**
   - MatSnackBar - 消息提示，用于操作反馈
   - MatDialog - 对话框，用于确认操作或详细信息展示
   - MatProgressSpinner - 加载指示器，用于异步操作等待

5. **按钮与指示器**
   - MatButtonModule - 按钮组件，用于各种操作按钮
   - MatIconModule - 图标组件，用于界面图标展示
   - MatTooltip - 工具提示，用于元素说明信息

### 与后端交互

前端将通过 RESTful API 与 Flask 后端进行通信：

- 使用 Angular HttpClient 进行 API 调用
- 实现统一的错误处理机制
- 使用环境配置管理不同环境的 API 地址

### 开发规范

- 遵循 Angular 官方风格指南
- 使用 TypeScript 严格模式
- 组件化开发，提高代码复用性
- 实现响应式设计，适配不同屏幕尺寸
- 遵循 Angular Material 设计规范，确保界面一致性
- 使用 Angular Reactive Forms 进行表单处理

### 待办事项

- [ ] 创建 Angular 项目结构
- [ ] 设计 UI/UX 原型
- [ ] 实现用户认证模块
- [ ] 实现管理员功能模块
- [ ] 实现教师功能模块
- [ ] 实现学生功能模块
- [ ] 编写单元测试
- [ ] 部署配置
