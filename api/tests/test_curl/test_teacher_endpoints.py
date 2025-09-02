#!/usr/bin/env python3
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类"""
    
    def setup_class(self, test_environment=None):
        """在类级别设置测试环境并登录"""
        # 如果没有通过参数传递，则使用默认配置
        if test_environment:
            self.base_url = test_environment['base_url']
            self.test_results_dir = test_environment['test_results_dir']
            self.curl_commands_file = test_environment['curl_commands_file']
            self.cookie_file = test_environment['cookie_file']
        else:
            from config.config import TestingConfig
            config = TestingConfig()
            self.base_url = f'http://localhost:{config.PORT}'
            self.test_results_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
            self.curl_commands_file = os.path.join(self.test_results_dir, 'curl_commands.txt')
            self.cookie_file = '/tmp/test_cookie.txt'
            
            os.makedirs(self.test_results_dir, exist_ok=True)
        
        # 设置curl命令记录文件
        self.set_curl_commands_file(self.curl_commands_file)
        
        # 教师登录
        assert self.login_teacher(self.base_url, self.cookie_file), "教师登录失败"
    
    def teardown_class(self):
        """在类级别登出"""
        assert self.logout(self.base_url, self.cookie_file), "教师登出失败"
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        # 设置测试环境
        self.test_setup = {
            'api_base_url': self.base_url,
            'result_dir': self.test_results_dir,
            'cookie_file': self.cookie_file
        }
    
    def test_01_get_exam_types(self):
        """测试用例1: 获取考试类型列表(教师)"""
        self.run_api_test(
            1, "获取考试类型列表(教师)",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types', '-b', self.cookie_file],
            "1_get_exam_types.json", self.test_setup
        )
    
    def test_02_create_exam_type(self):
        """测试用例2: 创建考试类型"""
        self.run_api_test(
            2, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exam-types',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Test Exam Type"}',
             '-b', self.cookie_file],
            "2_create_exam_type.json", self.test_setup
        )
    
    def test_03_get_specific_exam_type(self):
        """测试用例3: 获取特定考试类型"""
        self.run_api_test(
            3, "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types/1', '-b', self.cookie_file],
            "3_get_exam_type.json", self.test_setup
        )
    
    def test_04_update_exam_type(self):
        """测试用例4: 更新考试类型信息"""
        self.run_api_test(
            4, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam-types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Updated Exam Type Name"}',
             '-b', self.cookie_file],
            "4_update_exam_type.json", self.test_setup
        )
    
    def test_05_delete_exam_type(self):
        """测试用例5: 删除考试类型"""
        self.run_api_test(
            5, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam-types/10', '-b', self.cookie_file],
            "5_delete_exam_type.json", self.test_setup
        )
    
    def test_06_get_teacher_classes(self):
        """测试用例6: 教师获取任教班级列表"""
        self.run_api_test(
            6, "教师获取任教班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam/classes', '-b', self.cookie_file],
            "6_get_teacher_classes.json", self.test_setup
        )
    
    def test_07_get_scores(self):
        """测试用例7: 教师获取学生成绩列表"""
        self.run_api_test(
            7, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores', '-b', self.cookie_file],
            "7_get_teacher_scores.json", self.test_setup
        )
    
    def test_08_create_score(self):
        """测试用例8: 教师创建学生成绩"""
        self.run_api_test(
            8, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', self.cookie_file],
            "8_create_score.json", self.test_setup
        )
    
    def test_09_update_score(self):
        """测试用例9: 教师更新学生成绩"""
        self.run_api_test(
            9, "教师更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 90}',
             '-b', self.cookie_file],
            "9_update_score.json", self.test_setup
        )
    
    def test_10_delete_score(self):
        """测试用例10: 教师删除学生成绩"""
        self.run_api_test(
            10, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/scores/10', '-b', self.cookie_file],
            "10_delete_score.json", self.test_setup
        )
    
    def test_11_get_exams(self):
        """测试用例11: 教师获取考试列表"""
        self.run_api_test(
            11, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '-b', self.cookie_file],
            "11_get_exams.json", self.test_setup
        )
    
    def test_12_create_exam(self):
        """测试用例12: 教师创建考试"""
        self.run_api_test(
            12, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Test Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-09-01"}',
             '-b', self.cookie_file],
            "12_create_exam.json", self.test_setup
        )
    
    def test_13_get_specific_exam(self):
        """测试用例13: 教师获取特定考试"""
        self.run_api_test(
            13, "教师获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "13_get_exam.json", self.test_setup
        )
    
    def test_14_update_exam(self):
        """测试用例14: 教师更新考试信息"""
        self.run_api_test(
            14, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Exam Name"}',
             '-b', self.cookie_file],
            "14_update_exam.json", self.test_setup
        )
    
    def test_15_delete_exam(self):
        """测试用例15: 教师删除考试"""
        self.run_api_test(
            15, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/10', '-b', self.cookie_file],
            "15_delete_exam.json", self.test_setup
        )