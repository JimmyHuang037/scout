#!/usr/bin/env python3
"""
教师学生管理API测试
"""

import pytest
import json


class TestTeacherStudentManagement:
    """教师学生管理API测试类"""

    def test_get_my_students(self, teacher_client):
        """测试获取当前教师所教班级的学生列表"""
        response = teacher_client.get('/api/teacher/students')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        assert 'students' in data['data']
        assert 'pagination' in data['data']

    def test_get_my_students_with_pagination(self, teacher_client):
        """测试带分页参数获取当前教师所教班级的学生列表"""
        response = teacher_client.get('/api/teacher/students?page=1&per_page=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        assert 'students' in data['data']
        assert 'pagination' in data['data']