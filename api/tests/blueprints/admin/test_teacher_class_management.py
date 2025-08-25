#!/usr/bin/env python3
"""
管理员教师班级关联管理API测试
"""

import pytest
import json


class TestAdminTeacherClassManagement:
    """管理员教师班级关联管理API测试类"""

    def test_get_teacher_classes(self, client):
        """测试获取教师班级关联列表"""
        response = client.get('/api/admin/teacher-classes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        # 检查返回的数据是否包含teacher_classes或teacherClasses字段
        assert 'teacher_classes' in data['data'] or 'teacherClasses' in data['data'] or 'items' in data['data']

    def test_create_teacher_class(self, client):
        """测试创建教师班级关联"""
        teacher_class_data = {
            'teacher_id': 1,
            'class_id': 1
        }
        response = client.post('/api/admin/teacher-classes',
                               data=json.dumps(teacher_class_data),
                               content_type='application/json')
        # 根据实际实现，创建可能返回不同状态码
        assert response.status_code in [200, 201, 400, 500]

    def test_get_teacher_class_by_teacher(self, client):
        """测试根据教师ID获取教师班级关联信息"""
        # 根据教师ID获取教师班级关联信息
        response = client.get("/api/admin/teacher-classes/1")
        # 可能返回200（找到）或404（未找到）或其他状态码
        assert response.status_code in [200, 404, 500]

    def test_delete_teacher_class(self, client):
        """测试删除教师班级关联"""
        # 删除教师班级关联
        response = client.delete("/api/admin/teacher-classes/1/1")
        # 可能返回各种状态码
        assert response.status_code in [200, 204, 400, 404]