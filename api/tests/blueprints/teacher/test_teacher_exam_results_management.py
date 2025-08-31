#!/usr/bin/env python3
"""
教师考试结果管理API测试
"""

import pytest
import json


class TestTeacherExamResultsManagement:
    """教师考试结果管理API测试类"""

    def test_get_exam_results(self, teacher_client):
        """测试获取考试结果"""
        response = teacher_client.get('/api/teacher/exam-results')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'exam_results' in data['data']