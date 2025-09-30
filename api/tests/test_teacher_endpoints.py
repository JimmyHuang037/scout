#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

from .test_curl_base import CurlTestBase
from config import Config
import os


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类 - 无需登录和会话的测试"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.test_results_dir = Config.TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "teacher_curl_commands.log")
        
        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
        }

    def test_01_get_exam_classes(self):
        """测试用例1: 教师获取任教班级列表"""
        self.run_api_test(
            1, "教师获取任教班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam-classes', '|', 'jq'],
            "1_get_exam_classes.json",
            self.test_setup
        )
    
    def test_02_get_scores(self):
        """测试用例2: 教师获取学生成绩列表"""
        self.run_api_test(
            2, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores', '|', 'jq'],
            "2_get_scores.json",
            self.test_setup
        )
    
    def test_03_create_score(self):
        """测试用例3: 教师创建学生成绩"""
        self.run_api_test(
            3, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0601", "subject_id": 1, "exam_type_id": 2, "score": 85}',
             '|', 'jq'],
            "3_create_score.json",
            self.test_setup
        )
    
    def test_04_update_score_success(self):
        """测试用例4: 教师更新学生成绩 - 正常情况"""
        self.run_api_test(
            4, "教师更新学生成绩 - 正常情况",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 92}',
             '|', 'jq'],
            "4_update_score_success.json",
            self.test_setup
        )
    
    def test_05_update_score_not_found(self):
        """测试用例5: 教师更新学生成绩 - 更新不存在的成绩"""
        self.run_api_test(
            5, "教师更新学生成绩 - 更新不存在的成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/999',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 85}',
             '|', 'jq'],
            "5_update_score_not_found.json",
            self.test_setup
        )
    
    def test_06_update_score_invalid_range(self):
        """测试用例6: 教师更新学生成绩 - 分数超出范围"""
        self.run_api_test(
            6, "教师更新学生成绩 - 分数超出范围",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 150}',
             '|', 'jq'],
            "6_update_score_invalid_range.json",
            self.test_setup
        )
    
    def test_07_delete_score(self):
        """测试用例7: 教师删除学生成绩"""
        self.run_api_test(
            7, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/scores/1', '|', 'jq'],
            "7_delete_score.json",
            self.test_setup
        )
    
    def test_08_get_classes(self):
        """测试用例8: 获取班级列表"""
        self.run_api_test(
            8, "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes', '|', 'jq'],
            "teacher_8_get_classes.json",
            self.test_setup
        )
    
    def test_09_get_class_by_id(self):
        """测试用例9: 根据ID获取班级"""
        self.run_api_test(
            9, "根据ID获取班级",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/1', '|', 'jq'],
            "teacher_9_get_class_by_id.json",
            self.test_setup
        )
    
    def test_10_get_class_not_found(self):
        """测试用例10: 获取不存在的班级"""
        self.run_api_test(
            10, "获取不存在的班级",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/999', '|', 'jq'],
            "teacher_10_get_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_11_get_students(self):
        """测试用例11: 教师获取学生列表"""
        self.run_api_test(
            11, "教师获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/students', '|', 'jq'],
            "teacher_11_get_students.json",
            self.test_setup
        )
    
    def test_12_get_student_by_id(self):
        """测试用例12: 教师根据ID获取学生"""
        self.run_api_test(
            12, "教师根据ID获取学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/S0601', '|', 'jq'],
            "teacher_12_get_student_by_id.json",
            self.test_setup
        )
    
    def test_13_get_student_not_found(self):
        """测试用例13: 教师获取不存在的学生"""
        self.run_api_test(
            13, "教师获取不存在的学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/NOTEXIST', '|', 'jq'],
            "teacher_13_get_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_14_create_student(self):
        """测试用例14: 教师创建学生"""
        self.run_api_test(
            14, "教师创建学生",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/students',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "TEST001", "student_name": "测试学生", "class_name": "高一1班"}',
             '|', 'jq'],
            "teacher_14_create_student.json",
            self.test_setup
        )
    
    def test_15_create_student_duplicate(self):
        """测试用例15: 教师创建重复学生"""
        self.run_api_test(
            15, "教师创建重复学生",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/students',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0601", "student_name": "重复学生", "class_name": "高一1班"}',
             '|', 'jq'],
            "teacher_15_create_student_duplicate.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_16_create_student_invalid_data(self):
        """测试用例16: 教师创建学生 - 无效数据"""
        self.run_api_test(
            16, "教师创建学生 - 无效数据",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/students',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "无效数据学生"}',
             '|', 'jq'],
            "teacher_16_create_student_invalid_data.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_17_delete_student(self):
        """测试用例17: 教师删除学生"""
        self.run_api_test(
            17, "教师删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/students/TEST001', '|', 'jq'],
            "teacher_17_delete_student.json",
            self.test_setup
        )
    
    def test_18_update_student(self):
        """测试用例18: 教师更新学生信息"""
        self.run_api_test(
            18, "教师更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/students/S0601',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "Updated Name"}',
             '|', 'jq'],
            "teacher_18_update_student.json",
            self.test_setup
        )
    
    def test_19_get_teachers(self):
        """测试用例19: 教师获取教师列表"""
        self.run_api_test(
            19, "教师获取教师列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/teachers', '|', 'jq'],
            "teacher_19_get_teachers.json",
            self.test_setup
        )
    
    def test_20_get_teacher(self):
        """测试用例20: 教师获取特定教师信息"""
        self.run_api_test(
            20, "教师获取特定教师信息",
            ['curl', '-s', f'{self.base_url}/api/teacher/teachers/1', '|', 'jq'],
            "teacher_20_get_teacher.json",
            self.test_setup
        )
    
    def test_21_get_class_students(self):
        """测试用例21: 教师获取班级学生列表"""
        self.run_api_test(
            21, "教师获取班级学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/1/students', '|', 'jq'],
            "teacher_21_get_class_students.json",
            self.test_setup
        )
    
    def test_22_get_exams(self):
        """测试用例22: 教师获取考试列表"""
        self.run_api_test(
            22, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '|', 'jq'],
            "teacher_22_get_exams.json",
            self.test_setup
        )
    
    def test_23_get_exam_by_id(self):
        """测试用例23: 教师获取特定考试信息"""
        self.run_api_test(
            23, "教师获取特定考试信息",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '|', 'jq'],
            "teacher_23_get_exam_by_id.json",
            self.test_setup
        )
    
    def test_24_create_exam(self):
        """测试用例24: 教师创建考试"""
        self.run_api_test(
            24, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"name": "测试考试", "subject_id": 1, "class_ids": [1], "exam_type_id": 1, "date": "2025-10-01", "total_score": 100}',
             '|', 'jq'],
            "teacher_24_create_exam.json",
            self.test_setup
        )
    
    def test_25_update_exam(self):
        """测试用例25: 教师更新考试信息"""
        self.run_api_test(
            25, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"name": "更新的考试"}',
             '|', 'jq'],
            "teacher_25_update_exam.json",
            self.test_setup
        )
    
    def test_26_delete_exam(self):
        """测试用例26: 教师删除考试"""
        self.run_api_test(
            26, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/1', '|', 'jq'],
            "teacher_26_delete_exam.json",
            self.test_setup
        )
    
    def test_27_get_exam_scores(self):
        """测试用例27: 教师获取考试成绩列表"""
        self.run_api_test(
            27, "教师获取考试成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1/scores', '|', 'jq'],
            "teacher_27_get_exam_scores.json",
            self.test_setup
        )