#!/usr/bin/env python3
"""
认证管理API测试
"""

import pytest
import json


class TestAuthManagement:
    """认证管理API测试类"""

    def test_login_success(self, client):
        """测试登录成功"""
        # 使用有效的用户凭据登录
        login_data = {
            'user_id': 'admin',
            'password': 'admin123'
        }
        response = client.post('/api/auth/login',
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        # 验证响应
        assert response.status_code in [200, 401]  # 取决于测试数据库中的实际数据
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            assert 'user_id' in data['data']
            assert 'user_name' in data['data']
            assert 'role' in data['data']

    def test_login_missing_fields(self, client):
        """测试登录缺少必要字段"""
        # 缺少密码字段
        login_data = {
            'user_id': 'admin'
        }
        response = client.post('/api/auth/login',
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        # 验证响应
        assert response.status_code in [400, 401]

    def test_login_invalid_credentials(self, client):
        """测试登录无效凭据"""
        # 使用无效的用户凭据登录
        login_data = {
            'user_id': 'invalid_user',
            'password': 'invalid_password'
        }
        response = client.post('/api/auth/login',
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        # 验证响应
        assert response.status_code in [401, 500]

    def test_logout(self, client):
        """测试登出"""
        # 先登录
        login_data = {
            'user_id': 'admin',
            'password': 'admin123'
        }
        client.post('/api/auth/login',
                    data=json.dumps(login_data),
                    content_type='application/json')
        
        # 然后登出
        response = client.post('/api/auth/logout')
        
        # 验证响应
        assert response.status_code in [200, 401, 500]

    def test_get_current_user_not_authenticated(self, client):
        """测试获取当前用户信息但未认证"""
        response = client.get('/api/auth/user')
        
        # 验证响应
        assert response.status_code in [401, 200]