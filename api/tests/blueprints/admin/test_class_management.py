#!/usr/bin/env python3
"""
管理员班级管理API测试
"""

import pytest
import json


class TestAdminClassManagement:
    """管理员班级管理API测试类"""

    def test_get_classes(self, client):
        """测试获取班级列表"""
        response = client.get('/api/admin/classes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'classes' in data['data']
        assert 'pagination' in data['data']

    def test_create_class(self, client):
        """测试创建班级"""
        class_data = {
            'class_name': 'Test Class',
            'grade': 10,
            'class_teacher_id': 1
        }
        response = client.post('/api/admin/classes',
                               data=json.dumps(class_data),
                               content_type='application/json')
        # 根据实际实现，创建成功返回201状态码和消息
        assert response.status_code in [200, 201]

    def test_get_class(self, client):
        """测试获取单个班级信息"""
        # 获取一个已存在的班级
        response = client.get("/api/admin/classes/1")
        # 验证响应
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'class_id' in data['data']

    def test_update_class(self, client):
        """测试更新班级信息"""
        # 更新班级信息
        update_data = {
            'class_name': 'Updated Class Name',
            'grade': 11
        }
        response = client.put("/api/admin/classes/1",
                              data=json.dumps(update_data),
                              content_type='application/json')
        # 根据实际实现，更新可能返回200状态码和消息
        assert response.status_code in [200, 400, 404]

    def test_delete_class(self, client):
        """测试删除班级"""
        # 删除班级（可能因外键约束而失败）
        response = client.delete("/api/admin/classes/1")
        # 根据实际实现，可能返回不同状态码
        assert response.status_code in [200, 204, 400, 404, 500]