#!/usr/bin/env python3
"""
学生个人信息API测试
"""

import pytest
import json


class TestStudentProfileManagement:
    """学生个人信息API测试类"""

    def test_get_my_profile_unauthorized(self, client):
        """测试未认证用户获取个人信息"""
        response = client.get('/api/student/profile')
        # 未认证用户应该返回401或403错误
        assert response.status_code in [401, 403]

    def test_get_my_profile(self, student_client):
        """测试学生获取自己的个人信息"""
        response = student_client.get('/api/student/profile')
        # 学生用户应该能够成功获取个人信息
        assert response.status_code == 200
        
        # 验证返回的数据结构
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        
        # 验证返回的数据包含必要字段
        profile_data = data['data']
        assert 'student_id' in profile_data
        assert 'student_name' in profile_data
        assert 'class_name' in profile_data

    def test_get_my_profile_with_invalid_auth(self, client):
        """测试使用无效认证获取个人信息"""
        # 先用无效凭据登录
        login_data = {
            'user_id': 'invalid_user',
            'password': 'invalid_password'
        }
        client.post('/api/auth/login',
                   data=json.dumps(login_data),
                   content_type='application/json')
        
        # 尝试获取个人信息
        response = client.get('/api/student/profile')
        # 应该返回认证错误
        assert response.status_code in [401, 403]