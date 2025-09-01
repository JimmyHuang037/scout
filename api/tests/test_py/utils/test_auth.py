"""认证工具测试模块"""
import pytest
from flask import Flask, session
from utils.helpers import role_required


class TestAuth:
    """认证工具测试类"""

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
        with app.test_request_context():
            with app.test_client() as client:
                # 模拟设置session
                with client.session_transaction() as sess:
                    sess['user_id'] = '1'
                    sess['user_name'] = 'test'
                    sess['role'] = 'teacher'

                @role_required('admin')
                def test_func():
                    return "Success"
                
                # 创建一个请求上下文来测试装饰器
                with app.test_request_context():
                    # 手动设置session
                    session['user_id'] = '1'
                    session['user_name'] = 'test'
                    session['role'] = 'teacher'
                    
                    response = test_func()
                    # 检查返回的响应是否为403禁止访问
                    # 响应是一个元组 (json_response, status_code)
                    assert response[1] == 403

    def test_require_role_with_correct_role(self, app):
        """测试角色匹配时的角色检查"""
        with app.test_request_context():
            @role_required('admin')
            def test_func():
                return "Success"
            
            # 创建一个请求上下文来测试装饰器
            with app.test_request_context():
                # 手动设置session
                session['user_id'] = '1'
                session['user_name'] = 'test'
                session['role'] = 'admin'
                
                result = test_func()
                # 检查函数是否成功执行
                assert result == "Success"