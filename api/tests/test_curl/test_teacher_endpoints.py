#!/usr/bin/env python3
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, test_environment):
        """自动使用的fixture，用于设置测试环境"""
        # 设置测试环境配置
        self.setup_test_environment(test_environment)
        
        # 设置curl命令记录文件
        self.set_curl_commands_file(self.curl_commands_file)
        
        # 登录教师账户
        assert self.login_teacher(self.base_url, self.cookie_file), "教师登录失败"
        
        # 保存环境变量供测试方法使用
        self.test_setup = {
            'api_base_url': self.base_url,
            'result_dir': self.test_results_dir,
            'cookie_file': self.cookie_file
        }
        
        yield  # 测试执行完毕后继续执行下面的代码
        
        # 测试结束后登出
        self.logout(self.base_url, self.cookie_file)
    
    def test_01_get_exam_types(self):
        """测试用例1: 获取考试类型列表(教师)"""
        self.run_api_test(
            1, "获取考试类型列表(教师)",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types', '-b', self.cookie_file],
            "1_get_exam_types.json", self.test_setup
        )
    
    def test_02_create_exam_type(self):
        """测试用例2: 创建考试类型"""
        self.run_api_test(
            2, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exam-types',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Test Exam Type"}',
             '-b', self.cookie_file],
            "2_create_exam_type.json", self.test_setup
        )
    
    def test_03_get_specific_exam_type(self):
        """测试用例3: 获取特定考试类型"""
        self.run_api_test(
            3, "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types/1', '-b', self.cookie_file],
            "3_get_exam_type.json", self.test_setup
        )
    
    def test_04_update_exam_type(self):
        """测试用例4: 更新考试类型信息"""
        self.run_api_test(
            4, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam-types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Updated Exam Type Name"}',
             '-b', self.cookie_file],
            "4_update_exam_type.json", self.test_setup
        )
    
    def test_05_delete_exam_type(self):
        """测试用例5: 删除考试类型"""
        self.run_api_test(
            5, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam-types/10', '-b', self.cookie_file],
            "5_delete_exam_type.json", self.test_setup
        )
    
    def test_06_get_teacher_classes(self):
        """测试用例6: 教师获取任教班级列表"""
        self.run_api_test(
            6, "教师获取任教班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam/classes', '-b', self.cookie_file],
            "6_get_teacher_classes.json", self.test_setup
        )
    
    def test_07_get_scores(self):
        """测试用例7: 教师获取学生成绩列表"""
        self.run_api_test(
            7, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores', '-b', self.cookie_file],
            "7_get_teacher_scores.json", self.test_setup
        )
    
    def test_08_create_score(self):
        """测试用例8: 教师创建学生成绩"""
        self.run_api_test(
            8, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', self.cookie_file],
            "8_create_score.json", self.test_setup
        )
    
    def test_09_update_score(self):
        """测试用例9: 教师更新学生成绩"""
        self.run_api_test(
            9, "教师更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 90}',
             '-b', self.cookie_file],
            "9_update_score.json", self.test_setup
        )
    
    def test_10_delete_score(self):
        """测试用例10: 教师删除学生成绩"""
        self.run_api_test(
            10, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/scores/10', '-b', self.cookie_file],
            "10_delete_score.json", self.test_setup
        )
    
    def test_11_get_exams(self):
        """测试用例11: 教师获取考试列表"""
        self.run_api_test(
            11, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '-b', self.cookie_file],
            "11_get_exams.json", self.test_setup
        )
    
    def test_12_create_exam(self):
        """测试用例12: 教师创建考试"""
        self.run_api_test(
            12, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Test Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-09-01"}',
             '-b', self.cookie_file],
            "12_create_exam.json", self.test_setup
        )
    
    def test_13_get_specific_exam(self):
        """测试用例13: 教师获取特定考试"""
        self.run_api_test(
            13, "教师获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "13_get_exam.json", self.test_setup
        )
    
    def test_14_update_exam(self):
        """测试用例14: 教师更新考试信息"""
        self.run_api_test(
            14, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Exam Name"}',
             '-b', self.cookie_file],
            "14_update_exam.json", self.test_setup
        )
    
    def test_15_delete_exam(self):
        """测试用例15: 教师删除考试"""
        self.run_api_test(
            15, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/10', '-b', self.cookie_file],
            "15_delete_exam.json", self.test_setup
        )
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""

import os
import pytest
from tests.test_curl.test_curl_base import CurlTestBase


class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类"""
    
    @classmethod
    def setup_class(cls):
        """在类级别设置测试环境并登录"""
        pass
    
    @classmethod
    def teardown_class(cls):
        """在类级别登出"""
        pass
    
    @pytest.fixture(autouse=True)
    def _setup_test_environment(self, test_environment):
        """自动使用的fixture，用于设置测试环境"""
        # 创建类实例以访问基类方法
        instance = self.__class__()
        
        # 设置测试环境配置
        instance.setup_test_environment(test_environment)
        
        # 保存配置到类属性
        self.__class__.base_url = instance.base_url
        self.__class__.test_results_dir = instance.test_results_dir
        self.__class__.curl_commands_file = instance.curl_commands_file
        self.__class__.cookie_file = instance.cookie_file
        
        # 设置curl命令记录文件
        instance.set_curl_commands_file(self.__class__.curl_commands_file)
        
        # 教师登录
        assert instance.login_teacher(self.__class__.base_url, self.__class__.cookie_file), "教师登录失败"
    
    def setup_method(self, method):
        """每个测试方法执行前的设置"""
        # 设置测试环境
        self.test_setup = {
            'api_base_url': getattr(self, 'base_url', None),
            'result_dir': getattr(self, 'test_results_dir', None),
            'cookie_file': getattr(self, 'cookie_file', None)
        }
    
    def test_01_get_exam_types(self, test_environment):
        """测试用例1: 获取考试类型列表(教师)"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            1, "获取考试类型列表(教师)",
            ['curl', '-s', f'{base_url}/api/admin/exam-types', '-b', cookie_file],
            "1_get_exam_types.json", self.test_setup
        )
    
    def test_02_create_exam_type(self, test_environment):
        """测试用例2: 创建考试类型"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            2, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/admin/exam-types',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Test Exam Type"}',
             '-b', cookie_file],
            "2_create_exam_type.json", self.test_setup
        )
    
    def test_03_get_specific_exam_type(self, test_environment):
        """测试用例3: 获取特定考试类型"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            3, "获取特定考试类型",
            ['curl', '-s', f'{base_url}/api/admin/exam-types/1', '-b', cookie_file],
            "3_get_exam_type.json", self.test_setup
        )
    
    def test_04_update_exam_type(self, test_environment):
        """测试用例4: 更新考试类型信息"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            4, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/admin/exam-types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Updated Exam Type Name"}',
             '-b', cookie_file],
            "4_update_exam_type.json", self.test_setup
        )
    
    def test_05_delete_exam_type(self, test_environment):
        """测试用例5: 删除考试类型"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            5, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/admin/exam-types/10', '-b', cookie_file],
            "5_delete_exam_type.json", self.test_setup
        )
    
    def test_06_get_teacher_classes(self, test_environment):
        """测试用例6: 教师获取任教班级列表"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            6, "教师获取任教班级列表",
            ['curl', '-s', f'{base_url}/api/teacher/exam/classes', '-b', cookie_file],
            "6_get_teacher_classes.json", self.test_setup
        )
    
    def test_07_get_scores(self, test_environment):
        """测试用例7: 教师获取学生成绩列表"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            7, "教师获取学生成绩列表",
            ['curl', '-s', f'{base_url}/api/teacher/scores', '-b', cookie_file],
            "7_get_teacher_scores.json", self.test_setup
        )
    
    def test_08_create_score(self, test_environment):
        """测试用例8: 教师创建学生成绩"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            8, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', cookie_file],
            "8_create_score.json", self.test_setup
        )
    
    def test_09_update_score(self, test_environment):
        """测试用例9: 教师更新学生成绩"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            9, "教师更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 90}',
             '-b', cookie_file],
            "9_update_score.json", self.test_setup
        )
    
    def test_10_delete_score(self, test_environment):
        """测试用例10: 教师删除学生成绩"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            10, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/teacher/scores/10', '-b', cookie_file],
            "10_delete_score.json", self.test_setup
        )
    
    def test_11_get_exams(self, test_environment):
        """测试用例11: 教师获取考试列表"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            11, "教师获取考试列表",
            ['curl', '-s', f'{base_url}/api/teacher/exams', '-b', cookie_file],
            "11_get_exams.json", self.test_setup
        )
    
    def test_12_create_exam(self, test_environment):
        """测试用例12: 教师创建考试"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            12, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Test Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-09-01"}',
             '-b', cookie_file],
            "12_create_exam.json", self.test_setup
        )
    
    def test_13_get_specific_exam(self, test_environment):
        """测试用例13: 教师获取特定考试"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            13, "教师获取特定考试",
            ['curl', '-s', f'{base_url}/api/teacher/exams/1', '-b', cookie_file],
            "13_get_exam.json", self.test_setup
        )
    
    def test_14_update_exam(self, test_environment):
        """测试用例14: 教师更新考试信息"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            14, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Exam Name"}',
             '-b', cookie_file],
            "14_update_exam.json", self.test_setup
        )
    
    def test_15_delete_exam(self, test_environment):
        """测试用例15: 教师删除考试"""
        base_url = test_environment["api_base_url"]
        cookie_file = test_environment["cookie_file"]
        self.run_api_test(
            15, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{base_url}/api/teacher/exams/10', '-b', cookie_file],
            "15_delete_exam.json", self.test_setup
        )
    
    def test_01_get_exam_types(self):
        """测试用例1: 获取考试类型列表(教师)"""
        self.run_api_test(
            1, "获取考试类型列表(教师)",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types', '-b', self.cookie_file],
            "1_get_exam_types.json", self.test_setup
        )
    
    def test_02_create_exam_type(self):
        """测试用例2: 创建考试类型"""
        self.run_api_test(
            2, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exam-types',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Test Exam Type"}',
             '-b', self.cookie_file],
            "2_create_exam_type.json", self.test_setup
        )
    
    def test_03_get_specific_exam_type(self):
        """测试用例3: 获取特定考试类型"""
        self.run_api_test(
            3, "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam-types/1', '-b', self.cookie_file],
            "3_get_exam_type.json", self.test_setup
        )
    
    def test_04_update_exam_type(self):
        """测试用例4: 更新考试类型信息"""
        self.run_api_test(
            4, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam-types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "Updated Exam Type Name"}',
             '-b', self.cookie_file],
            "4_update_exam_type.json", self.test_setup
        )
    
    def test_05_delete_exam_type(self):
        """测试用例5: 删除考试类型"""
        self.run_api_test(
            5, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam-types/10', '-b', self.cookie_file],
            "5_delete_exam_type.json", self.test_setup
        )
    
    def test_06_get_teacher_classes(self):
        """测试用例6: 教师获取任教班级列表"""
        self.run_api_test(
            6, "教师获取任教班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exam/classes', '-b', self.cookie_file],
            "6_get_teacher_classes.json", self.test_setup
        )
    
    def test_07_get_scores(self):
        """测试用例7: 教师获取学生成绩列表"""
        self.run_api_test(
            7, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores', '-b', self.cookie_file],
            "7_get_teacher_scores.json", self.test_setup
        )
    
    def test_08_create_score(self):
        """测试用例8: 教师创建学生成绩"""
        self.run_api_test(
            8, "教师创建学生成绩",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/scores',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S0201", "subject_id": 1, "exam_type_id": 1, "score": 85}',
             '-b', self.cookie_file],
            "8_create_score.json", self.test_setup
        )
    
    def test_09_update_score(self):
        """测试用例9: 教师更新学生成绩"""
        self.run_api_test(
            9, "教师更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 90}',
             '-b', self.cookie_file],
            "9_update_score.json", self.test_setup
        )
    
    def test_10_delete_score(self):
        """测试用例10: 教师删除学生成绩"""
        self.run_api_test(
            10, "教师删除学生成绩",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/scores/10', '-b', self.cookie_file],
            "10_delete_score.json", self.test_setup
        )
    
    def test_11_get_exams(self):
        """测试用例11: 教师获取考试列表"""
        self.run_api_test(
            11, "教师获取考试列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams', '-b', self.cookie_file],
            "11_get_exams.json", self.test_setup
        )
    
    def test_12_create_exam(self):
        """测试用例12: 教师创建考试"""
        self.run_api_test(
            12, "教师创建考试",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/teacher/exams',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Test Exam", "subject_id": 1, "exam_type_id": 1, "exam_date": "2025-09-01"}',
             '-b', self.cookie_file],
            "12_create_exam.json", self.test_setup
        )
    
    def test_13_get_specific_exam(self):
        """测试用例13: 教师获取特定考试"""
        self.run_api_test(
            13, "教师获取特定考试",
            ['curl', '-s', f'{self.base_url}/api/teacher/exams/1', '-b', self.cookie_file],
            "13_get_exam.json", self.test_setup
        )
    
    def test_14_update_exam(self):
        """测试用例14: 教师更新考试信息"""
        self.run_api_test(
            14, "教师更新考试信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/exams/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_name": "Updated Exam Name"}',
             '-b', self.cookie_file],
            "14_update_exam.json", self.test_setup
        )
    
    def test_15_delete_exam(self):
        """测试用例15: 教师删除考试"""
        self.run_api_test(
            15, "教师删除考试",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/teacher/exams/10', '-b', self.cookie_file],
            "15_delete_exam.json", self.test_setup
        )