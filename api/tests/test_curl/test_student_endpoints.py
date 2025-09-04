#!/usr/bin/env python3
"""
学生端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase
from config.config import TestingConfig


class TestStudentEndpoints(CurlTestBase):
    """学生端点测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 创建实例以访问方法
        instance = cls()
        
        cls.base_url = f"http://127.0.0.1:{TestingConfig.PORT}"
        cls.cookie_file = "/tmp/test_cookie.txt"
        cls.test_results_dir = TestingConfig.CURL_TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "student_curl_commands.log")
        
        # 确保测试结果目录存在
        os.makedirs(cls.test_results_dir, exist_ok=True)
        
        # 清理之前的cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)
            
        # 登录学生账户
        instance.set_curl_commands_file(cls.curl_commands_file)  # 设置命令记录文件
        assert instance.login_student(cls.base_url, cls.cookie_file), "学生登录失败"
        
        # 保存环境变量供测试方法使用
        cls.test_setup = {
            'result_dir': cls.test_results_dir,
            'base_url': cls.base_url,
            'cookie_file': cls.cookie_file,
            'curl_commands_file': cls.curl_commands_file
        }
    
    @classmethod
    def teardown_class(cls):
        """测试类级别的清理"""
        # 创建实例以访问方法
        instance = cls()
        
        # 测试结束后登出
        if cls.base_url and cls.cookie_file:
            instance.logout(cls.base_url, cls.cookie_file)
            
        # 删除cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)

    def test_01_get_profile(self):
        """测试用例1: 学生获取个人信息"""
        self.run_api_test(
            1, "学生获取个人信息",
            ['curl', '-s', f'{self.base_url}/api/student/profile', '-b', self.cookie_file],
            "1_get_student_profile.json", self.test_setup
        )
    
    def test_02_get_scores(self):
        """测试用例2: 学生获取个人成绩"""
        self.run_api_test(
            2, "学生获取个人成绩",
            ['curl', '-s', f'{self.base_url}/api/student/scores', '-b', self.cookie_file],
            "2_get_student_scores.json", self.test_setup
        )
    
    def test_03_get_exam_results(self):
        """测试用例3: 学生获取考试结果"""
        self.run_api_test(
            3, "学生获取考试结果",
            ['curl', '-s', f'{self.base_url}/api/student/exam/results', '-b', self.cookie_file],
            "3_get_student_exam_results.json", self.test_setup
        )