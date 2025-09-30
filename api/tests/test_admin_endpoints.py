#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

# 将api目录添加到Python路径中
api_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

import os
from tests.test_curl.test_curl_base import CurlTestBase
from config.config import TestingConfig


class TestAdminEndpoints(CurlTestBase):
    """管理员端点测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.cookie_file = "/tmp/test_cookie.txt"
        cls.test_results_dir = TestingConfig.CURL_TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "admin_curl_commands.log")
        
        # 清理之前的cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)
        
        # 登录管理员账户
        # 创建一个实例来调用实例方法
        instance = cls()
        assert instance.login_admin(cls.base_url, cls.cookie_file), "管理员登录失败"

        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'cookie_file': cls.cookie_file,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
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
             '-d', '{"student_id": "S9999", "student_name": "张三", "class_id": 1, "password": "pass123"}',
             '-b', self.cookie_file],
            "2_create_student.json", self.test_setup
        )
    
    def test_03_get_student(self):
        """测试用例3: 获取特定学生"""
        self.run_api_test(
            3, "获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S0201', '-b', self.cookie_file],
            "3_get_student.json", self.test_setup
        )
    
    def test_04_update_student(self):
        """测试用例4: 更新学生信息"""
        self.run_api_test(
            4, "更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/students/S0201',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "更新的学生姓名"}',
             '-b', self.cookie_file],
            "4_update_student.json", self.test_setup
        )
    
    def test_05_delete_student(self):
        """测试用例5: 删除学生"""
        self.run_api_test(
            5, "删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S0201', '-b', self.cookie_file],
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
             '-d', '{"teacher_name": "李老师", "subject_id": 1, "password": "pass123"}',
             '-b', self.cookie_file],
            "7_create_teacher.json", self.test_setup
        )
    
    def test_08_get_teacher(self):
        """测试用例8: 获取特定教师"""
        self.run_api_test(
            8, "获取特定教师",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/3', '-b', self.cookie_file],
            "8_get_teacher.json", self.test_setup
        )
    
    def test_09_update_teacher(self):
        """测试用例9: 更新教师信息"""
        self.run_api_test(
            9, "更新教师信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teachers/3',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "更新的张老师", "subject_id": 2}',
             '-b', self.cookie_file],
            "9_update_teacher.json", self.test_setup
        )
    
    def test_10_delete_teacher(self):
        """测试用例10: 删除教师"""
        self.run_api_test(
            10, "删除教师",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teachers/999', '-b', self.cookie_file],
            "10_delete_teacher.json", self.test_setup, expect_error=True
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
             '-d', '{"class_name": "高三X班", "grade_id": 3}',
             '-b', self.cookie_file],
            "12_create_class.json", self.test_setup
        )
    
    def test_13_get_class(self):
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
             '-d', '{"class_name": "更新的班级名称"}',
             '-b', self.cookie_file],
            "14_update_class.json", self.test_setup
        )
    
    def test_15_delete_class(self):
        """测试用例15: 删除班级"""
        self.run_api_test(
            15, "删除班级",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/classes/1', '-b', self.cookie_file],
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
             '-d', '{"subject_name": "新科目", "description": "科目描述"}',
             '-b', self.cookie_file],
            "17_create_subject.json", self.test_setup
        )
    
    def test_18_get_subject(self):
        """测试用例18: 获取特定科目"""
        # 先读取测试17创建的科目结果，获取科目ID
        import json
        result_file = os.path.join(self.test_results_dir, "17_create_subject.json")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                result = json.load(f)
                subject_id = result.get('data', {}).get('subject_id', 4)
        else:
            subject_id = 4  # 默认值
        
        self.run_api_test(
            18, "获取特定科目",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/{subject_id}', '-b', self.cookie_file],
            "18_get_subject.json", self.test_setup
        )
    
    def test_19_update_subject(self):
        """测试用例19: 更新科目信息"""
        # 先读取测试17创建的科目结果，获取科目ID
        import json
        result_file = os.path.join(self.test_results_dir, "17_create_subject.json")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                result = json.load(f)
                subject_id = result.get('data', {}).get('subject_id', 4)
        else:
            subject_id = 4  # 默认值
        
        self.run_api_test(
            19, "更新科目信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/subjects/{subject_id}',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "更新的科目名称"}',
             '-b', self.cookie_file],
            "19_update_subject.json", self.test_setup
        )
    
    def test_20_delete_subject(self):
        """测试用例20: 删除科目"""
        # 先读取测试17创建的科目结果，获取科目ID
        import json
        result_file = os.path.join(self.test_results_dir, "17_create_subject.json")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                result = json.load(f)
                subject_id = result.get('data', {}).get('subject_id', 4)
        else:
            subject_id = 4  # 默认值
        
        self.run_api_test(
            20, "删除科目",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/subjects/{subject_id}', '-b', self.cookie_file],
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
             '-d', '{"exam_type_name": "新考试类型1", "description": "考试类型描述"}',
             '-b', self.cookie_file],
            "22_create_exam_type.json", self.test_setup
        )
    
    def test_23_get_exam_type(self):
        """测试用例23: 获取特定考试类型"""
        self.run_api_test(
            23, "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types/2', '-b', self.cookie_file],
            "23_get_exam_type.json", self.test_setup
        )
    
    def test_24_update_exam_type(self):
        """测试用例24: 更新考试类型信息"""
        self.run_api_test(
            24, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam-types/2',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "更新的考试类型名称"}',
             '-b', self.cookie_file],
            "24_update_exam_type.json", self.test_setup
        )
    
    def test_25_delete_exam_type(self):
        """测试用例25: 删除考试类型"""
        self.run_api_test(
            25, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam-types/2', '-b', self.cookie_file],
            "25_delete_exam_type.json", self.test_setup
        )
    
    def test_26_get_teacher_classes(self):
        """测试用例26: 获取教师班级关系列表"""
        self.run_api_test(
            26, "获取教师班级关系列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher-classes', '-b', self.cookie_file],
            "26_get_teacher_classes.json", self.test_setup
        )
    
    def test_27_create_teacher_class(self):
        """测试用例27: 创建教师班级关系"""
        self.run_api_test(
            27, "创建教师班级关系",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teacher-classes',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 4, "class_id": 2}',
             '-b', self.cookie_file],
            "27_create_teacher_class.json", self.test_setup
        )
    
    def test_28_get_teacher_class(self):
        """测试用例28: 获取特定教师班级关系"""
        self.run_api_test(
            28, "获取特定教师班级关系",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher-classes/1', '-b', self.cookie_file],
            "28_get_teacher_class.json", self.test_setup
        )
    
    def test_29_update_teacher_class(self):
        """测试用例29: 更新教师班级关系"""
        self.run_api_test(
            29, "更新教师班级关系",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teacher-classes/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 4, "class_id": 2}',
             '-b', self.cookie_file],
            "29_update_teacher_class.json", self.test_setup
        )
    
    def test_30_delete_teacher_class(self):
        """测试用例30: 删除教师班级关系"""
        self.run_api_test(
            30, "删除教师班级关系",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teacher-classes/4?class_id=2', '-b', self.cookie_file],
            "30_delete_teacher_class.json", self.test_setup
        )

    @classmethod
    def teardown_class(cls):
        """测试类级别的清理"""
        # 登出
        # 创建一个实例来调用实例方法
        instance = cls()
        instance.logout(cls.base_url, cls.cookie_file)
        
        # 清理cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])