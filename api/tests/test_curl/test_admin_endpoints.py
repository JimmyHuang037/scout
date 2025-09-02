#!/usr/bin/env python3
"""
Curl 测试基类
提供通用的测试方法和设置
"""

import os
import time
import subprocess
import signal
import json
import pytest
from urllib import request
from urllib.error import URLError
from pathlib import Path

# 导入配置
from config.config import TestingConfig


class CurlTestBase:
    """Curl 测试基类，提供通用测试功能"""

    def __init__(self):
        test_config = TestingConfig()
        self.base_url = f'http://localhost:{test_config.PORT}'

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

    def run_api_test(self, test_number, description, command, output_file, test_setup):
        """运行单个API测试"""
        print(f"\n{test_number}. {description}")
        print(f"执行命令: {' '.join(command)}")

        # 管理员登录
        self.login_admin(test_setup['api_base_url'], test_setup['cookie_file'])

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
管理员端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestAdminEndpoints(CurlTestBase):
    """管理员端点测试类"""
    
    def test_admin_student_endpoints(self, start_api_server, test_results_dir):
        """测试管理员学生管理端点"""
        test_config = TestingConfig()
        base_url = f'http://localhost:{test_config.PORT}'
        cookie_file = '/tmp/test_cookie.txt'
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': test_results_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例1: 获取学生列表
        self.run_api_test(
            1, "获取学生列表",
            ['curl', '-s', f'{base_url}/api/admin/students', '-b', cookie_file],
            "1_get_students.json", test_setup
        )
        
        # 测试用例2: 创建学生
        self.run_api_test(
            2, "创建学生",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/admin/students',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S9999", "student_name": "Test Student", "class_id": 1, "password": "password123"}',
             '-b', cookie_file],
            "2_create_student.json", test_setup
        )
        
        # 测试用例3: 获取特定学生
        self.run_api_test(
            3, "获取特定学生",
            ['curl', '-s', f'{base_url}/api/admin/students/S0101', '-b', cookie_file],
            "3_get_student.json", test_setup
        )
        
        # 测试用例4: 更新学生信息
        self.run_api_test(
            4, "更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/admin/students/S0101',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "Updated Student Name", "class_id": 1, "password": "password123"}',
             '-b', cookie_file],
            "4_update_student.json", test_setup
        )
        
        # 测试用例5: 删除学生
        self.run_api_test(
            5, "删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/admin/students/S9999', '-b', cookie_file],
            "5_delete_student.json", test_setup
        )
    
    def test_admin_teacher_endpoints(self, start_api_server, test_results_dir):
        """测试管理员教师管理端点"""
        base_url = 'http://localhost:5010'
        cookie_file = '/tmp/test_cookie.txt'
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': test_results_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例6: 获取教师列表
        self.run_api_test(
            6, "获取教师列表",
            ['curl', '-s', f'{base_url}/api/admin/teachers', '-b', cookie_file],
            "6_get_teachers.json", test_setup
        )
        
        # 测试用例7: 创建教师
        self.run_api_test(
            7, "创建教师",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/admin/teachers',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "Test Teacher", "teacher_id": 999, "subject_id": 1, "password": "password123"}',
             '-b', cookie_file],
            "7_create_teacher.json", test_setup
        )
        
        # 测试用例8: 获取特定教师
        self.run_api_test(
            8, "获取特定教师",
            ['curl', '-s', f'{base_url}/api/admin/teachers/1', '-b', cookie_file],
            "8_get_teacher.json", test_setup
        )
        
        # 测试用例9: 更新教师信息
        self.run_api_test(
            9, "更新教师信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/admin/teachers/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "Updated Teacher Name"}',
             '-b', cookie_file],
            "9_update_teacher.json", test_setup
        )
        
        # 测试用例10: 删除教师
        self.run_api_test(
            10, "删除教师",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/admin/teachers/999', '-b', cookie_file],
            "10_delete_teacher.json", test_setup
        )
    
    def test_admin_class_endpoints(self, start_api_server, test_results_dir):
        """测试管理员班级管理端点"""
        base_url = 'http://localhost:5010'
        cookie_file = '/tmp/test_cookie.txt'
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': test_results_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例11: 获取班级列表
        self.run_api_test(
            11, "获取班级列表",
            ['curl', '-s', f'{base_url}/api/admin/classes', '-b', cookie_file],
            "11_get_classes.json", test_setup
        )
        
        # 测试用例12: 创建班级
        self.run_api_test(
            12, "创建班级",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/admin/classes',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "Test Class"}',
             '-b', cookie_file],
            "12_create_class.json", test_setup
        )
        
        # 测试用例13: 获取特定班级
        self.run_api_test(
            13, "获取特定班级",
            ['curl', '-s', f'{base_url}/api/admin/classes/1', '-b', cookie_file],
            "13_get_class.json", test_setup
        )
        
        # 测试用例14: 更新班级信息
        self.run_api_test(
            14, "更新班级信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/admin/classes/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "Updated Class Name", "grade": 1}',
             '-b', cookie_file],
            "14_update_class.json", test_setup
        )
        
        # 测试用例15: 删除班级
        self.run_api_test(
            15, "删除班级",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/admin/classes/1', '-b', cookie_file],
            "15_delete_class.json", test_setup
        )
    
    def test_admin_subject_endpoints(self, start_api_server, test_results_dir):
        """测试管理员科目管理端点"""
        base_url = 'http://localhost:5010'
        cookie_file = '/tmp/test_cookie.txt'
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': test_results_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例16: 获取科目列表(管理员)
        self.run_api_test(
            16, "获取科目列表(管理员)",
            ['curl', '-s', f'{base_url}/api/admin/subjects', '-b', cookie_file],
            "16_get_subjects.json", test_setup
        )
        
        # 测试用例17: 创建科目
        self.run_api_test(
            17, "创建科目",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/admin/subjects',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "Test Subject"}',
             '-b', cookie_file],
            "17_create_subject.json", test_setup
        )
        
        # 测试用例18: 获取特定科目
        self.run_api_test(
            18, "获取特定科目",
            ['curl', '-s', f'{base_url}/api/admin/subjects/1', '-b', cookie_file],
            "18_get_subject.json", test_setup
        )
        
        # 测试用例19: 更新科目信息
        self.run_api_test(
            19, "更新科目信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/admin/subjects/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "Updated Subject Name"}',
             '-b', cookie_file],
            "19_update_subject.json", test_setup
        )
        
        # 测试用例20: 删除科目
        self.run_api_test(
            20, "删除科目",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/admin/subjects/1', '-b', cookie_file],
            "20_delete_subject.json", test_setup
        )