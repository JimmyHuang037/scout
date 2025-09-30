#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from .test_curl_base import CurlTestBase
from config import Config


class TestStudentEndpoints(CurlTestBase):
    """学生端点测试类 - 无需登录和会话的测试"""

    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.test_results_dir = Config.TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "student_curl_commands.log")
        
        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
        }

    def test_01_get_student_profile(self):
        """测试用例1: 获取学生个人资料（无需登录和会话）"""
        # 根据API实现，使用路径参数传递学生ID
        self.run_api_test(
            1, "获取学生个人资料",
            ['curl', '-s', f'{self.base_url}/api/student/S0101/profile', '|', 'jq'],
            "student_1_get_profile.json", self.test_setup
        )

    def test_02_get_student_scores(self):
        """测试用例2: 获取学生成绩（无需登录和会话）"""
        self.run_api_test(
            2, "获取学生成绩",
            ['curl', '-s', f'{self.base_url}/api/student/S0101/scores', '|', 'jq'],
            "student_2_get_scores.json", self.test_setup
        )

    def test_03_get_student_exam_results(self):
        """测试用例3: 获取学生考试结果（无需登录和会话）"""
        self.run_api_test(
            3, "获取学生考试结果",
            ['curl', '-s', f'{self.base_url}/api/student/S0101/exam_results', '|', 'jq'],
            "student_3_get_exam_results.json", self.test_setup
        )
