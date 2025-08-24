#!/usr/bin/env python3
"""
Pytest配置文件
包含测试夹具和全局配置
"""

import pytest
import sys
import os
import subprocess

# 将api目录添加到Python路径中
api_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(api_dir))

from app.factory import create_app


def pytest_configure(config):
    """Pytest配置初始化，恢复测试数据库"""
    # 获取项目根目录
    project_root = os.path.join(os.path.dirname(__file__), '..', '..')
    db_restore_script = os.path.join(project_root, 'db', 'restore_db.sh')
    backup_file = 'school_management_backup_20250823_233411.sql'
    
    # 检查恢复脚本是否存在
    if os.path.exists(db_restore_script):
        try:
            # 运行数据库恢复脚本，恢复测试数据库
            result = subprocess.run(
                [db_restore_script, backup_file, 'school_management_test'],
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