# School Management System - Database Schema

## Overview

This document describes the database schema for the School Management System. The database name is `school_management` and contains 7 tables that store information about classes, students, teachers, subjects, scores, exam types, and the relationship between teachers and classes.

## Database Tables

### 1. Classes Table

Stores information about school classes.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
class_id | int | NO | PRI | NULL | auto_increment
class_name | varchar(255) | NO |  | NULL | 

- **Primary Key**: class_id
- **Record Count**: 40

### 2. Students Table

Stores information about students.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
student_id | varchar(255) | NO | PRI | NULL | 
student_name | varchar(255) | NO | MUL | NULL | 
class_id | int | NO | MUL | NULL | 
password | varchar(255) | YES |  | NULL | 

- **Primary Key**: student_id
- **Foreign Key**: class_id references Classes(class_id)
- **Index**: student_name (for searching students by name)
- **Record Count**: 120

### 3. Teachers Table

Stores information about teachers.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
teacher_id | int | NO | PRI | NULL | auto_increment
teacher_name | varchar(255) | NO | MUL |  | NULL | 
subject_id | int | NO | MUL | NULL | 

- **Primary Key**: teacher_id
- **Foreign Key**: subject_id references Subjects(subject_id)
- **Index**: teacher_name (for searching teachers by name)
- **Record Count**: 144

### 4. Subjects Table

Stores information about subjects.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
subject_id | int | NO | PRI | NULL | 
subject_name | varchar(255) | NO | UNI | NULL | 

- **Primary Key**: subject_id
- **Unique Constraint**: subject_name
- **Record Count**: 6

### 5. Scores Table

Stores student scores for various subjects and exam types.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
score_id | int | NO | PRI | NULL | auto_increment
student_id | varchar(255) | NO | MUL | NULL | 
subject_id | int | NO | MUL | NULL | 
exam_type_id | int | NO | MUL | NULL | 
score_value | decimal(5,2) | YES |  | NULL | 

- **Primary Key**: score_id
- **Foreign Keys**: 
  - student_id references Students(student_id)
  - subject_id references Subjects(subject_id)
  - exam_type_id references ExamTypes(exam_type_id)
- **Composite Indexes**:
  - (student_id, subject_id) for querying specific student's scores in specific subjects
  - (subject_id, exam_type_id) for querying scores of specific subject and exam type
  - (exam_type_id, subject_id) for querying scores of specific exam type and subject
- **Check Constraint**: score_value should be between 0 and 100
- **Record Count**: 31,680

### 6. ExamTypes Table

Stores information about different exam types.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
exam_type_id | int | NO | PRI | NULL | auto_increment
exam_type_name | varchar(255) | NO | UNI | NULL | 

- **Primary Key**: exam_type_id
- **Unique Constraint**: exam_type_name
- **Record Count**: 8

### 7. TeacherClasses Table

Stores the many-to-many relationship between teachers and classes.

Column Name | Data Type | Null | Key | Default | Extra
-------------|-----------|------|-----|---------|-------
teacher_id | int | NO | MUL | NULL | 
class_id | int | NO | MUL | NULL | 

- **Foreign Keys**:
  - teacher_id references Teachers(teacher_id)
  - class_id references Classes(class_id)
- **Unique Constraint**: (teacher_id, class_id) to prevent duplicate assignments
- **Record Count**: 192

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
7. **Scores.exam_type_id** → **ExamTypes.exam_type_id**

## Data Summary

Table | Record Count
-------|--------------
Classes | 40
Students | 120
Teachers | 144
Subjects | 6
Scores | 31,680
ExamTypes | 8
TeacherClasses | 192

The Scores table contains the largest amount of data, which is expected as each student has multiple scores across different subjects and exam types.