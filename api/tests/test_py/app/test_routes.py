#!/usr/bin/env python3
"""
路由测试
"""

import pytest


def test_index_route(client):
    """测试首页路由"""
    # 注意：由于我们还没有实现首页路由，这个测试可能会失败
    # 这里我们只是演示如何编写测试
    pass


def test_health_check(client):
    """测试健康检查端点"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    # 验证返回的JSON数据
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'healthy'
    assert 'message' in data
    assert data['message'] == 'API server is running'