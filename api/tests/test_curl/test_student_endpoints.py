#!/usr/bin/env python3
"""
学生端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestStudentEndpoints(CurlTestBase):
    """学生端点测试类"""
    
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
        
        # 学生登录
        assert self.login_student(self.base_url, self.cookie_file), "学生登录失败"
    
    def teardown_class(self):
        """在类级别登出"""
        assert self.logout(self.base_url, self.cookie_file), "学生登出失败"
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        # 设置测试环境
        self.test_setup = {
            'api_base_url': self.base_url,
            'result_dir': self.test_results_dir,
            'cookie_file': self.cookie_file
        }
    
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