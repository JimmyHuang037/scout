#!/usr/bin/env python3
"""
test_curl模块的pytest配置文件
"""

import pytest
import subprocess
import os
import time
import signal
import sys


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
        'run', '--port', '5000'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 等待服务器启动
    time.sleep(3)
    
    yield server_process
    
    # 关闭服务器
    server_process.terminate()
    server_process.wait()
    
    # 恢复原始目录
    os.chdir(original_dir)