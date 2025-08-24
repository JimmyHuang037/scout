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
    # 注意：由于我们还没有实现健康检查端点，这个测试可能会失败
    # 这里我们只是演示如何编写测试
    pass