#!/usr/bin/env python3
"""
测试配置文件
"""

import os
import sys
import pytest

# =============================================================================
# 初始化设置
# =============================================================================

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# =============================================================================
# 导入项目模块
# =============================================================================

from app.factory import create_app
from utils.database_service import DatabaseService


# =============================================================================
# Flask应用和测试客户端相关功能
# =============================================================================

@pytest.fixture(scope="session")
def app():
    """创建应用实例"""
    app = create_app('testing')
    return app


@pytest.fixture(scope="function")
def client(app):
    """创建未认证的测试客户端"""
    return app.test_client(use_cookies=True)


# =============================================================================
# 数据库服务相关功能
# =============================================================================

@pytest.fixture(scope="function")
def db():
    """创建数据库服务实例"""
    db_service = DatabaseService()
    yield db_service
    db_service.close()


# =============================================================================
# 认证客户端相关功能
# =============================================================================

@pytest.fixture(scope="function")
def admin_client(client):
    """创建已登录的管理员测试客户端"""
    response = client.post('/api/auth/login', json={
        'user_id': 'admin',
        'password': 'admin'
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as admin: {response.get_json()}")
    
    return client


@pytest.fixture(scope="function")
def teacher_client(client):
    """创建已登录的教师测试客户端"""
    response = client.post('/api/auth/login', json={
        'user_id': '1',  # 使用实际存在的教师ID
        'password': 'test123'  # 使用实际的密码
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as teacher: {response.get_json()}")
    
    return client


@pytest.fixture(scope="function")
def student_client(client):
    """创建已登录的学生测试客户端"""
    response = client.post('/api/auth/login', json={
        'user_id': 'S0201',  # 使用实际存在的学生ID
        'password': 'pass123'  # 使用实际的密码
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as student: {response.get_json()}")
    
    return client