#!/usr/bin/env python3
"""
管理员班级管理API测试
"""

import pytest
import json
import time
import random


class TestAdminClassManagement:
    """管理员班级管理API测试类"""
    
    @pytest.fixture()
    def created_class(self, admin_client):
        """创建一个测试班级供使用"""
        # 使用唯一的时间戳确保测试数据不重复
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        class_data = {
            'class_name': f'Test Class {timestamp}_{random_num}'
        }
        response = admin_client.post('/api/admin/classes',
                                     data=json.dumps(class_data),
                                     content_type='application/json')
        assert response.status_code in [200, 201]
        
        # 返回创建的班级数据
        return json.loads(response.data)['data']

    def test_get_classes(self, admin_client):
        """测试获取班级列表"""
        response = admin_client.get('/api/admin/classes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'classes' in data['data']
        assert 'pagination' in data['data']

    def test_create_class(self, admin_client):
        """测试创建班级"""
        # 已移至created_class fixture
        pass

    def test_get_class(self, admin_client, created_class):
        """测试获取单个班级信息"""
        # 获取已创建的班级
        class_id = created_class['class_id']
        response = admin_client.get(f"/api/admin/classes/{class_id}")
        # 验证响应
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'class_id' in data['data']
        assert data['data']['class_id'] == class_id

    def test_update_class(self, admin_client):
        """测试更新班级信息"""
        # 更新班级信息
        update_data = {
            'class_name': 'Updated Class Name'
        }
        response = admin_client.put("/api/admin/classes/1",
                                    data=json.dumps(update_data),
                                    content_type='application/json')
        # 根据实际实现，更新可能返回200状态码和消息
        assert response.status_code == 200

        # 验证更新结果
        response_data = json.loads(response.data)
        assert response_data['success'] is True

    def test_delete_class(self, admin_client, created_class):
        """测试删除班级"""
        # 获取已创建的班级ID
        class_id = created_class['class_id']
        
        # 删除班级
        response = admin_client.delete(f"/api/admin/classes/{class_id}")
        # 根据实际实现，可能返回不同状态码
        assert response.status_code in [200, 204]
        
        # 验证删除
        response = admin_client.get(f"/api/admin/classes/{class_id}")
        assert response.status_code == 404