#!/usr/bin/env python3
"""
test_curl模块的pytest配置文件
"""

import pytest
import subprocess
import os
import sys
import time
import signal
import warnings

# 忽略flask_session的所有弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_session")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cachelib")

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


@pytest.fixture(scope="session")
def start_api_server():
    """启动API服务器用于测试"""
    # 切换到API目录
    api_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    original_dir = os.getcwd()
    os.chdir(api_dir)
    
    # 启动API服务器
    server_process = subprocess.Popen([
        'python', '-m', 'flask', '--app', 'app/factory:create_app', 
        'run', '--port', '5010'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    
    # 等待服务器启动
    time.sleep(3)
    
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