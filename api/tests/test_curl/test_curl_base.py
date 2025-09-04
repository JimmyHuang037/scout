#!/usr/bin/env python3
"""
Curl测试基类
包含所有test_curl测试文件共享的方法和功能
"""

import os
import subprocess
import json
import shlex
from config.config import TestingConfig


class CurlTestBase:
    """Curl测试基类"""
    
    def setup_test_environment(self, test_environment):
        """设置测试环境配置"""
        # 确保curl_commands_file属性存在
        if not hasattr(self, 'curl_commands_file'):
            self.curl_commands_file = None
            
        if test_environment:
            self.base_url = test_environment['base_url']
            self.test_results_dir = test_environment['test_results_dir']
            self.curl_commands_file = test_environment['curl_commands_file']
            self.cookie_file = test_environment['cookie_file']
    
    def set_curl_commands_file(self, file_path):
        """设置curl命令记录文件路径"""
        self.curl_commands_file = file_path
    
    def _record_curl_command(self, test_number, description, command):
        """记录curl命令到文件"""
        if self.curl_commands_file:
            with open(self.curl_commands_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{test_number}. {description}\n")
                f.write(f"命令: {' '.join(command)}\n")
    
    def run_api_test(self, test_number, description, command, output_file, test_setup):
        """运行单个API测试"""
        print(f"\n{test_number}. {description}")
        print(f"执行命令: {' '.join(command)}")
        
        # 记录curl命令
        self._record_curl_command(test_number, description, command)
        
        # 使用shlex.join来正确处理命令参数中的引号
        if '|' not in ' '.join(command):
            # 如果命令中没有管道符，添加jq处理
            full_command = shlex.join(command) + ' | jq'
        else:
            # 如果已经有管道符，直接使用原命令
            full_command = shlex.join(command)
        
        # 执行测试命令
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
        
        # 保存结果
        output_path = os.path.join(test_setup['result_dir'], output_file)
        try:
            # 尝试解析为JSON
            json_data = json.loads(result.stdout)
            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
                
            # 检查返回的JSON中是否有error字段
            if 'error' in json_data and json_data['error']:
                assert False, f"测试 {test_number} 失败: API返回错误 - {json_data['error']}"
        except json.JSONDecodeError:
            # 保存为文本
            with open(output_path, 'w', encoding='utf-8') as f:
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
        
        # 记录curl命令
        self._record_curl_command("登录", "管理员登录", cmd)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"登录结果: returncode={result.returncode}, stdout={result.stdout}, stderr={result.stderr}")
        return result.returncode == 0
    
    def login_teacher(self, base_url, cookie_file):
        """教师登录"""
        print("登录教师账户...")
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "3", "password": "123456"}',
            '-c', cookie_file
        ]
        
        # 记录curl命令
        self._record_curl_command("登录", "教师登录", cmd)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"登录结果: returncode={result.returncode}, stdout={result.stdout}, stderr={result.stderr}")
        return result.returncode == 0
    
    def login_student(self, base_url, cookie_file):
        """学生登录"""
        print("登录学生账户...")
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"user_id": "S0201", "password": "pass123"}',
            '-c', cookie_file
        ]
        
        # 记录curl命令
        self._record_curl_command("登录", "学生登录", cmd)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"登录结果: returncode={result.returncode}, stdout={result.stdout}, stderr={result.stderr}")
        return result.returncode == 0
    
    def logout(self, base_url, cookie_file):
        """登出"""
        print("登出账户...")
        cmd = [
            'curl', '-s', '-X', 'POST', f'{base_url}/api/auth/logout',
            '-b', cookie_file
        ]
        
        # 记录curl命令
        self._record_curl_command("登出", "用户登出", cmd)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0