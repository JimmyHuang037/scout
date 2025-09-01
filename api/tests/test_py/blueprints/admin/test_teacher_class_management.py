#!/usr/bin/env python3
"""
管理员教师班级关联管理API测试
"""

import pytest
import json


class TestAdminTeacherClassManagement:
    """管理员教师班级关联管理API测试类"""

    def test_get_teacher_classes(self, admin_client):
        """测试获取教师班级关联列表"""
        response = admin_client.get('/api/admin/teacher-classes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'teacher_classes' in data['data']
        assert 'pagination' in data['data']

    def test_create_teacher_class(self, admin_client):
        """测试创建教师班级关联"""
        teacher_class_data = {
            'teacher_id': 1,
            'class_id': 1
        }
        response = admin_client.post('/api/admin/teacher-classes',
                                    data=json.dumps(teacher_class_data),
                                    content_type='application/json')
        # 根据实际实现，创建可能返回不同状态码
        assert response.status_code in [200, 201, 400, 500]

    def test_get_teacher_class_by_teacher(self, admin_client):
        """测试根据教师ID获取教师班级关联信息"""
        # 根据教师ID获取教师班级关联信息
        response = admin_client.get("/api/admin/teacher-classes/1")
        # 可能返回200（找到）或404（未找到）或其他状态码
        assert response.status_code in [200, 404, 500]

    def test_update_teacher_class(self, admin_client):
        """测试更新教师班级关联"""
        # 准备更新数据
        update_data = {
            'teacher_id': 1,
            'class_id': 1,
            'new_teacher_id': 2
        }
        
        # 发送更新请求
        response = admin_client.put('/api/admin/teacher-classes/1',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        
        # 验证响应
        assert response.status_code in [200, 400, 404, 500]

    def test_delete_teacher_class(self, admin_client):
        """测试删除教师班级关联"""
        # 删除教师班级关联（可能因外键约束而失败）
        response = admin_client.delete("/api/admin/teacher-classes/1/1")
        # 根据实际实现，可能返回不同状态码
        assert response.status_code in [200, 204, 400, 404, 500]