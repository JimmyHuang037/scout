#!/usr/bin/env python3
"""
学生考试管理API测试
"""

import pytest
import json


class TestStudentExamManagement:
    """学生考试管理API测试类"""

    def test_get_my_exam_results_unauthorized(self, client):
        """测试未认证用户获取考试结果"""
        response = client.get('/api/student/exam/results')
        # 未认证用户应该返回401或403错误
        assert response.status_code in [401, 403]

    def test_get_my_exam_results(self, student_client):
        """测试学生获取自己的考试结果"""
        response = student_client.get('/api/student/exam/results')
        # 学生用户应该能够成功获取考试结果
        assert response.status_code == 200
        
        # 验证返回的数据结构
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        
        # 验证返回的结果是列表格式
        assert isinstance(data['data'], list)

    def test_get_my_exam_results_with_invalid_auth(self, client):
        """测试使用无效认证获取考试结果"""
        # 先用无效凭据登录
        login_data = {
            'user_id': 'invalid_user',
            'password': 'invalid_password'
        }
        client.post('/api/auth/login',
                   data=json.dumps(login_data),
                   content_type='application/json')
        
        # 尝试获取考试结果
        response = client.get('/api/student/exam/results')
        # 应该返回认证错误
        assert response.status_code in [401, 403]