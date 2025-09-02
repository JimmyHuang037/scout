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

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


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


@pytest.fixture(scope="session")
def start_api_server():
    """启动API服务器用于测试"""
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'testing'
    
    # 获取项目路径
    api_dir = os.path.join(os.path.dirname(__file__), '..')
    db_dir = os.path.join(api_dir, 'db')
    original_dir = os.getcwd()
    
    # 切换到API目录
    os.chdir(api_dir)
    
    # 启动API服务器
    server_process = subprocess.Popen([
        'python', '-m', 'flask', '--app', 'app/factory:create_app', 
        'run', '--port', '5010'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    
    # 等待服务器启动并验证
    server_ready = False
    for _ in range(10):  # 最多等待10秒
        try:
            response = request.urlopen('http://localhost:5010/api/auth/health', timeout=1)
            if response.getcode() == 200:
                server_ready = True
                break
        except URLError:
            time.sleep(1)
    
    if not server_ready:
        # 终止进程
        try:
            os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        except:
            pass
        raise Exception("API服务器启动失败")
    
    print("API服务器启动成功!")
    
    yield server_process
    
    # 关闭服务器
    try:
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        server_process.wait(timeout=5)
    except:
        try:
            os.killpg(os.getpgid(server_process.pid), signal.SIGKILL)
        except:
            pass
    
    # 恢复原始目录
    os.chdir(original_dir)