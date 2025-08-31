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
        'password': 'admin'  # 修复管理员密码为正确值
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    # 返回客户端，此时应该已认证
    return client


@pytest.fixture(scope='function')
def teacher_client(app):
    """创建已认证的教师测试客户端"""
    with app.test_client() as client:
        # 模拟教师登录
        with client.session_transaction() as session:
            session['user_id'] = '8'  # 使用字符串类型的教师ID
            session['user_name'] = 'Test Teacher'  # 添加教师姓名
            session['role'] = 'teacher'
        yield client


@pytest.fixture(scope='function')
def student_client(app):
    """创建已认证的学生测试客户端"""
    with app.test_client() as client:
        # 模拟学生登录
        with client.session_transaction() as session:
            session['user_id'] = 'S0101'  # 使用有效的学生ID
            session['user_name'] = 'Test Student'  # 添加学生姓名
            session['role'] = 'student'
        yield client


@pytest.fixture(scope='function')
def auth_client(app):
    """创建已认证的测试客户端（管理员）"""
    with app.test_client() as client:
        # 模拟管理员登录
        with client.session_transaction() as session:
            session['user_id'] = 'admin'
            session['user_name'] = 'Administrator'  # 添加管理员姓名
            session['role'] = 'admin'
        yield client