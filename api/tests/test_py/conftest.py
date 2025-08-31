#!/usr/bin/env python3
"""
测试配置文件
"""

import os
import sys
import pytest
from flask import Flask, session
import warnings

# 忽略flask_session的所有弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_session")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cachelib")

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.factory import create_app
from utils.database_service import DatabaseService


@pytest.fixture(scope="session")
def app():
    """创建应用实例"""
    # 使用testing配置
    app = create_app('testing')
    # 确保应用配置了SECRET_KEY
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture(scope="function")
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture(scope="function")
def db():
    """创建数据库服务实例"""
    db_service = DatabaseService()
    yield db_service
    db_service.close()


@pytest.fixture(scope="function")
def admin_client(client):
    """创建已登录的管理员测试客户端"""
    # 登录管理员账户
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
    # 登录教师账户 (ID: 3)
    response = client.post('/api/auth/login', json={
        'user_id': '3',
        'password': '123456'
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as teacher: {response.get_json()}")
    
    return client


@pytest.fixture(scope="function")
def student_client(client):
    """创建已登录的学生测试客户端"""
    # 登录学生账户 (ID: S0201)
    response = client.post('/api/auth/login', json={
        'user_id': 'S0201',
        'password': 'pass123'
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as student: {response.get_json()}")
    
    return client
