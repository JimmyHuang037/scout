#!/usr/bin/env python3
"""
学生成绩API测试
"""

import pytest
import json


class TestStudentScores:
    """学生成绩API测试类"""

    def test_get_my_scores_unauthorized(self, client):
        """测试未认证用户获取成绩"""
        response = client.get('/api/student/scores')
        # 未认证用户应该返回401或403错误
        assert response.status_code in [401, 403]

    def test_get_my_scores(self, student_client):
        """测试学生获取自己的成绩"""
        response = student_client.get('/api/student/scores')
        # 学生用户应该能够成功获取成绩
        assert response.status_code == 200
        
        # 验证返回的数据结构
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        
        # 验证返回的成绩是列表格式
        assert isinstance(data['data'], list)

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