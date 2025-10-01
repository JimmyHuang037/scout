import os
from .test_curl_base import CurlTestBase
from config import Config


class TestAuthEndpoints(CurlTestBase):
    """认证端点测试类 - 无需登录和会话的测试"""

    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.test_results_dir = Config.TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "auth_curl_commands.log")
        
        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
        }

    def test_01_auth_login(self):
        """测试用例1: 用户登录（无需登录和会话）"""
        self.run_api_test(
            1, "用户登录",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/login',
             '-H', 'Content-Type: application/json',
             '-d', '{"user_id": "S0101", "password": "pass123"}',
             '|', 'jq'],
            "auth_1_login.json", self.test_setup
        )

    def test_02_auth_get_current_user(self):
        """测试用例2: 获取当前用户信息（无需登录和会话）"""
        # 注意：此测试可能会返回未登录错误，因为没有会话
        self.run_api_test(
            2, "获取当前用户信息",
            ['curl', '-s', '-X', 'GET', f'{self.base_url}/api/auth/me',
             '|', 'jq'],
            "auth_2_get_current_user.json", self.test_setup,
            expect_error=True  # 期望返回错误，因为没有会话
        )

    def test_03_auth_logout(self):
        """测试用例3: 用户登出（无需登录和会话）"""
        # 注意：此测试可能会返回错误，因为没有活动会话
        self.run_api_test(
            3, "用户登出",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/logout',
             '|', 'jq'],
            "auth_3_logout.json", self.test_setup,
            expect_error=True  # 期望返回错误，因为没有会话
        )