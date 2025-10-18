# 学校管理系统数据库


## 数据库连接信息
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Newuser1'
    MYSQL_DB = 'school_management'

## 系统信息
操作系统：Ubuntu Linux
数据库服务器：MySQL 8.4.6-0ubuntu0.25.04.1

## AI规则
**重要规则：AI助手必须始终用中文回复用户，所有文档和注释也必须使用中文。**

## 数据库概览

### 表记录统计
| 表名 | 记录数量 | 说明 |
|------|----------|------|
| Classes | 12 | 班级表 |
| Students | 360 | 学生表 |
| Teachers | 20 | 教师表 |
| Subjects | 6 | 科目表 |
| ExamTypes | 4 | 考试类型表 |
| Scores | 8,640 | 成绩表 |
| TeacherClasses | 72 | 教师班级关联表 |

## 数据库表完整定义

### Classes (班级表)
```sql
CREATE TABLE `Classes` (
  `class_id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `class_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### Students (学生表)
```sql
CREATE TABLE `Students` (
  `student_id` varchar(255) NOT NULL,
  `student_name` varchar(255) DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  KEY `fk_students_class_id` (`class_id`),
  CONSTRAINT `fk_students_class_id` FOREIGN KEY (`class_id`) REFERENCES `Classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### Teachers (教师表)
```sql
CREATE TABLE `Teachers` (
  `teacher_id` int NOT NULL AUTO_INCREMENT,
  `teacher_name` varchar(255) DEFAULT NULL,
  `subject_id` int NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  KEY `subject_id` (`subject_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### Subjects (科目表)
```sql
CREATE TABLE `Subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`subject_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### ExamTypes (考试类型表)
```sql
CREATE TABLE `ExamTypes` (
  `exam_type_id` int NOT NULL AUTO_INCREMENT,
  `exam_type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`exam_type_id`),
  UNIQUE KEY `exam_type` (`exam_type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### Scores (成绩表)
```sql
CREATE TABLE `Scores` (
  `score_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(255) DEFAULT NULL,
  `subject_id` int DEFAULT NULL,
  `exam_type_id` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`score_id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  KEY `exam_type_id` (`exam_type_id`),
  CONSTRAINT `Scores_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Students` (`student_id`),
  CONSTRAINT `Scores_ibfk_3` FOREIGN KEY (`exam_type_id`) REFERENCES `ExamTypes` (`exam_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8651 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### TeacherClasses (教师班级关联表)
```sql
CREATE TABLE `TeacherClasses` (
  `teacher_id` int NOT NULL,
  `class_id` int NOT NULL,
  PRIMARY KEY (`teacher_id`,`class_id`),
  KEY `fk_teacher_classes_teacher_id` (`teacher_id`),
  KEY `fk_teacher_classes_class_id` (`class_id`),
  CONSTRAINT `fk_teacher_classes_class_id` FOREIGN KEY (`class_id`) REFERENCES `Classes` (`class_id`),
  CONSTRAINT `fk_teacher_classes_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `Teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## 数据库视图完整定义

### exam_class (班级考试视图)
```sql
SELECT 
  `student_grades`.`class_name` AS `class_name`,
  `student_grades`.`exam_type` AS `exam_type`,
  SUM(CASE WHEN (`student_grades`.`total_score` >= 90) THEN 1 ELSE 0 END) AS `A_count`,
  SUM(CASE WHEN ((`student_grades`.`total_score` >= 80) AND (`student_grades`.`total_score` < 90)) THEN 1 ELSE 0 END) AS `B_count`,
  SUM(CASE WHEN ((`student_grades`.`total_score` >= 70) AND (`student_grades`.`total_score` < 80)) THEN 1 ELSE 0 END) AS `C_count`,
  SUM(CASE WHEN (`student_grades`.`total_score` < 70) THEN 1 ELSE 0 END) AS `D_count`
FROM (
  SELECT 
    `c`.`class_name` AS `class_name`,
    `et`.`exam_type_name` AS `exam_type`,
    `s`.`student_id` AS `student_id`,
    `s`.`student_name` AS `student_name`,
    SUM(`sc`.`score`) AS `total_score`
  FROM 
    ((`Students` `s` JOIN `Classes` `c` ON ((`s`.`class_id` = `c`.`class_id`))) 
    JOIN `Scores` `sc` ON ((`s`.`student_id` = `sc`.`student_id`))) 
    JOIN `ExamTypes` `et` ON ((`sc`.`exam_type_id` = `et`.`exam_type_id`))
  GROUP BY `c`.`class_name`, `et`.`exam_type_name`, `s`.`student_id`, `s`.`student_name`
) `student_grades`
GROUP BY `student_grades`.`class_name`, `student_grades`.`exam_type`
ORDER BY `student_grades`.`class_name`, `student_grades`.`exam_type`;
```

### exam_results (考试结果视图)
```sql
SELECT 
  `s`.`student_id` AS `student_id`,
  `s`.`student_name` AS `student_name`,
  `c`.`class_name` AS `class_name`,
  `et`.`exam_type_name` AS `exam_type`,
  `sub`.`subject_name` AS `subject_name`,
  `sc`.`score` AS `subject_score`,
  (SELECT SUM(`s2`.`score`) 
   FROM ((`Scores` `s2` JOIN `ExamTypes` `et2` ON ((`s2`.`exam_type_id` = `et2`.`exam_type_id`))) 
   JOIN `Subjects` `sub2` ON ((`s2`.`subject_id` = `sub2`.`subject_id`))) 
   WHERE ((`s2`.`student_id` = `s`.`student_id`) AND (`et2`.`exam_type_name` = `et`.`exam_type_name`))) AS `total_score`,
  (SELECT rank() OVER (ORDER BY SUM(`s2`.`score`) DESC) 
   FROM ((`Scores` `s2` JOIN `ExamTypes` `et2` ON ((`s2`.`exam_type_id` = `et2`.`exam_type_id`))) 
   JOIN `Subjects` `sub2` ON ((`s2`.`subject_id` = `sub2`.`subject_id`))) 
   WHERE (`et2`.`exam_type_name` = `et`.`exam_type_name`) 
   GROUP BY `s2`.`student_id`) AS `rank_in_exam`
FROM 
  ((((`Students` `s` JOIN `Classes` `c` ON ((`s`.`class_id` = `c`.`class_id`))) 
  JOIN `Scores` `sc` ON ((`s`.`student_id` = `sc`.`student_id`))) 
  JOIN `ExamTypes` `et` ON ((`sc`.`exam_type_id` = `et`.`exam_type_id`))) 
  JOIN `Subjects` `sub` ON ((`sc`.`subject_id` = `sub`.`subject_id`)));
```

### scores (成绩视图)
```sql
SELECT 
  `s`.`student_id` AS `student_id`,
  `s`.`student_name` AS `student_name`,
  `c`.`class_name` AS `class_name`,
  `sub`.`subject_name` AS `subject_name`,
  `et`.`exam_type_name` AS `exam_type_name`,
  `sc`.`score` AS `score`
FROM 
  ((((`Students` `s` JOIN `Classes` `c` ON ((`s`.`class_id` = `c`.`class_id`))) 
  JOIN `Scores` `sc` ON ((`s`.`student_id` = `sc`.`student_id`))) 
  JOIN `Subjects` `sub` ON ((`sc`.`subject_id` = `sub`.`subject_id`))) 
  JOIN `ExamTypes` `et` ON ((`sc`.`exam_type_id` = `et`.`exam_type_id`)));
```

### students (学生视图)
```sql
SELECT 
  `s`.`student_id` AS `student_id`,
  `s`.`student_name` AS `student_name`,
  `c`.`class_name` AS `class_name`,
  `s`.`password` AS `password`
FROM (`Students` `s` JOIN `Classes` `c` ON ((`s`.`class_id` = `c`.`class_id`)));
```

### teacher_classes (教师班级视图)
```sql
SELECT 
  `t`.`teacher_id` AS `teacher_id`,
  `t`.`teacher_name` AS `teacher_name`,
  `sub`.`subject_name` AS `subject_name`,
  `c`.`class_name` AS `class_name`
FROM 
  (((`Teachers` `t` JOIN `Subjects` `sub` ON ((`t`.`subject_id` = `sub`.`subject_id`))) 
  JOIN `TeacherClasses` `tc` ON ((`t`.`teacher_id` = `tc`.`teacher_id`))) 
  JOIN `Classes` `c` ON ((`tc`.`class_id` = `c`.`class_id`)));
```

### teacher_counts (教师统计视图)
```sql
SELECT 
  `t`.`teacher_id` AS `teacher_id`,
  `t`.`teacher_name` AS `teacher_name`,
  `sub`.`subject_name` AS `subject_name`,
  COUNT(`tc`.`class_id`) AS `class_count`
FROM 
  ((`Teachers` `t` JOIN `Subjects` `sub` ON ((`t`.`subject_id` = `sub`.`subject_id`))) 
  JOIN `TeacherClasses` `tc` ON ((`t`.`teacher_id` = `tc`.`teacher_id`)))
GROUP BY `t`.`teacher_id`, `t`.`teacher_name`, `sub`.`subject_name`;
```

### teacher_performance (教师绩效视图)
```sql
SELECT 
  `t`.`teacher_id` AS `teacher_id`,
  `t`.`teacher_name` AS `teacher_name`,
  `s`.`subject_id` AS `subject_id`,
  `s`.`subject_name` AS `subject_name`,
  `c`.`class_id` AS `class_id`,
  `c`.`class_name` AS `class_name`,
  `et`.`exam_type_id` AS `exam_type_id`,
  `et`.`exam_type_name` AS `exam_type_name`,
  AVG(`sc`.`score`) AS `average_score`,
  row_number() OVER (PARTITION BY `s`.`subject_id`, `et`.`exam_type_id` ORDER BY avg(`sc`.`score`) DESC) AS `rank_in_subject`,
  row_number() OVER (PARTITION BY `et`.`exam_type_id` ORDER BY avg(`sc`.`score`) DESC) AS `rank_in_school`
FROM 
  (((((`Teachers` `t` JOIN `Subjects` `s` ON ((`t`.`subject_id` = `s`.`subject_id`))) 
  JOIN `TeacherClasses` `tc` ON ((`t`.`teacher_id` = `tc`.`teacher_id`))) 
  JOIN `Classes` `c` ON ((`tc`.`class_id` = `c`.`class_id`))) 
  JOIN `Students` `st` ON ((`c`.`class_id` = `st`.`class_id`))) 
  JOIN `Scores` `sc` ON ((`st`.`student_id` = `sc`.`student_id`))) 
  JOIN `ExamTypes` `et` ON ((`sc`.`exam_type_id` = `et`.`exam_type_id`)))
GROUP BY `t`.`teacher_id`, `t`.`teacher_name`, `s`.`subject_id`, `s`.`subject_name`, `c`.`class_id`, `c`.`class_name`, `et`.`exam_type_id`, `et`.`exam_type_name`;
```

### teachers (教师视图)
```sql
SELECT 
  `t`.`teacher_id` AS `teacher_id`,
  `t`.`teacher_name` AS `teacher_name`,
  `sub`.`subject_name` AS `subject_name`,
  `t`.`password` AS `password`
FROM (`Teachers` `t` JOIN `Subjects` `sub` ON ((`t`.`subject_id` = `sub`.`subject_id`)));
```

### users (用户视图)
```sql
SELECT 
  `students`.`student_id` AS `user_id`,
  `students`.`student_name` AS `user_name`,
  `students`.`password` AS `password`,
  'student' AS `role`
FROM `students`
UNION ALL
SELECT 
  `teachers`.`teacher_id` AS `user_id`,
  `teachers`.`teacher_name` AS `user_name`,
  `teachers`.`password` AS `password`,
  'teacher' AS `role`
FROM `teachers`
UNION ALL
SELECT 
  'admin' AS `user_id`,
  'admin' AS `user_name`,
  'admin' AS `password`,
  'admin' AS `role`;
```

## 数据关系说明

### 主要关系
1. **学生-班级关系**：每个学生属于一个班级（多对一）
2. **教师-科目关系**：每个教师负责一个科目（多对一）
3. **教师-班级关系**：教师可以教授多个班级，每个班级可以有多个教师（多对多）
4. **成绩关系**：每个学生在每个科目的每种考试类型下都有成绩记录

### 数据完整性
- 所有外键关系都已正确建立
- 数据统计验证：360名学生 × 6个科目 × 4种考试类型 = 8,640条成绩记录
- 教师分配：20名教师对应6个科目，部分科目有多名教师

## 视图功能说明

### 分析类视图
- **exam_class**: 班级考试成绩分布分析，按等级统计
- **exam_results**: 学生考试结果详情，包含排名信息
- **teacher_performance**: 教师绩效分析，包含科目内和全校排名

### 信息类视图
- **scores**: 成绩详细信息，关联所有相关表
- **students**: 学生基本信息，包含班级名称
- **teachers**: 教师基本信息，包含科目名称
- **teacher_classes**: 教师班级分配情况
- **teacher_counts**: 教师教授班级数量统计

### 系统类视图
- **users**: 统一用户视图，整合学生、教师和管理员账户

## 数据库恢复脚本使用说明

### 恢复命令示例

#### 恢复到默认数据库（school_management）
```bash
# 恢复到默认 school_management 数据库，使用最新备份文件，自动确认
./restore_db.sh --auto --latest
```
**说明**: 此命令将最新的备份文件恢复到默认的 `school_management` 数据库，无需用户确认。

#### 恢复到测试数据库（school_management_test）
```bash
# 恢复到 school_management_test 数据库，使用最新备份文件，自动确认
./restore_db.sh --latest school_management_test --auto
```
**说明**: 此命令将最新的备份文件恢复到测试数据库 `school_management_test`，无需用户确认。

### 命令参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--auto` | 自动确认模式，跳过用户确认提示 | `--auto` |
| `--latest` | 自动选择最新的备份文件 | `--latest` |
| `[数据库名]` | 指定目标数据库名称 | `school_management_test` |

### 使用场景建议

- **开发/测试环境**: 推荐使用第二个命令，恢复到 `school_management_test` 数据库
- **生产环境恢复**: 使用第一个命令，恢复到 `school_management` 数据库
- **数据验证**: 建议先恢复到测试数据库验证数据完整性，确认无误后再恢复到生产数据库

### 安全注意事项

1. **数据覆盖警告**: 恢复操作将覆盖目标数据库中的所有现有数据
2. **备份建议**: 在执行恢复前，建议先备份当前数据库
3. **权限要求**: 确保执行脚本的用户有足够的数据库操作权限
4. **连接检查**: 脚本会自动检查MySQL连接状态，确保数据库服务正常运行

## 最后更新时间
2025年6月20日 - 根据实际数据库结构验证并更新，添加完整表和视图定义及数据库恢复脚本使用说明