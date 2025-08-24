#!/usr/bin/env python3
"""
工具函数测试
"""

import pytest
from utils.helpers import create_success_response, create_error_response


class TestHelpers:
    """工具函数测试类"""
    
    def test_create_success_response(self):
        """测试创建成功响应"""
        data = {'message': '操作成功'}
        response = create_success_response(data)
        
        assert response['success'] is True
        assert response['data'] == data
        assert 'error' not in response
    
    def test_create_error_response(self):
        """测试创建错误响应"""
        error_message = '操作失败'
        response = create_error_response(error_message)
        
        assert response['success'] is False
        assert response['error'] == error_message
        assert 'data' not in response
    
    def test_create_success_response_with_empty_data(self):
        """测试创建空数据的成功响应"""
        response = create_success_response()
        
        assert response['success'] is True
        assert response['data'] is None
        assert 'error' not in response