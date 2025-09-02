#!/usr/bin/env python3
"""
管理员端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestAdminEndpoints(CurlTestBase):
    """管理员端点测试类"""
    
    def setup_class(self, test_environment):
        """在类级别设置测试环境并登录"""
        # 调用父类初始化方法设置测试环境
        super().__init__(test_environment)
        
        # 设置curl命令记录文件
        self.set_curl_commands_file(self.curl_commands_file)
        
        # 管理员登录
        assert self.login_admin(self.base_url, self.cookie_file), "管理员登录失败"
    
    def teardown_class(self):
        """在类级别登出"""
        assert self.logout(self.base_url, self.cookie_file), "管理员登出失败"
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        # 设置测试环境
        self.test_setup = {
            'api_base_url': self.base_url,
            'result_dir': self.test_results_dir,
            'cookie_file': self.cookie_file
        }
    
    def test_01_get_students(self):
        """测试用例1: 获取学生列表"""
        self.run_api_test(
            1, "获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/admin/students', '-b', self.cookie_file],
            "1_get_students.json", self.test_setup
        )
    
    def test_02_create_student(self):
        """测试用例2: 创建学生"""
        self.run_api_test(
            2, "创建学生",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/students',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S9999", "student_name": "Test Student", "class_id": 1, "password": "password123"}',
             '-b', self.cookie_file],
            "2_create_student.json", self.test_setup
        )
    
    def test_03_get_specific_student(self):
        """测试用例3: 获取特定学生"""
        self.run_api_test(
            3, "获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S0101', '-b', self.cookie_file],
            "3_get_student.json", self.test_setup
        )
    
    def test_04_update_student(self):
        """测试用例4: 更新学生信息"""
        self.run_api_test(
            4, "更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/students/S0101',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "Updated Student Name", "class_id": 1, "password": "password123"}',
             '-b', self.cookie_file],
            "4_update_student.json", self.test_setup
        )
    
    def test_05_delete_student(self):
        """测试用例5: 删除学生"""
        self.run_api_test(
            5, "删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S9999', '-b', self.cookie_file],
            "5_delete_student.json", self.test_setup
        )
    
    def test_06_get_teachers(self):
        """测试用例6: 获取教师列表"""
        self.run_api_test(
            6, "获取教师列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers', '-b', self.cookie_file],
            "6_get_teachers.json", self.test_setup
        )
    
    def test_07_create_teacher(self):
        """测试用例7: 创建教师"""
        self.run_api_test(
            7, "创建教师",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teachers',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "Test Teacher", "teacher_id": 999, "subject_id": 1, "password": "password123"}',
             '-b', self.cookie_file],
            "7_create_teacher.json", self.test_setup
        )
    
    def test_08_get_specific_teacher(self):
        """测试用例8: 获取特定教师"""
        self.run_api_test(
            8, "获取特定教师",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/1', '-b', self.cookie_file],
            "8_get_teacher.json", self.test_setup
        )
    
    def test_09_update_teacher(self):
        """测试用例9: 更新教师信息"""
        self.run_api_test(
            9, "更新教师信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teachers/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "Updated Teacher Name"}',
             '-b', self.cookie_file],
            "9_update_teacher.json", self.test_setup
        )
    
    def test_10_delete_teacher(self):
        """测试用例10: 删除教师"""
        self.run_api_test(
            10, "删除教师",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teachers/999', '-b', self.cookie_file],
            "10_delete_teacher.json", self.test_setup
        )
    
    def test_11_get_classes(self):
        """测试用例11: 获取班级列表"""
        self.run_api_test(
            11, "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/admin/classes', '-b', self.cookie_file],
            "11_get_classes.json", self.test_setup
        )
    
    def test_12_create_class(self):
        """测试用例12: 创建班级"""
        self.run_api_test(
            12, "创建班级",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/classes',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "Test Class", "grade": 1}',
             '-b', self.cookie_file],
            "12_create_class.json", self.test_setup
        )
    
    def test_13_get_specific_class(self):
        """测试用例13: 获取特定班级"""
        self.run_api_test(
            13, "获取特定班级",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/1', '-b', self.cookie_file],
            "13_get_class.json", self.test_setup
        )
    
    def test_14_update_class(self):
        """测试用例14: 更新班级信息"""
        self.run_api_test(
            14, "更新班级信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/classes/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "Updated Class Name"}',
             '-b', self.cookie_file],
            "14_update_class.json", self.test_setup
        )
    
    def test_15_delete_class(self):
        """测试用例15: 删除班级"""
        self.run_api_test(
            15, "删除班级",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/classes/10', '-b', self.cookie_file],
            "15_delete_class.json", self.test_setup
        )
    
    def test_16_get_subjects(self):
        """测试用例16: 获取科目列表"""
        self.run_api_test(
            16, "获取科目列表",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects', '-b', self.cookie_file],
            "16_get_subjects.json", self.test_setup
        )
    
    def test_17_create_subject(self):
        """测试用例17: 创建科目"""
        self.run_api_test(
            17, "创建科目",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/subjects',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "Test Subject"}',
             '-b', self.cookie_file],
            "17_create_subject.json", self.test_setup
        )
    
    def test_18_get_specific_subject(self):
        """测试用例18: 获取特定科目"""
        self.run_api_test(
            18, "获取特定科目",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/1', '-b', self.cookie_file],
            "18_get_subject.json", self.test_setup
        )
    
    def test_19_update_subject(self):
        """测试用例19: 更新科目信息"""
        self.run_api_test(
            19, "更新科目信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/subjects/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "Updated Subject Name"}',
             '-b', self.cookie_file],
            "19_update_subject.json", self.test_setup
        )
    
    def test_20_delete_subject(self):
        """测试用例20: 删除科目"""
        self.run_api_test(
            20, "删除科目",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/subjects/10', '-b', self.cookie_file],
            "20_delete_subject.json", self.test_setup
        )
    
    def test_21_get_exam_types(self):
        """测试用例21: 获取考试类型列表"""
        self.run_api_test(
            21, "获取考试类型列表",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types', '-b', self.cookie_file],
            "21_get_exam_types.json", self.test_setup
        )
    
    def test_22_create_exam_type(self):
        """测试用例22: 创建考试类型"""
        self.run_api_test(
            22, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exam-types',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Test Exam Type"}',
             '-b', self.cookie_file],
            "22_create_exam_type.json", self.test_setup
        )
    
    def test_23_get_specific_exam_type(self):
        """测试用例23: 获取特定考试类型"""
        self.run_api_test(
            23, "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types/1', '-b', self.cookie_file],
            "23_get_exam_type.json", self.test_setup
        )
    
    def test_24_update_exam_type(self):
        """测试用例24: 更新考试类型信息"""
        self.run_api_test(
            24, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam-types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Updated Exam Type Name"}',
             '-b', self.cookie_file],
            "24_update_exam_type.json", self.test_setup
        )
    
    def test_25_delete_exam_type(self):
        """测试用例25: 删除考试类型"""
        self.run_api_test(
            25, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam-types/10', '-b', self.cookie_file],
            "25_delete_exam_type.json", self.test_setup
        )
    
    def test_26_get_exams(self):
        """测试用例26: 获取考试列表"""
        self.run_api_test(
            26, "获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/admin/exams', '-b', self.cookie_file],
            "26_get_exams.json", self.test_setup
        )
    
    def test_27_create_exam(self):
        """测试用例27: 创建考试"""
        self.run_api_test(
            27, "创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Test Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-09-01"}',
             '-b', self.cookie_file],
            "27_create_exam.json", self.test_setup
        )
    
    def test_28_get_specific_exam(self):
        """测试用例28: 获取特定考试"""
        self.run_api_test(
            28, "获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/admin/exams/1', '-b', self.cookie_file],
            "28_get_exam.json", self.test_setup
        )
    
    def test_29_update_exam(self):
        """测试用例29: 更新考试信息"""
        self.run_api_test(
            29, "更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Exam Name"}',
             '-b', self.cookie_file],
            "29_update_exam.json", self.test_setup
        )
    
    def test_30_delete_exam(self):
        """测试用例30: 删除考试"""
        self.run_api_test(
            30, "删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exams/10', '-b', self.cookie_file],
            "30_delete_exam.json", self.test_setup
        )
    
    def test_31_get_scores(self):
        """测试用例31: 获取成绩列表"""
        self.run_api_test(
            31, "获取成绩列表",
            ['curl', '-s', f'{self.base_url}/api/admin/scores', '-b', self.cookie_file],
            "31_get_scores.json", self.test_setup
        )
    
    def test_32_create_score(self):
        """测试用例32: 创建成绩"""
        self.run_api_test(
            32, "创建成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', self.cookie_file],
            "32_create_score.json", self.test_setup
        )
    
    def test_33_get_specific_score(self):
        """测试用例33: 获取特定成绩"""
        self.run_api_test(
            33, "获取特定成绩",
            ['curl', '-s', f'{self.base_url}/api/admin/scores/1', '-b', self.cookie_file],
            "33_get_score.json", self.test_setup
        )
    
    def test_34_update_score(self):
        """测试用例34: 更新成绩信息"""
        self.run_api_test(
            34, "更新成绩信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 90}',
             '-b', self.cookie_file],
            "34_update_score.json", self.test_setup
        )
    
    def test_35_delete_score(self):
        """测试用例35: 删除成绩"""
        self.run_api_test(
            35, "删除成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/scores/10', '-b', self.cookie_file],
            "35_delete_score.json", self.test_setup
        )
    
    def test_36_get_class_subjects(self):
        """测试用例36: 获取班级科目列表"""
        self.run_api_test(
            36, "获取班级科目列表",
            ['curl', '-s', f'{self.base_url}/api/admin/class-subjects', '-b', self.cookie_file],
            "36_get_class_subjects.json", self.test_setup
        )
    
    def test_37_create_class_subject(self):
        """测试用例37: 创建班级科目关联"""
        self.run_api_test(
            37, "创建班级科目关联",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/class-subjects',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_id": 1, "subject_id": 1}',
             '-b', self.cookie_file],
            "37_create_class_subject.json", self.test_setup
        )
    
    def test_38_get_specific_class_subject(self):
        """测试用例38: 获取特定班级科目关联"""
        self.run_api_test(
            38, "获取特定班级科目关联",
            ['curl', '-s', f'{self.base_url}/api/admin/class-subjects/1', '-b', self.cookie_file],
            "38_get_class_subject.json", self.test_setup
        )
    
    def test_39_delete_class_subject(self):
        """测试用例39: 删除班级科目关联"""
        self.run_api_test(
            39, "删除班级科目关联",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/class-subjects/10', '-b', self.cookie_file],
            "39_delete_class_subject.json", self.test_setup
        )