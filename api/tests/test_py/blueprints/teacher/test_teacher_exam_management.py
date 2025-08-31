#!/usr/bin/env python3
"""
教师考试管理API测试
"""

import pytest
import json


class TestTeacherExamManagement:
    """教师考试管理API测试类"""

    def test_get_exams(self, teacher_client):
        """测试获取教师相关的考试列表"""
        response = teacher_client.get('/api/teacher/exams')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'exams' in data['data']
        assert 'pagination' in data['data']

    def test_create_exam(self, teacher_client):
        """测试创建考试"""
        exam_data = {
            'name': 'Test Exam',
            'subject_id': 1,
            'class_ids': [1],
            'exam_type_id': 1,
            'date': '2025-09-01',
            'total_score': 100
        }
        response = teacher_client.post('/api/teacher/exams',
                                      data=json.dumps(exam_data),
                                      content_type='application/json')
        assert response.status_code == 200

    def test_get_exam(self, teacher_client):
        """测试获取考试详情"""
        # 使用ID为1的考试进行测试
        response = teacher_client.get('/api/teacher/exams/1')
        assert response.status_code == 200

    def test_update_exam(self, teacher_client):
        """测试更新考试"""
        exam_data = {
            'name': 'Updated Test Exam',
            'subject_id': 1,
            'class_ids': [1],
            'exam_type_id': 1,
            'date': '2025-09-02',
            'total_score': 100
        }
        response = teacher_client.put('/api/teacher/exams/1',
                                     data=json.dumps(exam_data),
                                     content_type='application/json')
        assert response.status_code == 200

    def test_delete_exam(self, teacher_client):
        """测试删除考试"""
        response = teacher_client.delete('/api/teacher/exams/1')
        assert response.status_code == 200