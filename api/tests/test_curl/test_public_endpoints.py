#!/usr/bin/env python3
"""
公共端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import subprocess
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestPublicEndpoints(CurlTestBase):
    """公共端点测试类"""
    
    def test_public_endpoints(self, start_api_server, test_results_dir, curl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_filecurl_commands_file):
        """测试公共端点"""
        # 设置测试环境
        test_setup, cookie_file = self.setup_test_environment(test_results_dir, curl_commands_file)
        
        # 测试用例38: 健康检查
        self.run_api_test(
            38, "健康检查",
            ['curl', '-s', f'{self.base_url}/api/auth/health'],
            "38_health_check.json", test_setup
        )
        
        # 测试用例39: 登录
        cmd = [
            'curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}'
        ]
        self.run_api_test(
            39, "登录",
            cmd,
            "39_login.json", test_setup
        )
        
        # 测试用例40: 登出
        # 首先需要登录以获取cookie
        login_cmd = [
            'curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}',
            '-c', test_setup['cookie_file']
        ]
        self._record_curl_command(40, "登录以获取cookie", login_cmd)
        subprocess.run(login_cmd, capture_output=True, text=True)
        
        # 然后执行登出
        logout_cmd = [
            'curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/logout',
            '-b', test_setup['cookie_file']
        ]
        self.run_api_test(
            40, "登出",
            logout_cmd,
            "40_logout.json", test_setup
        )
    """公共端点测试类"""
    
    def test_public_endpoints(self, start_api_server, test_results_dir, curl_commands_file):
        """测试公共端点"""
        # 设置curl命令记录文件
        self.set_curl_commands_file(curl_commands_file)
        
        # 设置测试环境
        test_setup, cookie_file = self.setup_test_environment(test_results_dir)
        
        # 测试用例38: 健康检查
        self.run_api_test(
            38, "健康检查",
            ['curl', '-s', f'{self.base_url}/api/auth/health'],
            "38_health_check.json", test_setup
        )
        
        # 测试用例39: 登录
        cmd = [
            'curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}'
        ]
        self.run_api_test(
            39, "登录",
            cmd,
            "39_login.json", test_setup
        )
        
        # 测试用例40: 登出
        # 首先需要登录以获取cookie
        login_cmd = [
            'curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}',
            '-c', test_setup['cookie_file']
        ]
        self._record_curl_command(40, "登录以获取cookie", login_cmd)
        subprocess.run(login_cmd, capture_output=True, text=True)
        
        # 然后执行登出
        logout_cmd = [
            'curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/logout',
            '-b', test_setup['cookie_file']
        ]
        self.run_api_test(
            40, "登出",
            logout_cmd,
            "40_logout.json", test_setup
        )