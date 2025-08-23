# School Management System - Database Schema

## Overview

This document describes the database schema for the School Management System. The database name is `school_management` and contains 7 tables that store information about classes, students, teachers, subjects, scores, exam types, and the relationship between teachers and classes.

## Database Tables

### 1. Classes Table

Stores information about school classes.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
class_id | int | NO | PRI | NULL | auto_increment
class_name | varchar(255) | YES |  | NULL | 

- **Primary Key**: class_id
- **Record Count**: 12

### 2. Students Table

Stores information about students.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
student_id | varchar(255) | NO | PRI | NULL | 
student_name | varchar(255) | YES |  | NULL | 
class_id | int | YES | MUL | NULL | 
password | varchar(255) | YES |  | NULL | 

- **Primary Key**: student_id
- **Foreign Key**: class_id references Classes(class_id)
- **Record Count**: 360

### 3. Teachers Table

Stores information about teachers.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
teacher_id | int | NO | PRI | NULL | auto_increment
teacher_name | varchar(255) | YES |  | NULL | 
subject_id | int | NO | MUL | NULL | 
password | varchar(255) | YES |  | NULL | 

- **Primary Key**: teacher_id
- **Foreign Key**: subject_id references Subjects(subject_id)
- **Record Count**: 20

### 4. Subjects Table

Stores information about subjects.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
subject_id | int | NO | PRI | NULL | 
subject_name | varchar(255) | YES |  | NULL | 

- **Primary Key**: subject_id
- **Record Count**: 6

### 5. Scores Table

Stores student scores for various subjects and exam types.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
score_id | int | NO | PRI | NULL | auto_increment
student_id | varchar(255) | YES | MUL | NULL | 
subject_id | int | YES | MUL | NULL | 
exam_type_id | int | YES | MUL | NULL | 
score | int | YES |  | NULL | 

- **Primary Key**: score_id
- **Foreign Keys**: 
  - student_id references Students(student_id)
  - subject_id references Subjects(subject_id)
  - exam_type_id references ExamTypes(type_id)
- **Record Count**: 8640

### 6. ExamTypes Table

Stores different types of exams.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
type_id | int | NO | PRI | NULL | auto_increment
exam_type_name | varchar(255) | YES | UNI | NULL | 

- **Primary Key**: type_id
- **Record Count**: 4

### 7. teacher_classes Table

Stores the relationship between teachers and classes.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
teacher_id | int | YES | MUL | NULL | 
class_id | int | YES | MUL | NULL | 

- **Foreign Keys**: 
  - teacher_id references Teachers(teacher_id)
  - class_id references Classes(class_id)
- **Record Count**: 72

## Database Views

### 1. exam_class View

Shows the grade distribution (A, B, C, D) for each class in each exam type.

Column Name | Description
------------|------------
class_name | Name of the class
exam_type | Type of exam
A | Count of students with A grade (top 25%)
B | Count of students with B grade (25%-50%)
C | Count of students with C grade (50%-75%)
D | Count of students with D grade (bottom 25%)

### 2. exam_results View

Shows student scores for each subject and exam type, with total scores and rankings.

Column Name | Description
------------|------------
exam_type | Type of exam
student_name | Name of the student
chinese | Chinese score
math | Math score
english | English score
physics | Physics score
chemistry | Chemistry score
politics | Politics score
total_score | Total score across all subjects
ranking | Ranking within the exam type

### 3. scores View

Shows detailed score information with descriptive names.

Column Name | Description
------------|------------
score_id | Score identifier
student_name | Name of the student
subject_name | Name of the subject
exam_type_name | Name of the exam type
score_value | Actual score value

### 4. students View

Shows student information with class names.

Column Name | Description
------------|------------
student_id | Student identifier
student_name | Name of the student
class_name | Name of the class
password | Student password

### 5. teacher_classes View

Shows teacher-class relationships with descriptive names.

Column Name | Description
------------|------------
teacher_name | Name of the teacher
class_name | Name of the class

### 6. teacher_counts View

Shows how many classes each teacher teaches.

Column Name | Description
------------|------------
teacher_name | Name of the teacher
subject_name | Name of the subject taught
class_count | Number of classes taught

### 7. teacher_performance View

Shows teacher performance metrics including average scores (excluding highest and lowest), highest score, lowest score, and ranking for each exam type.

Column Name | Description
------------|------------
teacher_name | Name of the teacher
subject | Subject taught
class | Class name
exam_type_name | Name of the exam type
average_score | Average score (excluding highest and lowest)
highest_score | Highest score in the class
lowest_score | Lowest score in the class
ranking | Ranking among teachers of the same subject and exam type

### 8. teachers View

Shows teacher information with subject names.

Column Name | Description
------------|------------
teacher_id | Teacher identifier
teacher_name | Name of the teacher
subject_name | Name of the subject taught
password | Teacher password

### 9. users View

Shows all users (students, teachers, and admin) in a unified view for authentication.

Column Name | Description
------------|------------
user_id | User identifier
user_name | Name of the user
password | User password
role | Role of the user (student, teacher, or admin)

## Entity Relationship Diagram

```
Classes ||--o{ Students : "1 class has many students"
Classes }o--o{ TeacherClasses : "many-to-many relationship"
Teachers }o--o{ TeacherClasses : "many-to-many relationship"
Teachers }|--o{ Subjects : "many teachers can teach 1 subject"
Students ||--o{ Scores : "1 student has many scores"
Scores }|--o{ Subjects : "many scores for 1 subject"
Scores }|--o{ ExamTypes : "many scores for 1 exam type"
```

## Foreign Key Constraints

1. **Students.class_id** → **Classes.class_id**
2. **Scores.student_id** → **Students.student_id**
3. **TeacherClasses.teacher_id** → **Teachers.teacher_id**
4. **TeacherClasses.class_id** → **Classes.class_id**
5. **Teachers.subject_id** → **Subjects.subject_id**
6. **Scores.subject_id** → **Subjects.subject_id**
7. **Scores.exam_type_id** → **ExamTypes.type_id**

## Data Summary

Table | Record Count
-------|--------------
Classes | 12
Students | 360
Teachers | 20
Subjects | 6
Scores | 8640
ExamTypes | 4
TeacherClasses | 72

The Scores table contains the largest amount of data, which is expected as each student has multiple scores across different subjects and exam types.

# 数据库结构文档

## Classes 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| class_id | int | 主键，自动递增 | 班级ID |
| class_name | varchar(255) | 非空 | 班级名称 |

### 示例数据
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

## Teachers 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| teacher_id | int | 主键，自动递增 | 教师ID |
| teacher_name | varchar(255) | 非空 | 教师姓名 |
| subject_id | int | 非空，外键 | 所教科目ID，引用Subjects.subject_id |
| password | varchar(255) | 可为空 | 密码 |

### 示例数据
```
+------------+-------------+------------+----------+
| teacher_id | teacher_name| subject_id | password |
+------------+-------------+------------+----------+
|          1 | 王老师      |          1 | NULL     |
|          2 | 李老师      |          2 | NULL     |
|          3 | 张老师      |          3 | NULL     |
|          4 | 胡老师      |          4 | NULL     |
|          5 | 赵老师      |          5 | NULL     |
+------------+-------------+------------+----------+
```

## TeacherClasses 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| teacher_id | int | 主键的一部分，外键 | 教师ID，引用Teachers.teacher_id |
| class_id | int | 主键的一部分，外键 | 班级ID，引用Classes.class_id |

### 示例数据
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

## Students 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| student_id | varchar(255) | 主键 | 学生ID |
| student_name | varchar(255) | 非空 | 学生姓名 |
| class_id | int | 非空，外键 | 所在班级ID，引用Classes.class_id |
| password | varchar(255) | 可为空 | 密码 |

### 示例数据
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

## Scores 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| score_id | int | 主键，自动递增 | 成绩ID |
| student_id | varchar(255) | 外键 | 学生ID，引用Students.student_id |
| subject_id | int | 外键 | 科目ID，引用Subjects.subject_id |
| exam_type_id | int | 外键 | 考试类型ID，引用ExamTypes.type_id |
| score | int | 可为空 | 分数 |

### 示例数据
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

## ExamTypes 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| type_id | int | 主键，自动递增 | 考试类型ID |
| exam_type_name | varchar(255) | 非空，唯一 | 考试类型名称 |

### 示例数据
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

## Subjects 表

### 表结构
| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| subject_id | int | 主键 | 科目ID |
| subject_name | varchar(255) | 非空 | 科目名称 |

### 示例数据
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

