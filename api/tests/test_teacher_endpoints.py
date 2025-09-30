#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

from tests.test_curl.test_curl_base import CurlTestBase
from config.config import TestingConfig


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.cookie_file = "/tmp/test_cookie.txt"
        cls.test_results_dir = TestingConfig.CURL_TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "teacher_curl_commands.log")
        
        # 清理之前的cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)
        
        # 登录教师账户
        login_data = {
            "user_id": "4",
            "password": "123456"
        }
        import json
        import subprocess
        curl_cmd = [
            "curl", "-s", "-X", "POST", f"{cls.base_url}/api/auth/login",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(login_data),
            "-c", cls.cookie_file
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"教师登录失败: {result.stderr}"
        
        response_data = json.loads(result.stdout)
        assert response_data.get("success"), f"教师登录失败: {response_data.get('message', 'Unknown error')}"

        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'cookie_file': cls.cookie_file,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
        }
    
    @classmethod
    def teardown_class(cls):
        """测试类级别的清理"""
        # 登出
        import subprocess
        curl_cmd = [
            "curl", "-s", "-X", "POST", f"{cls.base_url}/api/auth/logout",
            "-b", cls.cookie_file
        ]
        
        subprocess.run(curl_cmd, capture_output=True, text=True)
        
        # 清理cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)

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
             '-d', '{"student_id": "S0601", "subject_id": 1, "exam_type_id": 2, "score": 85}',
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
    
    def test_08_get_classes(self):
        """测试用例8: 获取班级列表"""
        self.run_api_test(
            8, "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes', '-b', self.cookie_file],
            "teacher_8_get_classes.json", self.test_setup
        )
    
    def test_09_get_class_students(self):
        """测试用例9: 获取班级学生列表"""
        self.run_api_test(
            9, "获取班级学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/1/students', '-b', self.cookie_file],
            "teacher_9_get_class_students.json", self.test_setup
        )
    
    def test_10_get_exams(self):
        """测试用例10: 教师获取考试列表"""
        self.run_api_test(
            10, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '-b', self.cookie_file],
            "teacher_10_get_exams.json",
            self.test_setup
        )
    
    def test_10_create_exam(self):
        """测试用例10: 教师创建考试"""
        self.run_api_test(
            10, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"name": "Midterm Exam", "subject_id": 1, "class_ids": [6], "exam_type_id": 2, "date": "2025-10-15", "total_score": 100}',
             '-b', self.cookie_file],
            "teacher_10_create_exam.json",
            self.test_setup
        )
    
    def test_11_get_exam(self):
        """测试用例11: 教师获取特定考试"""
        self.run_api_test(
            11, "教师获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "teacher_11_get_exam.json",
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
            "teacher_12_update_exam.json",
            self.test_setup
        )
    
    def test_13_delete_exam(self):
        """测试用例13: 教师删除考试"""
        self.run_api_test(
            13, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "teacher_13_delete_exam.json",
            self.test_setup
        )
    
    def test_14_get_exam_results(self):
        """测试用例14: 教师获取考试结果"""
        self.run_api_test(
            14, "教师获取考试结果",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam-results', '-b', self.cookie_file],
            "teacher_14_get_exam_results.json",
            self.test_setup
        )
    
    def test_15_get_performance_stats(self):
        """测试用例15: 教师获取教学表现统计"""
        self.run_api_test(
            15, "教师获取教学表现统计",
            ['curl', '-s', f'{self.base_url}/api/teacher/performance', '-b', self.cookie_file],
            "teacher_15_get_performance_stats.json",
            self.test_setup
        )
    
    def test_16_get_students(self):
        """测试用例16: 教师获取学生列表"""
        self.run_api_test(
            16, "教师获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/students', '-b', self.cookie_file],
            "teacher_16_get_students.json",
            self.test_setup
        )
    
    def test_17_get_student(self):
        """测试用例17: 教师获取特定学生"""
        self.run_api_test(
            17, "教师获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/S0601', '-b', self.cookie_file],
            "teacher_17_get_student.json",
            self.test_setup
        )
    
    def test_18_update_student(self):
        """测试用例18: 教师更新学生信息"""
        self.run_api_test(
            18, "教师更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/students/S0601',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "Updated Name"}',
             '-b', self.cookie_file],
            "teacher_18_update_student.json",
            self.test_setup
        )
    
    def test_19_get_teachers(self):
        """测试用例19: 教师获取教师列表"""
        self.run_api_test(
            19, "教师获取教师列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/teachers', '-b', self.cookie_file],
            "teacher_19_get_teachers.json",
            self.test_setup
        )
    
    def test_20_get_teacher(self):
        """测试用例20: 教师获取特定教师信息"""
        self.run_api_test(
            20, "教师获取特定教师信息",
            ['curl', '-s', f'{self.base_url}/api/teacher/teachers/1', '-b', self.cookie_file],
            "teacher_20_get_teacher.json",
            self.test_setup
        )