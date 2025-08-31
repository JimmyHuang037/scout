#!/usr/bin/env python3
"""
test_py模块的pytest配置文件
包含测试夹具和配置
"""

import pytest
import os
import sys
import subprocess
import warnings

# 忽略flask_session的所有弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_session")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cachelib")

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.factory import create_app


def pytest_configure(config):
    """Pytest配置初始化，恢复测试数据库"""
    # 获取项目根目录
    project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
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


@pytest.fixture(scope='session')
def app():
    """创建Flask应用实例用于测试"""
    # 创建测试应用实例
    app = create_app('testing')
    
    # 确保会话目录存在
    session_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'logs_testing', 'flask_session')
    os.makedirs(session_dir, exist_ok=True)
    
    # 推送应用上下文
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def client(app):
    """创建测试客户端"""
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
        'password': 'admin'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login', json=login_data)
    
    # 检查登录是否成功
    if response.status_code == 200:
        # 返回已认证的客户端
        return client
    else:
        raise Exception(f"Failed to login as admin: {response.get_json()}")


@pytest.fixture
def teacher_client(client):
    """创建教师身份验证的客户端"""
    # 模拟教师登录 (user_id为1的教师密码是test123)
    login_data = {
        'user_id': '1',
        'password': 'test123'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login', json=login_data)
    
    # 检查登录是否成功
    if response.status_code == 200:
        # 返回已认证的客户端
        return client
    else:
        raise Exception(f"Failed to login as teacher: {response.get_json()}")


@pytest.fixture
def student_client(client):
    """创建学生身份验证的客户端"""
    # 模拟学生登录
    login_data = {
        'user_id': 'S0101',
        'password': 'pass123'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login', json=login_data)
    
    # 检查登录是否成功
    if response.status_code == 200:
        # 返回已认证的客户端
        return client
    else:
        raise Exception(f"Failed to login as student: {response.get_json()}")