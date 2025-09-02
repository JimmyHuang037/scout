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
    
    @pytest.fixture(autouse=True)
    def setup_test(self, test_environment):
        """自动使用的fixture，用于设置测试环境"""
        # 设置测试环境配置
        self.setup_test_environment(test_environment)
        
        # 设置curl命令记录文件
        self.set_curl_commands_file(self.curl_commands_file)
        
        # 登录学生账户
        assert self.login_student(self.base_url, self.cookie_file), "学生登录失败"
        
        # 保存环境变量供测试方法使用
        self.test_setup = {
            'api_base_url': self.base_url,
            'result_dir': self.test_results_dir,
            'cookie_file': self.cookie_file
        }
        
        yield  # 测试执行完毕后继续执行下面的代码
        
        # 测试结束后登出
        self.logout(self.base_url, self.cookie_file)
    
    def teardown_method(self, request):
        """每个测试方法执行后的清理工作"""
        pass
    
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