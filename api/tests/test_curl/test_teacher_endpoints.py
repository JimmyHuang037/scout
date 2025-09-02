#!/usr/bin/env python3
"""
教师端点测试
使用 pytest 框架执行黑盒测试
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


class TestTeacherEndpoints:
    """教师端点测试类"""
    
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
    
    def run_api_test(self, test_number, description, command, output_file, test_setup):
        """运行单个API测试"""
        print(f"\n{test_number}. {description}")
        print(f"执行命令: {' '.join(command)}")
        
        # 教师登录
        self.login_teacher(test_setup['api_base_url'], test_setup['cookie_file'])
        
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
    
    def test_teacher_exam_type_endpoints(self, start_api_server):
        """测试教师考试类型管理端点"""
        base_url = 'http://localhost:5010'
        cookie_file = '/tmp/test_cookie.txt'
        result_dir = '/tmp/curl_test_results'
        os.makedirs(result_dir, exist_ok=True)
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': result_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例21: 获取考试类型列表(教师)
        self.run_api_test(
            21, "获取考试类型列表(教师)",
            ['curl', '-s', f'{base_url}/api/admin/exam-types', '-b', cookie_file],
            "21_get_exam_types.json", test_setup
        )
        
        # 测试用例22: 创建考试类型
        self.run_api_test(
            22, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/admin/exam-types',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Test Exam Type"}',
             '-b', cookie_file],
            "22_create_exam_type.json", test_setup
        )
        
        # 测试用例23: 获取特定考试类型
        self.run_api_test(
            23, "获取特定考试类型",
            ['curl', '-s', f'{base_url}/api/admin/exam-types/1', '-b', cookie_file],
            "23_get_exam_type.json", test_setup
        )
        
        # 测试用例24: 更新考试类型信息
        self.run_api_test(
            24, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/admin/exam-types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Updated Exam Type Name"}',
             '-b', cookie_file],
            "24_update_exam_type.json", test_setup
        )
        
        # 测试用例25: 删除考试类型
        self.run_api_test(
            25, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/admin/exam-types/1', '-b', cookie_file],
            "25_delete_exam_type.json", test_setup
        )
    
    def test_teacher_score_endpoints(self, start_api_server):
        """测试教师成绩管理端点"""
        base_url = 'http://localhost:5010'
        cookie_file = '/tmp/test_cookie.txt'
        result_dir = '/tmp/curl_test_results'
        os.makedirs(result_dir, exist_ok=True)
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': result_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例26: 教师获取任教班级列表
        self.run_api_test(
            26, "教师获取任教班级列表",
            ['curl', '-s', f'{base_url}/api/teacher/exam/classes', '-b', cookie_file],
            "26_get_teacher_classes.json", test_setup
        )
        
        # 测试用例27: 教师获取学生成绩列表
        self.run_api_test(
            27, "教师获取学生成绩列表",
            ['curl', '-s', f'{base_url}/api/teacher/scores', '-b', cookie_file],
            "27_get_teacher_scores.json", test_setup
        )
        
        # 测试用例28: 教师创建学生成绩
        self.run_api_test(
            28, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', cookie_file],
            "28_create_score.json", test_setup
        )
        
        # 测试用例29: 教师更新学生成绩
        self.run_api_test(
            29, "教师更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 90}',
             '-b', cookie_file],
            "29_update_score.json", test_setup
        )
        
        # 测试用例30: 教师删除学生成绩
        self.run_api_test(
            30, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/teacher/scores/1', '-b', cookie_file],
            "30_delete_score.json", test_setup
        )
    
    def test_teacher_exam_endpoints(self, start_api_server):
        """测试教师考试管理端点"""
        base_url = 'http://localhost:5010'
        cookie_file = '/tmp/test_cookie.txt'
        result_dir = '/tmp/curl_test_results'
        os.makedirs(result_dir, exist_ok=True)
        
        test_setup = {
            'api_base_url': base_url,
            'result_dir': result_dir,
            'cookie_file': cookie_file
        }
        
        # 测试用例31: 教师获取考试列表
        self.run_api_test(
            31, "教师获取考试列表",
            ['curl', '-s', f'{base_url}/api/teacher/exams', '-b', cookie_file],
            "31_get_exams.json", test_setup
        )
        
        # 测试用例32: 教师创建考试
        self.run_api_test(
            32, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Test Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-09-01"}',
             '-b', cookie_file],
            "32_create_exam.json", test_setup
        )
        
        # 测试用例33: 教师获取特定考试
        self.run_api_test(
            33, "教师获取特定考试",
            ['curl', '-s', f'{base_url}/api/teacher/exams/1', '-b', cookie_file],
            "33_get_exam.json", test_setup
        )
        
        # 测试用例34: 教师更新考试信息
        self.run_api_test(
            34, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Exam Name"}',
             '-b', cookie_file],
            "34_update_exam.json", test_setup
        )
        
        # 测试用例35: 教师删除考试
        self.run_api_test(
            35, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/teacher/exams/1', '-b', cookie_file],
            "35_delete_exam.json", test_setup
        )