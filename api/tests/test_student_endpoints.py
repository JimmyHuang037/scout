#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import pytest
from config import Config


class TestStudentEndpoints:
    """学生端点测试类 - 无需登录和会话的测试"""

    @pytest.fixture(autouse=True)
    def setup_method(self, restore_database):
        """每个测试方法运行前自动重置数据库"""
        self.base_url = f"http://{Config.HOST}:{Config.PORT}"
        self.test_results_dir = Config.CURL_TEST_DIR
        os.makedirs(self.test_results_dir, exist_ok=True)

    def test_01_get_student_profile(self):
        """测试用例1: 获取学生个人资料（无需登录和会话）"""
        print("测试获取学生个人资料...")

        # 直接访问API端点，不附加任何认证信息
        curl_cmd = [
            "curl", "-s", f"{self.base_url}/api/student/profile"
        ]

        # 执行测试
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # 验证结果
        assert result.returncode == 0, f"请求失败: {result.stderr}"

        # 解析响应
        try:
            response_data = json.loads(result.stdout)
            print(f"响应数据: {response_data}")
            # 验证返回的数据结构
            assert "success" in response_data
            if response_data["success"]:
                assert "data" in response_data
        except json.JSONDecodeError:
            assert False, f"响应不是有效的JSON格式: {result.stdout}"

    def test_02_get_student_scores(self):
        """测试用例2: 获取学生成绩（无需登录和会话）"""
        print("测试获取学生成绩...")

        # 直接访问API端点，不附加任何认证信息
        curl_cmd = [
            "curl", "-s", f"{self.base_url}/api/student/scores"
        ]

        # 执行测试
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # 验证结果
        assert result.returncode == 0, f"请求失败: {result.stderr}"

        # 解析响应
        try:
            response_data = json.loads(result.stdout)
            print(f"响应数据: {response_data}")
            # 验证返回的数据结构
            assert "success" in response_data
            if response_data["success"]:
                assert "data" in response_data
        except json.JSONDecodeError:
            assert False, f"响应不是有效的JSON格式: {result.stdout}"

    def test_03_get_student_exam_results(self):
        """测试用例3: 获取学生考试结果（无需登录和会话）"""
        print("测试获取学生考试结果...")

        # 直接访问API端点，不附加任何认证信息
        curl_cmd = [
            "curl", "-s", f"{self.base_url}/api/student/exam/results"
        ]

        # 执行测试
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # 验证结果
        assert result.returncode == 0, f"请求失败: {result.stderr}"

        # 解析响应
        try:
            response_data = json.loads(result.stdout)
            print(f"响应数据: {response_data}")
            # 验证返回的数据结构
            assert "success" in response_data
            if response_data["success"]:
                assert "data" in response_data
        except json.JSONDecodeError:
            assert False, f"响应不是有效的JSON格式: {result.stdout}"