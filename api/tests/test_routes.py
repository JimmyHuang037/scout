#!/usr/bin/env python3
"""
路由测试
"""

import pytest


def test_index_route(client):
    """测试首页路由"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'version' in data