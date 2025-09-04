#!/usr/bin/env python3
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import json
import subprocess
import pytest
from tests.test_curl.test_curl_base import CurlTestBase
from config.config import TestingConfig


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类"""
    
    def setup_class(self):
        """测试类级别的设置"""
        self.base_url = f"http://127.0.0.1:{TestingConfig.PORT}"
        self.cookie_file = "/tmp/test_cookie.txt"
        self.test_results_dir = TestingConfig.CURL_TEST_DIR
        self.curl_commands_file = os.path.join(self.test_results_dir, "teacher_curl_commands.log")
        
        # 确保测试结果目录存在
        os.makedirs(self.test_results_dir, exist_ok=True)
        
        # 清理之前的cookie文件
        if os.path.exists(self.cookie_file):
            os.remove(self.cookie_file)
            
        # 登录教师账户
        curl_test_base = CurlTestBase()
        curl_test_base.curl_commands_file = self.curl_commands_file  # 直接设置属性
        assert curl_test_base.login_teacher(self.base_url, self.cookie_file), "教师登录失败"
        
        # 保存环境变量供测试方法使用
        self.test_setup = {
            'result_dir': self.test_results_dir,
            'base_url': self.base_url,
            'cookie_file': self.cookie_file,
            'curl_commands_file': self.curl_commands_file
        }
    
    def teardown_class(self):
        """测试类级别的清理"""
        # 测试结束后登出
        if self.base_url and self.cookie_file:
            curl_test_base = CurlTestBase()
            curl_test_base.curl_commands_file = self.curl_commands_file  # 直接设置属性
            curl_test_base.logout(self.base_url, self.cookie_file)
            
        # 删除cookie文件
        if os.path.exists(self.cookie_file):
            os.remove(self.cookie_file)

    def test_01_get_exam_classes(self):
        """测试用例1: 教师获取任教班级列表"""
        self.run_api_test(
            1, "教师获取任教班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam-classes', '-b', self.cookie_file],
            "1_get_exam_classes.json",
            self.test_setup
        )
    
    def test_02_get_scores(self):
        """测试用例2: 教师获取学生成绩列表"""
        self.run_api_test(
            2, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores', '-b', self.cookie_file],
            "2_get_scores.json",
            self.test_setup
        )
    
    def test_03_create_score(self):
        """测试用例3: 教师创建学生成绩"""
        self.run_api_test(
            3, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', self.cookie_file],
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
             '-b', self.cookie_file],
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
             '-b', self.cookie_file],
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
             '-b', self.cookie_file],
            "6_update_score_invalid_range.json",
            self.test_setup
        )
    
    def test_07_delete_score(self):
        """测试用例8: 教师删除学生成绩"""
        self.run_api_test(
            8, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/scores/1', '-b', self.cookie_file],
            "8_delete_score.json",
            self.test_setup
        )
    
    def test_09_get_exams(self):
        """测试用例9: 教师获取考试列表"""
        self.run_api_test(
            9, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '-b', self.cookie_file],
            "9_get_exams.json",
            self.test_setup
        )
    
    def test_10_create_exam(self):
        """测试用例10: 教师创建考试"""
        self.run_api_test(
            10, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"name": "Midterm Exam", "subject_id": 1, "class_ids": [1], "exam_type_id": 1, "date": "2025-10-15", "total_score": 100}',
             '-b', self.cookie_file],
            "10_create_exam.json",
            self.test_setup
        )
    
    def test_11_get_exam(self):
        """测试用例11: 教师获取特定考试"""
        self.run_api_test(
            11, "教师获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "11_get_exam.json",
            self.test_setup
        )
    
    def test_12_update_exam(self):
        """测试用例12: 教师更新考试信息"""
        self.run_api_test(
            12, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Midterm Exam", "exam_date": "2025-10-20"}',
             '-b', self.cookie_file],
            "12_update_exam.json",
            self.test_setup
        )
    
    def test_13_delete_exam(self):
        """测试用例13: 教师删除考试"""
        self.run_api_test(
            13, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "13_delete_exam.json",
            self.test_setup
        )
    
    def test_14_get_exam_results(self):
        """测试用例14: 教师获取考试结果"""
        self.run_api_test(
            14, "教师获取考试结果",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam-results', '-b', self.cookie_file],
            "14_get_exam_results.json",
            self.test_setup
        )
    
    def test_15_get_performance_stats(self):
        """测试用例15: 教师获取教学表现统计"""
        self.run_api_test(
            15, "教师获取教学表现统计",
            ['curl', '-s', f'{self.base_url}/api/teacher/performance', '-b', self.cookie_file],
            "15_get_performance_stats.json",
            self.test_setup
        )
    
    def test_16_get_students(self):
        """测试用例16: 教师获取学生列表"""
        self.run_api_test(
            16, "教师获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/students', '-b', self.cookie_file],
            "16_get_students.json",
            self.test_setup
        )
    
    def test_17_get_student(self):
        """测试用例17: 教师获取特定学生"""
        self.run_api_test(
            17, "教师获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/S0201', '-b', self.cookie_file],
            "17_get_student.json",
            self.test_setup
        )
    
    def test_18_update_student(self):
        """测试用例18: 教师更新学生信息"""
        self.run_api_test(
            18, "教师更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/students/S0201',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "Updated Name"}',
             '-b', self.cookie_file],
            "18_update_student.json",
            self.test_setup
        )
