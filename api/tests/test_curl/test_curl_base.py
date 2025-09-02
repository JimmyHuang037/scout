呕#!/usr/bin/env python3
"""
Curl测试基类
包含所有test_curl测试文件共享的方法和功能
"""

import os
import subprocess
import json
from config.config import TestingConfig


class CurlTestBase:
    """Curl测试基类"""
    
    def __init__(self):
        """初始化测试基类"""
        self.test_config = TestingConfig()
        self.base_url = f'http://localhost:{self.test_config.PORT}'
    
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
    
    def login_admin(self, base_url, cookie_file):
        """管理员登录"""
        print("登录管理员账户...")
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "admin", "password": "admin"}',
            '-c', cookie_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    def login_teacher(self, base_url, cookie_file):
        """教师登录"""
        print("登录教师账户...")
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "3", "password": "123456"}',
            '-c', cookie_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    def login_student(self, base_url, cookie_file):
        """学生登录"""
        print("登录学生账户...")
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "S0201", "password": "pass123"}',
            '-c', cookie_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout