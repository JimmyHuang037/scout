#!/usr/bin/env python3
"""
测试配置文件，包含所有测试所需的fixtures
"""

import pytest
import sys
import os

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.factory import create_app
from utils.db import DatabaseService


@pytest.fixture
def app():
    """创建测试应用实例"""
    # 使用测试配置创建应用
    app = create_app('testing')
    
    # 创建应用上下文
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """创建已认证的测试客户端"""
    # 模拟登录
    login_data = {
        'user_id': 'admin',
        'password': 'admin123'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    # 返回客户端，此时应该已认证
    return client


# 删除旧文件
