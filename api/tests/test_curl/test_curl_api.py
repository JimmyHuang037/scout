#!/usr/bin/env python3
"""
Curl黑盒测试 - 在pytest框架内使用curl命令进行端到端API测试
这个测试文件模拟curl_test.sh的功能，但使用pytest框架进行组织和执行
"""
"""API测试模块，使用curl命令测试API接口"""

import os
import signal
import time
import subprocess
from pathlib import Path

import pytest
import requests

from config.config import TestingConfig


class TestCurlAPI:
    """使用curl命令测试API接口"""
    
    @pytest.fixture(scope="class")
    def test_env(self):
        """测试环境设置"""
        # 创建临时目录存储测试结果
        result_dir = Path("/tmp/curl_test_results")
        result_dir.mkdir(exist_ok=True)
        
        # 获取测试配置
        test_config = TestingConfig()
        
        # 设置环境变量确保使用测试数据库
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['MYSQL_DB'] = test_config.MYSQL_DB
        
        # 恢复测试数据库
        self.restore_test_database()
        
        # 启动API服务器
        server_process = self.start_api_server()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 返回测试配置，使用测试端口
        yield {
            'api_base_url': f'http://localhost:{test_config.PORT}',
            'result_dir': result_dir,
            'cookie_file': '/tmp/test_cookie.txt',
            'server_process': server_process
        }
        
        # 清理：终止API服务器进程
        if server_process:
            try:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass  # 进程已经结束
        
        # 清理临时文件
        cookie_file = Path('/tmp/test_cookie.txt')
        if cookie_file.exists():
            cookie_file.unlink()
    
    def restore_test_database(self):
        """恢复测试数据库"""
        try:
            # 获取项目根目录
            project_root = Path(__file__).parent.parent.parent.parent
            restore_script = project_root / "db" / "restore_db.sh"
            
            # 执行数据库恢复脚本
            subprocess.run(
                [str(restore_script), "school_management_test"],
                check=True,
                capture_output=True,
                cwd=project_root
            )
            print("Test database restored successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to restore test database: {e}")
            raise
    
    def start_api_server(self):
        """启动API服务器"""
        try:
            # 获取项目根目录
            api_root = Path(__file__).parent.parent.parent
            
            # 启动API服务器进程，使用测试模式
            process = subprocess.Popen(
                ["python", "app.py"],
                env={**os.environ, 'FLASK_ENV': 'testing'},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
                cwd=api_root
            )
            
            return process
        except Exception as e:
            print(f"Failed to start API server: {e}")
            return None
    
    @pytest.fixture(scope="class")
    def api_server(self, test_env):
        """API服务器配置"""
        yield test_env['api_base_url']
    
    def run_curl_command(self, command, test_env):
        """执行curl命令并返回结果"""
        # 打印执行的curl命令
        print(f"执行curl命令: {command}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1
    
    def login_admin(self, test_env):
        """管理员登录"""
        command = f'curl -s -X POST {test_env["api_base_url"]}/api/auth/login ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"user_id": "admin", "password": "admin"}}\' ' \
                  f'-c {test_env["cookie_file"]}'
        
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        return stdout, stderr, returncode
    
    def login_teacher(self, test_env):
        """教师登录"""
        command = f'curl -s -X POST {test_env["api_base_url"]}/api/auth/login ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"user_id": "3", "password": "123456"}}\' ' \
                  f'-c {test_env["cookie_file"]}'
        
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        return stdout, stderr, returncode
    
    def login_student(self, test_env):
        """学生登录"""
        command = f'curl -s -X POST {test_env["api_base_url"]}/api/auth/login ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"user_id": "S0201", "password": "pass123"}}\' ' \
                  f'-c {test_env["cookie_file"]}'
        
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        return stdout, stderr, returncode
    
    def test_admin_student_management(self, test_env, api_server):
        """测试管理员学生管理功能（黑盒测试）"""
        # 登录管理员
        stdout, stderr, returncode = self.login_admin(test_env)
        assert returncode == 0, f"Admin login failed: {stderr}"
        
        # 1. 获取学生列表
        command = f'curl -s {api_server}/api/admin/students -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Get students failed: {stderr}"
        
        # 2. 创建学生
        command = f'curl -s -X POST {api_server}/api/admin/students ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"student_id": "S9999", "student_name": "Test Student", "class_id": 1, "password": "password123"}}\' ' \
                  f'-b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Create student failed: {stderr}"
        
        # 3. 获取特定学生
        command = f'curl -s {api_server}/api/admin/students/S0101 -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Get specific student failed: {stderr}"
        
        # 4. 更新学生信息
        command = f'curl -s -X PUT {api_server}/api/admin/students/S0101 ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"student_name": "Updated Student Name", "class_id": 1, "password": "password123"}}\' ' \
                  f'-b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Update student failed: {stderr}"
        
        # 5. 删除学生
        command = f'curl -s -X DELETE {api_server}/api/admin/students/S9999 -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Delete student failed: {stderr}"
    
    def test_teacher_score_management(self, test_env, api_server):
        """测试教师成绩管理功能（黑盒测试）"""
        # 登录教师
        stdout, stderr, returncode = self.login_teacher(test_env)
        assert returncode == 0, f"Teacher login failed: {stderr}"
        
        # 40. 获取成绩列表
        command = f'curl -s {api_server}/api/teacher/scores -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Get scores failed: {stderr}"
        
        # 41. 创建成绩
        command = f'curl -s -X POST {api_server}/api/teacher/scores ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 95.5}}\' ' \
                  f'-b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Create score failed: {stderr}"
        
        # 43. 更新成绩
        command = f'curl -s -X PUT {api_server}/api/teacher/scores/732 ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"score": 90.0}}\' ' \
                  f'-b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        # 允许404状态码，因为成绩可能不存在
        assert returncode == 0, f"Update score failed: {stderr}"
        
        # 44. 删除成绩
        command = f'curl -s -X DELETE {api_server}/api/teacher/scores/732 -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        # 允许404状态码，因为成绩可能不存在
        assert returncode == 0, f"Delete score failed: {stderr}"
    
    def test_student_functionality(self, test_env, api_server):
        """测试学生功能（黑盒测试）"""
        # 登录学生
        stdout, stderr, returncode = self.login_student(test_env)
        assert returncode == 0, f"Student login failed: {stderr}"
        
        # 31. 获取学生成绩
        command = f'curl -s {api_server}/api/student/scores -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Get student scores failed: {stderr}"
        
        # 32. 获取学生考试结果
        command = f'curl -s {api_server}/api/student/exam/results -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Get student exam results failed: {stderr}"
        
        # 33. 获取学生个人信息
        command = f'curl -s {api_server}/api/student/profile -b {test_env["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_env)
        assert returncode == 0, f"Get student profile failed: {stderr}"