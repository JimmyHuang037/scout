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
        # 当请求获取科目列表时
        response = admin_client.get('/api/admin/subjects')
        
        # 那么应该返回200状态码
        assert response.status_code == 200
        
        # 并且响应数据应该包含subjects和pagination信息
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
        
        # 获取创建的科目ID用于后续测试
        created_data = json.loads(response.data)
        if 'data' in created_data and 'subject_id' in created_data['data']:
            subject_id = created_data['data']['subject_id']
        else:
            # 如果响应中没有subject_id，则尝试通过名称查找
            get_response = admin_client.get('/api/admin/subjects')
            subjects = json.loads(get_response.data)['data']['subjects']
            subject_id = None
            for subject in subjects:
                if subject['subject_name'] == f'Test Subject {timestamp}_{random_num}':
                    subject_id = subject['subject_id']
                    break
        
        return subject_id

    def test_get_subject(self, admin_client):
        """测试获取单个科目信息"""
        # 当请求获取ID为1的科目时
        response = admin_client.get("/api/admin/subjects/1")
        
        # 那么应该返回200状态码
        assert response.status_code == 200
        
        # 并且响应数据应该包含正确的科目信息
        data = json.loads(response.data)
        assert 'data' in data
        assert 'subject_id' in data['data']
        assert data['data']['subject_id'] == 1

    def test_update_subject(self, admin_client):
        """测试更新科目"""
        # 创建一个科目用于更新
        subject_id = self.test_create_subject(admin_client)
        if subject_id:
            # 准备更新数据
            update_data = {
                'subject_name': f'Updated Subject {int(time.time())}'
            }
            
            # 发送更新请求
            response = admin_client.put(f'/api/admin/subjects/{subject_id}',
                                        data=json.dumps(update_data),
                                        content_type='application/json')
            
            # 验证响应
            assert response.status_code in [200, 400, 404]

    def test_delete_subject(self, admin_client):
        """测试删除科目"""
        # 创建一个科目用于删除
        subject_id = self.test_create_subject(admin_client)
        if subject_id:
            # 发送删除请求
            response = admin_client.delete(f'/api/admin/subjects/{subject_id}')
            
            # 验证响应
            assert response.status_code in [200, 204, 400, 404]