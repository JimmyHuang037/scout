#!/usr/bin/env python3
"""
应用核心功能测试
"""

import pytest


def test_app_creation(app):
    """测试应用创建"""
    assert app is not None
    assert app.config['TESTING'] is True


def test_health_check(client):
    """测试健康检查端点"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'OK'
    assert 'message' in data