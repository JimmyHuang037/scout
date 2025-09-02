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
from urllib import request
from urllib.error import URLError

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


@pytest.fixture(scope="session")
def start_api_server():
    """启动API服务器用于测试"""
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'testing'
    
    # 获取项目路径
    api_dir = os.path.join(os.path.dirname(__file__), '..', '..')
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