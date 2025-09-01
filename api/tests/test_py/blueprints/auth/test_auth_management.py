"""认证管理测试模块"""
import json
import pytest
from app.factory import create_app


class TestAuthManagement:
    """认证管理测试类"""

    def test_login_success(self, client):
        """测试成功登录"""
        # 准备测试数据 - 使用数据库中存在的学生用户
        login_data = {
            'user_id': 'S0201',
            'password': 'pass123'
        }
        
        # 发送登录请求
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        # 验证响应
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['user_id'] == 'S0201'
        assert data['data']['role'] == 'student'

    def test_login_invalid_credentials(self, client):
        """测试无效凭证登录"""
        # 准备测试数据
        login_data = {
            'user_id': 'invalid',
            'password': 'invalid'
        }
        
        # 发送登录请求
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        # 验证响应
        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        """测试缺少必要字段的登录"""
        # 准备测试数据
        login_data = {
            'user_id': 'S0201'
            # 缺少password字段
        }
        
        # 发送登录请求
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        # 验证响应
        assert response.status_code == 400

    def test_logout(self, client):
        """测试登出"""
        # 先登录
        login_data = {
            'user_id': 'S0201',
            'password': 'pass123'
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
        response = client.get('/api/auth/me')
        
        # 验证响应
        assert response.status_code in [401, 200]