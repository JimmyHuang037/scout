#!/usr/bin/env python3
"""
认证工具测试
"""

import pytest
from flask import Flask, session
from utils.helpers import auth_required, role_required


class TestAuth:
    """认证装饰器测试类"""

    def test_require_auth_with_no_session(self, app):
        """测试没有会话时的身份验证检查"""
        with app.test_request_context():
            @auth_required
            def test_func():
                return "Success"
            
            response = test_func()
            # 检查返回的响应是否为401未授权
            # 响应是一个元组 (json_response, status_code)
            assert response[1] == 401

    def test_require_role_with_no_session(self, app):
        """测试没有会话时的角色检查"""
        with app.test_request_context():
            @role_required('admin')
            def test_func():
                return "Success"
            
            response = test_func()
            # 检查返回的响应是否为401未授权
            # 响应是一个元组 (json_response, status_code)
            assert response[1] == 401

    def test_require_role_with_wrong_role(self, app):
        """测试角色不匹配时的角色检查"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['user_name'] = 'test'
                sess['role'] = 'teacher'

            @role_required('admin')
            def test_func():
                return "Success"
            
            response = test_func()
            # 检查返回的响应是否为403禁止访问
            # 响应是一个元组 (json_response, status_code)
            assert response[1] == 403

    def test_require_role_with_correct_role(self, app):
        """测试角色匹配时的角色检查"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['user_name'] = 'test'
                sess['role'] = 'admin'

            @role_required('admin')
            def test_func():
                return "Success"
            
            result = test_func()
            # 检查函数是否成功执行
            assert result == "Success"