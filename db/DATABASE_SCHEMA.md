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