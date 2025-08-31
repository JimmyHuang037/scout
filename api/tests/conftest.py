#!/usr/bin/env python3
"""
测试配置文件，包含所有测试所需的fixtures
"""

import pytest
import sys
import os
import subprocess
import warnings
import glob

# 忽略flask_session的所有弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_session")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cachelib")

# 将api目录添加到Python路径中
api_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(api_dir))

from app.factory import create_app


def pytest_configure(config):
    """Pytest配置初始化，恢复测试数据库"""
    # 获取项目根目录
    project_root = os.path.join(os.path.dirname(__file__), '..', '..')
    db_restore_script = os.path.join(project_root, 'db', 'restore_db.sh')
    
    # 使用最新的备份文件
    backup_filename = 'school_management_backup_20250831_103236.sql'
    
    # 检查恢复脚本是否存在
    if os.path.exists(db_restore_script):
        try:
            # 运行数据库恢复脚本，恢复测试数据库
            result = subprocess.run(
                [db_restore_script, backup_filename, 'school_management_test'],
                cwd=os.path.join(project_root, 'db'),
                input='y\n',  # 自动确认
                text=True,
                capture_output=True
            )
            
            if result.returncode == 0:
                print("测试数据库恢复成功")
            else:
                print(f"测试数据库恢复失败: {result.stderr}")
        except Exception as e:
            print(f"恢复测试数据库时出错: {e}")
    else:
        print(f"数据库恢复脚本不存在: {db_restore_script}")


@pytest.fixture
def app():
    """创建测试应用实例"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    # 处理Werkzeug版本兼容性问题
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建CLI运行器"""
    return app.test_cli_runner()


@pytest.fixture
def admin_client(client):
    """创建管理员身份验证的客户端"""
    # 模拟管理员登录
    login_data = {
        'user_id': 'admin',
        'password': 'admin'  # 修复管理员密码为正确值
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    # 返回客户端，此时应该已认证
    return client


@pytest.fixture
def teacher_client(client):
    """创建教师身份验证的客户端"""
    # 模拟教师登录 (使用教师ID 1，密码在数据库中存在)
    login_data = {
        'user_id': '1',
        'password': 'test123'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    # 返回客户端，此时应该已认证
    return client


@pytest.fixture
def student_client(client):
    """创建学生身份验证的客户端"""
    # 模拟学生登录 (使用学生ID S1001，密码在数据库中应该存在)
    login_data = {
        'user_id': 'S1001',
        'password': 'pass123'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    # 返回客户端，此时应该已认证
    return client


@pytest.fixture
def auth_client(client):
    """创建已认证的客户端"""
    # 这里应该实现登录逻辑
    # 由于当前系统可能使用session或token验证，暂时返回普通客户端
    return client


# 删除旧文件