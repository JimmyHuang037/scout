#!/usr/bin/env python3
"""
管理员科目管理API测试
"""

import pytest
import json
import time
import random


class TestAdminSubjectManagement:
    """管理员科目管理API测试类"""

    def test_get_subjects(self, admin_client):
        """测试获取科目列表"""
        response = admin_client.get('/api/admin/subjects')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'subjects' in data['data']
        assert 'pagination' in data['data']

    def test_create_subject(self, admin_client):
        """测试创建科目"""
        # 使用唯一的时间戳确保测试数据不重复
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        subject_data = {
            'subject_name': f'Test Subject {timestamp}_{random_num}'
        }
        response = admin_client.post('/api/admin/subjects',
                                     data=json.dumps(subject_data),
                                     content_type='application/json')
        # 根据实际实现，创建成功返回201状态码和消息
        assert response.status_code in [200, 201]

    def test_get_subject(self, admin_client):
        """测试获取单个科目信息"""
        # 获取一个已存在的科目 (使用ID为1的科目)
        response = admin_client.get("/api/admin/subjects/1")
        # 验证响应
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'subject_id' in data['data']
        assert data['data']['subject_id'] == 1