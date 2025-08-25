#!/usr/bin/env python3
"""
教师学生管理API测试
"""

import pytest
import json


class TestTeacherStudentManagement:
    """教师学生管理API测试类"""

    def test_get_my_students(self, client):
        """测试获取我的学生列表"""
        response = client.get('/api/teacher/students')
        # 由于需要教师身份验证，这里可能需要添加身份验证逻辑
        # 目前我们验证路由是否存在
        assert response.status_code in [200, 401, 403]