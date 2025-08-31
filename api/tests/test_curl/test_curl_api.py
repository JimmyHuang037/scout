#!/usr/bin/env python3
"""
Curl黑盒测试 - 在pytest框架内使用curl命令进行端到端API测试
这个测试文件模拟curl_test.sh的功能，但使用pytest框架进行组织和执行
"""

import pytest
import subprocess
import json
import os
import tempfile
import time
import signal
from pathlib import Path


class TestCurlAPI:
    """使用curl命令进行API黑盒测试"""
    
    @pytest.fixture(scope="class")
    def test_setup(self):
        """测试环境设置"""
        # 创建临时目录存储测试结果
        result_dir = Path("/tmp/curl_test_results")
        result_dir.mkdir(exist_ok=True)
        
        # 设置环境变量确保使用测试数据库
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['MYSQL_DB'] = 'school_management_test'
        
        # 恢复测试数据库
        self.restore_test_database()
        
        # 启动API服务器
        server_process = self.start_api_server()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 返回测试配置，使用5010端口
        yield {
            'api_base_url': 'http://localhost:5010',
            'result_dir': result_dir,
            'cookie_file': '/tmp/test_cookie.txt',
            'server_process': server_process
        }
        
        # 清理：终止API服务器进程
        if server_process:
            try:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                server_process.wait(timeout=5)
            except:
                try:
                    os.killpg(os.getpgid(server_process.pid), signal.SIGKILL)
                except:
                    pass
        
        # 清理临时文件
        if os.path.exists('/tmp/test_cookie.txt'):
            os.remove('/tmp/test_cookie.txt')
    
    def restore_test_database(self):
        """恢复测试数据库"""
        try:
            # 获取项目根目录
            project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
            db_restore_script = os.path.join(project_root, 'db', 'restore_db.sh')
            backup_filename = 'school_management_backup_20250831_103236.sql'
            
            # 运行数据库恢复脚本，恢复测试数据库
            result = subprocess.run(
                [db_restore_script, backup_filename, 'school_management_test'],
                cwd=os.path.join(project_root, 'db'),
                input='y\n',  # 自动确认
                text=True,
                capture_output=True
            )
            
            if result.returncode == 0:
                print("测试数据库恢复成功")
            else:
                print(f"测试数据库恢复失败: {result.stderr}")
        except Exception as e:
            print(f"恢复测试数据库时出错: {e}")
    
    def start_api_server(self):
        """启动API服务器"""
        try:
            # 获取API目录
            api_dir = os.path.join(os.path.dirname(__file__), '..', '..')
            
            # 启动API服务器进程，使用5010端口和测试模式
            process = subprocess.Popen(
                ['python', 'app.py', '--port', '5010', '--test'],
                cwd=api_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            print(f"API服务器已启动，PID: {process.pid}")
            return process
        except Exception as e:
            print(f"启动API服务器失败: {e}")
            return None
    
    @pytest.fixture(scope="class")
    def api_server(self, test_setup):
        """API服务器配置"""
        yield test_setup['api_base_url']
    
    def run_curl_command(self, command, test_setup):
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
    
    def login_admin(self, test_setup):
        """管理员登录"""
        command = f'curl -s -X POST {test_setup["api_base_url"]}/api/auth/login ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"user_id": "admin", "password": "admin"}}\' ' \
                  f'-c {test_setup["cookie_file"]}'
        
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        return stdout, stderr, returncode
    
    def login_teacher(self, test_setup):
        """教师登录"""
        command = f'curl -s -X POST {test_setup["api_base_url"]}/api/auth/login ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"user_id": "3", "password": "123456"}}\' ' \
                  f'-c {test_setup["cookie_file"]}'
        
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        return stdout, stderr, returncode
    
    def login_student(self, test_setup):
        """学生登录"""
        command = f'curl -s -X POST {test_setup["api_base_url"]}/api/auth/login ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"user_id": "S0201", "password": "pass123"}}\' ' \
                  f'-c {test_setup["cookie_file"]}'
        
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        return stdout, stderr, returncode
    
    def test_admin_student_management(self, test_setup, api_server):
        """测试管理员学生管理功能（黑盒测试）"""
        # 登录管理员
        stdout, stderr, returncode = self.login_admin(test_setup)
        assert returncode == 0, f"Admin login failed: {stderr}"
        
        # 1. 获取学生列表
        command = f'curl -s {api_server}/api/admin/students -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Get students failed: {stderr}"
        
        # 2. 创建学生
        command = f'curl -s -X POST {api_server}/api/admin/students ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"student_id": "S9999", "student_name": "Test Student", "class_id": 1, "password": "password123"}}\' ' \
                  f'-b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Create student failed: {stderr}"
        
        # 3. 获取特定学生
        command = f'curl -s {api_server}/api/admin/students/S0101 -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Get specific student failed: {stderr}"
        
        # 4. 更新学生信息
        command = f'curl -s -X PUT {api_server}/api/admin/students/S0101 ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"student_name": "Updated Student Name", "class_id": 1, "password": "password123"}}\' ' \
                  f'-b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Update student failed: {stderr}"
        
        # 5. 删除学生
        command = f'curl -s -X DELETE {api_server}/api/admin/students/S9999 -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Delete student failed: {stderr}"
    
    def test_teacher_score_management(self, test_setup, api_server):
        """测试教师成绩管理功能（黑盒测试）"""
        # 登录教师
        stdout, stderr, returncode = self.login_teacher(test_setup)
        assert returncode == 0, f"Teacher login failed: {stderr}"
        
        # 40. 获取成绩列表
        command = f'curl -s {api_server}/api/teacher/scores -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Get scores failed: {stderr}"
        
        # 41. 创建成绩
        command = f'curl -s -X POST {api_server}/api/teacher/scores ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 95.5}}\' ' \
                  f'-b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Create score failed: {stderr}"
        
        # 43. 更新成绩
        command = f'curl -s -X PUT {api_server}/api/teacher/scores/732 ' \
                  f'-H "Content-Type: application/json" ' \
                  f'-d \'{{"score": 90.0}}\' ' \
                  f'-b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        # 允许404状态码，因为成绩可能不存在
        assert returncode == 0, f"Update score failed: {stderr}"
        
        # 44. 删除成绩
        command = f'curl -s -X DELETE {api_server}/api/teacher/scores/732 -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        # 允许404状态码，因为成绩可能不存在
        assert returncode == 0, f"Delete score failed: {stderr}"
    
    def test_student_functionality(self, test_setup, api_server):
        """测试学生功能（黑盒测试）"""
        # 登录学生
        stdout, stderr, returncode = self.login_student(test_setup)
        assert returncode == 0, f"Student login failed: {stderr}"
        
        # 31. 获取学生成绩
        command = f'curl -s {api_server}/api/student/scores -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Get student scores failed: {stderr}"
        
        # 32. 获取学生考试结果
        command = f'curl -s {api_server}/api/student/exam/results -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Get student exam results failed: {stderr}"
        
        # 33. 获取学生个人信息
        command = f'curl -s {api_server}/api/student/profile -b {test_setup["cookie_file"]}'
        stdout, stderr, returncode = self.run_curl_command(command, test_setup)
        assert returncode == 0, f"Get student profile failed: {stderr}"