#!/usr/bin/env python3
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import json
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类"""
    
    def setup_class(self):
        """测试类级别的设置"""
        self.base_url = "http://127.0.0.1:5010"
        self.cookie_file = "/tmp/test_cookie.txt"
        self.test_results_dir = "/home/jimmy/repo/scout/logs_testing/curl_test"
        self.curl_commands_file = os.path.join(self.test_results_dir, "teacher_curl_commands.log")
        
        # 确保测试结果目录存在
        os.makedirs(self.test_results_dir, exist_ok=True)
        
        # 清理之前的cookie文件
        if os.path.exists(self.cookie_file):
            os.remove(self.cookie_file)
            
        # 登录教师账户
        assert self.login_teacher(self.base_url, self.cookie_file), "教师登录失败"
    
    def teardown_class(self):
        """测试类级别的清理"""
        # 测试结束后登出
        if self.base_url and self.cookie_file:
            self.logout(self.base_url, self.cookie_file)
            
        # 删除cookie文件
        if os.path.exists(self.cookie_file):
            os.remove(self.cookie_file)
    
    def test_01_get_exam_classes(self):
        """测试用例1: 教师获取任教班级列表"""
        self.run_api_test(
            1, "教师获取任教班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam-classes', '-b', self.cookie_file],
            "1_get_teacher_classes.json"
        )
    
    def test_02_get_scores(self):
        """测试用例2: 教师获取学生成绩列表"""
        self.run_api_test(
            2, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores', '-b', self.cookie_file],
            "2_get_teacher_scores.json"
        )
    
    def test_03_create_score(self):
        """测试用例3: 教师创建学生成绩"""
        self.run_api_test(
            3, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', self.cookie_file],
            "3_create_score.json"
        )
    
    def test_04_update_score(self):
        """测试用例4: 教师更新学生成绩"""
        self.run_api_test(
            4, "教师更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 92}',
             '-b', self.cookie_file],
            "4_update_score.json"
        )
    
    def test_05_delete_score(self):
        """测试用例5: 教师删除学生成绩"""
        self.run_api_test(
            5, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/scores/1', '-b', self.cookie_file],
            "5_delete_score.json"
        )
    
    def test_06_get_exams(self):
        """测试用例6: 教师获取考试列表"""
        self.run_api_test(
            6, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '-b', self.cookie_file],
            "6_get_exams.json"
        )
    
    def test_07_create_exam(self):
        """测试用例7: 教师创建考试"""
        self.run_api_test(
            7, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Midterm Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-10-15", "class_id": 1}',
             '-b', self.cookie_file],
            "7_create_exam.json"
        )
    
    def test_08_get_exam(self):
        """测试用例8: 教师获取特定考试"""
        self.run_api_test(
            8, "教师获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "8_get_exam.json"
        )
    
    def test_09_update_exam(self):
        """测试用例9: 教师更新考试信息"""
        self.run_api_test(
            9, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Midterm Exam", "exam_date": "2025-10-20"}',
             '-b', self.cookie_file],
            "9_update_exam.json"
        )
    
    def test_10_delete_exam(self):
        """测试用例10: 教师删除考试"""
        self.run_api_test(
            10, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "10_delete_exam.json"
        )
    
    def test_11_get_exam_results(self):
        """测试用例11: 教师获取考试结果"""
        self.run_api_test(
            11, "教师获取考试结果",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam-results', '-b', self.cookie_file],
            "11_get_exam_results.json"
        )
    
    def test_12_get_performance_stats(self):
        """测试用例12: 教师获取教学表现统计"""
        self.run_api_test(
            12, "教师获取教学表现统计",
            ['curl', '-s', f'{self.base_url}/api/teacher/performance', '-b', self.cookie_file],
            "12_get_performance_stats.json"
        )
    
    def test_13_get_students(self):
        """测试用例13: 教师获取学生列表"""
        self.run_api_test(
            13, "教师获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/students', '-b', self.cookie_file],
            "13_get_students.json"
        )
    
    def test_14_get_student(self):
        """测试用例14: 教师获取特定学生"""
        self.run_api_test(
            14, "教师获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/S0201', '-b', self.cookie_file],
            "14_get_student.json"
        )
    
    def test_15_update_student(self):
        """测试用例15: 教师更新学生信息"""
        self.run_api_test(
            15, "教师更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/students/S0201',
             '-H', 'Content-Type: application/json',
             '-d', '{"phone": "13800138000", "address": "Updated Address"}',
             '-b', self.cookie_file],
            "15_update_student.json"
        )
