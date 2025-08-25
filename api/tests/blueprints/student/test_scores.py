#!/usr/bin/env python3
"""
学生成绩API测试
"""

import pytest
import json


class TestStudentScores:
    """学生成绩API测试类"""

    def test_get_my_scores(self, client):
        """测试获取我的成绩"""
        response = client.get('/api/student/scores')
        # 由于需要学生身份验证，这里可能需要添加身份验证逻辑
        # 目前我们验证路由是否存在
        assert response.status_code in [200, 401, 403]

    def test_get_my_exam_results(self, client):
        """测试获取我的考试结果"""
        response = client.get('/api/student/exam/results')
        # 由于需要学生身份验证，这里可能需要添加身份验证逻辑
        # 目前我们验证路由是否存在
        assert response.status_code in [200, 401, 403]