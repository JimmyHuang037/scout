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
    
    def run_api_test(self, test_number, description, command, output_file, test_setup):
        """运行单个API测试"""
        print(f"\n{test_number}. {description}")
        print(f"执行命令: {' '.join(command)}")
        
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
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestPublicEndpoints(CurlTestBase):
    """公共端点测试类"""
    
    def test_public_endpoints(self, start_api_server, test_results_dir):
        """测试公共端点"""
        base_url = 'http://localhost:5010'
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': test_results_dir,
            'cookie_file': '/tmp/test_cookie.txt'
        }
        
        # 测试用例38: 健康检查
        self.run_api_test(
            38, "健康检查",
            ['curl', '-s', f'{base_url}/api/auth/health'],
            "38_health_check.json", test_setup
        )
        
        # 测试用例39: 登录
        print("\n39. 登录")
        print("执行命令: curl -s -X POST http://localhost:5010/api/auth/login -H \"Content-Type: application/json\" -d '{\"user_id\": \"admin\", \"password\": \"admin\"}'")
        
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        output_path = os.path.join(test_setup['result_dir'], "39_login.json")
        
        try:
            json_data = json.loads(result.stdout)
            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=2)
        except json.JSONDecodeError:
            with open(output_path, 'w') as f:
                f.write(result.stdout)
        
        assert result.returncode == 0, f"测试 39 失败: {result.stderr}"
        print("测试 39 完成")
        
        # 测试用例40: 登出
        print("\n40. 登出")
        print("执行命令: curl -s -X POST http://localhost:5010/api/auth/logout -b /tmp/test_cookie.txt")
        
        # 首先需要登录以获取cookie
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}',
            '-c', test_setup['cookie_file']
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        
        # 然后执行登出
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/logout',
            '-b', test_setup['cookie_file']
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        output_path = os.path.join(test_setup['result_dir'], "40_logout.json")
        
        try:
            json_data = json.loads(result.stdout)
            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=2)
        except json.JSONDecodeError:
            with open(output_path, 'w') as f:
                f.write(result.stdout)
        
        assert result.returncode == 0, f"测试 40 失败: {result.stderr}"
        print("测试 40 完成")