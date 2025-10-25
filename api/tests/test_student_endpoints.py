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
            ['curl', '-s', f'{self.base_url}/api/student/profile/S0101', '|', 'jq'],
            "student_1_get_profile.json", self.test_setup
        )

    def test_02_get_student_scores(self):
        """测试用例2: 获取学生成绩（无需登录和会话）"""
        self.run_api_test(
            2, "获取学生成绩",
            ['curl', '-s', f'{self.base_url}/api/student/scores/S0101', '|', 'jq'],
            "student_2_get_scores.json", self.test_setup
        )

    def test_03_get_student_exam_results(self):
        """测试用例3: 获取学生考试结果（无需登录和会话）"""
        self.run_api_test(
            3, "获取学生考试结果",
            ['curl', '-s', f'{self.base_url}/api/student/exam_results/S0101', '|', 'jq'],
            "student_3_get_exam_results.json", self.test_setup
        )
        
    def test_04_get_student_exam_results_not_found(self):
        """测试用例4: 获取不存在学生ID的考试结果，应返回404错误"""
        self.run_api_test(
            4, "获取不存在学生ID的考试结果",
            ['curl', '-s', f'{self.base_url}/api/student/exam_results/S999', '|', 'jq'],
            "student_4_get_exam_results_not_found.json", self.test_setup,
            expect_error=True
        )

    def test_05_get_student_scores_chinese(self):
        """测试用例5: 获取学生语文成绩（无需登录和会话）"""
        self.run_api_test(
            5, "获取学生成绩",
            ['curl', '-s', f'{self.base_url}/api/student/scores/chinese/S0101', '|', 'jq'],
            "student_5_get_scores_chinese.json", self.test_setup
        )

