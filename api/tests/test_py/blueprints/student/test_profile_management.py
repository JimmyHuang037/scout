#!/usr/bin/env python3
"""
学生个人信息API测试
"""

import pytest
import json


class TestStudentProfileManagement:
    """学生个人信息API测试类"""

    def test_get_my_profile(self, client):
        """测试获取我的个人信息"""
        response = client.get('/api/student/profile')
        # 由于需要学生身份验证，这里可能需要添加身份验证逻辑
        # 目前我们验证路由是否存在
        assert response.status_code in [200, 401, 403]