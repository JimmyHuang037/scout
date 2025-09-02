#!/usr/bin/env python3
"""
CURL测试基类
提供通用的测试方法和设置
"""

import os
import subprocess
import json
import pytest

class CurlTestBase:
    """CURL测试基类"""
    
    def __init__(self):
        """初始化测试基类"""
        self.base_url = 'http://localhost:5010'
        self.curl_commands_file = None
    
    def set_curl_commands_file(self, curl_commands_file):
        """设置curl命令记录文件"""
        self.curl_commands_file = curl_commands_file
    
    def _record_curl_command(self, test_number, description, command):
        """记录curl命令到文件"""
        if self.curl_commands_file:
            with open(self.curl_commands_file, 'a') as f:
                f.write(f"{test_number}. {description}\n")
                f.write(f"{' '.join(command)}\n\n")
    
    def run_api_test(self, test_number, description, command, output_file, test_setup):
        """运行单个API测试"""
        print(f"\n{test_number}. {description}")
        print(f"执行命令: {' '.join(command)}")
        
        # 记录curl命令到文件
        self._record_curl_command(test_number, description, command)
        
        # 执行测试命令
        result = subprocess.run(command, capture_output=True, text=True)
        
        # 保存结果
        output_path = os.path.join(test_setup['result_dir'], output_file)
        try:
            # 尝试解析为JSON
            json_data = json.loads(result.stdout)
            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=2)
        except json.JSONDecodeError:
            # 保存为文本
            with open(output_path, 'w') as f:
                f.write(result.stdout)
        
        # 验证结果
        assert result.returncode == 0, f"测试 {test_number} 失败: {result.stderr}"
        print(f"测试 {test_number} 完成")

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
    
    def test_public_endpoints(self, start_api_server, test_results_dir, curl_commands_file):
        """测试公共端点"""
        # 设置curl命令记录文件
        self.set_curl_commands_file(curl_commands_file)
        
        test_setup = {
            'api_base_url': self.base_url,
            'result_dir': test_results_dir,
            'cookie_file': '/tmp/test_cookie.txt'
        }
        
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