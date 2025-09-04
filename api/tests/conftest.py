#!/usr/bin/env python3
"""
测试配置文件 - 公共fixture和配置
"""

import os
import sys
import pytest
import subprocess
import glob
import time
import signal
from pathlib import Path
from urllib import request
from urllib.error import URLError
from datetime import datetime

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """在测试会话开始前自动设置测试环境"""
    # 设置FLASK_ENV为testing，确保使用测试配置
    os.environ['FLASK_ENV'] = 'testing'
    print("测试环境已设置: FLASK_ENV=testing")
    
    # 清空测试日志文件
    logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs_testing')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'app.log')
    
    # 清空日志文件
    with open(log_file, 'w') as f:
        f.write(f"=== TEST SESSION STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")


def restore_test_database():
    """恢复测试数据库"""
    try:
        # 获取项目根目录
        project_root = os.path.join(os.path.dirname(__file__), '..', '..')
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
        
        # 只在失败时打印详细错误信息
        if result.returncode == 0:
            print("数据库恢复成功完成!")
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
    print("正在恢复测试数据库...")
    success = restore_test_database()
    if success:
        print("测试数据库恢复成功!")
    else:
        print("测试数据库恢复失败!")
    return success