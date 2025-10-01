import os
import pytest
from .test_curl_base import CurlTestBase
from config import Config


@pytest.mark.order("first")
class TestAuthEndpoints(CurlTestBase):
    """认证端点测试类 - 会话保持测试"""

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
        
        # 定义会话文件路径
        cls.session_file = os.path.join(cls.test_results_dir, "auth_session.cookie")

    def test_01_auth_login_with_session(self):
        """测试用例1: 用户登录并保存会话"""
        self.run_session_api_test(
            1, "用户登录并保存会话",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/login',
             '-H', 'Content-Type: application/json',
             '-d', '{"user_id": "S0101", "password": "pass123"}',
             '-c', self.session_file],
            "auth_1_login_with_session.json",
            self.test_setup
        )
        
    def test_02_auth_get_current_user_with_session(self):
        """测试用例2: 使用会话获取当前用户信息"""
        self.run_session_api_test(
            2, "使用会话获取当前用户信息",
            ['curl', '-s', '-X', 'GET', f'{self.base_url}/api/auth/me',
             '-b', self.session_file],
            "auth_2_get_current_user_with_session.json",
            self.test_setup
        )
        
    def test_03_auth_logout_with_session(self):
        """测试用例3: 使用会话登出"""
        self.run_session_api_test(
            3, "使用会话登出",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/auth/logout',
             '-b', self.session_file],
            "auth_3_logout_with_session.json",
            self.test_setup
        )