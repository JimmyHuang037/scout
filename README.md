# 学生成绩管理系统

## 数据库连接信息

使用以下命令连接到MySQL数据库：

```bash
mysql -u root -p Newuser1
```

默认数据库为 `school_management`。

## 数据库结构文档

有关详细的数据库表结构信息，请参阅 [DATABASE_SCHEMA.md](file:///home/jimmy/repo/scout/DATABASE_SCHEMA.md) 文件。

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

3. **teacher_classes 表**：
   - teacher_id (int, 非空, 外键引用Teachers.teacher_id)
   - class_id (int, 非空, 外键引用Classes.class_id)
   
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

系统中的数据来自 [school_management_data.xlsx](file:///home/jimmy/repo/scout/school_management_data.xlsx) 文件，包含以下7个工作表：

1. **Classes** - 班级信息
2. **Teachers** - 教师信息
3. **TeacherClasses** - 教师班级关联信息
4. **Students** - 学生信息
5. **Scores** - 学生成绩信息
6. **ExamTypes** - 考试类型信息
7. **Subjects** - 科目信息

使用以下脚本将Excel数据导入到数据库：

```bash
python3 import_school_data.py
```

也可以使用以下脚本将数据库数据导出到Excel文件：

```bash
python3 export_school_data.py
```

导入完成后，数据库中的数据量如下：
- Classes 表: 12 条记录
- Students 表: 360 条记录
- Teachers 表: 20 条记录
- Subjects 表: 6 条记录
- Scores 表: 8640 条记录
- ExamTypes 表: 4 条记录
- TeacherClasses 表: 50 条记录

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

## 数据库视图

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

## Flask API 开发指南

在开发 Flask API 时，对于不同的数据实体，应根据其特性和可更新性选择使用基础表或视图：

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
