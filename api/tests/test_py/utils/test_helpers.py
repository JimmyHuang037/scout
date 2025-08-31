#!/usr/bin/env python3
"""
工具函数测试
"""

import pytest
from utils.helpers import success_response, error_response
from app.factory import create_app


class TestHelpers:
    """工具函数测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_success_response(self, app):
        """测试创建成功响应"""
        data = {'message': '操作成功'}
        with app.app_context():
            response, status_code = success_response(data)
            assert status_code == 200
    
    def test_error_response(self, app):
        """测试创建错误响应"""
        with app.app_context():
            response, status_code = error_response("操作失败", 400)
            assert status_code == 400
    
    def test_success_response_with_empty_data(self, app):
        """测试创建空数据的成功响应"""
        with app.app_context():
            response, status_code = success_response()
            assert status_code == 200