#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 将api目录添加到Python路径中
api_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from tests.test_curl.test_curl_base import CurlTestBase
from config.config import TestingConfig


class TestStudentEndpoints(CurlTestBase):
    """学生端点测试类"""

    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.cookie_file = "/tmp/test_cookie.txt"
        cls.test_results_dir = TestingConfig.CURL_TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "student_curl_commands.log")
        
        # 清理之前的cookie文件
        if os.path.exists(cls.cookie_file):
            os.remove(cls.cookie_file)
        
        # 登录学生账户
        login_data = {
            "user_id": "S0101",
            "password": "pass123"
        }
        import json
        import subprocess
        curl_cmd = [
            "curl", "-s", "-X", "POST", f"{cls.base_url}/api/auth/login",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(login_data),
            "-c", cls.cookie_file
        ]
        print("startlogin")
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        print("endlogin")
        print(result)
        assert result.returncode == 0, f"学生登录失败: {result.stderr}"
        
        response_data = json.loads(result.stdout)
        assert response_data.get("success"), f"学生登录失败: {response_data.get('message', 'Unknown error')}"

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

    def test_01_get_grades(self):
        """测试用例1: 获取成绩列表"""
        print("test123")
        self.run_api_test(
            1, "获取成绩列表",
            ['curl', '-s', f'{self.base_url}/api/student/scores', '-b', self.cookie_file],
            "student_1_get_grades.json", self.test_setup
        )