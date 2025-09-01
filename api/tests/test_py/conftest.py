#!/usr/bin/env python3
"""
测试配置文件
"""

import os
import sys
import pytest
import warnings
import subprocess
import glob

# =============================================================================
# 初始化设置
# =============================================================================

# 忽略特定模块的弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_session")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cachelib")

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# =============================================================================
# 导入项目模块
# =============================================================================

from app.factory import create_app
from utils.database_service import DatabaseService


# =============================================================================
# 数据库恢复相关功能
# =============================================================================

def restore_test_database():
    """恢复测试数据库"""
    try:
        # 获取项目根目录
        project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        backup_dir = os.path.join(project_root, 'db', 'backup')
        
        # 查找最新的备份文件
        backup_files = glob.glob(os.path.join(backup_dir, '*.sql'))
        if not backup_files:
            print("警告: 没有找到备份文件")
            return False
            
        # 按修改时间排序，获取最新的备份文件
        latest_backup = max(backup_files, key=os.path.getmtime)
        print(f"使用备份文件: {latest_backup}")
        
        # 构建恢复命令，并启用自动模式
        restore_script = os.path.join(project_root, 'db', 'restore_db.sh')
        cmd = ['bash', restore_script, os.path.basename(latest_backup), 'school_management_test', '--auto']
        
        # 设置环境变量，使用config.py中的配置
        env = os.environ.copy()
        env['DB_USER'] = 'root'  # 在测试环境中使用root用户
        env['DB_PASS'] = 'Newuser1'  # 测试环境密码
        
        # 执行恢复命令
        result = subprocess.run(
            cmd,
            cwd=os.path.join(project_root, 'db'),
            text=True,
            capture_output=True,
            env=env
        )
        
        print(f"恢复命令: {' '.join(cmd)}")
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"标准输出: {result.stdout}")
        if result.stderr:
            print(f"错误输出: {result.stderr}")
            
        if result.returncode == 0:
            print(f"成功恢复测试数据库: {os.path.basename(latest_backup)}")
            return True
        else:
            print(f"恢复测试数据库失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"恢复测试数据库时出错: {str(e)}")
        return False


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """在测试会话开始前自动恢复测试数据库"""
    restore_test_database()


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
        'user_id': '3',
        'password': '123456'
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as teacher: {response.get_json()}")
    
    return client


@pytest.fixture(scope="function")
def student_client(client):
    """创建已登录的学生测试客户端"""
    response = client.post('/api/auth/login', json={
        'user_id': 'S0201',
        'password': 'pass123'
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to login as student: {response.get_json()}")
    
    return client