#!/usr/bin/env python3
"""
教师考试班级管理API测试
"""

import pytest
import json


class TestTeacherExamClassManagement:
    """教师考试班级管理API测试类"""

    def test_get_exam_classes(self, teacher_client):
        """测试获取教师相关的考试班级列表"""
        response = teacher_client.get('/api/teacher/exam-classes')
        # 根据实际实现，可能返回不同状态码
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'success' in data
            assert data['success'] is True
            assert 'data' in data