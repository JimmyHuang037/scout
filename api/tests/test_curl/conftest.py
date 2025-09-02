#!/usr/bin/env python3
"""
测试配置文件
"""

import os
import sys
import time
import signal
import subprocess
import pytest
from config.config import TestingConfig


@pytest.fixture(scope="session")
def start_api_server():
    """启动和关闭API服务器"""
    config = TestingConfig()
    base_url = f'http://localhost:{config.PORT}'
    env = os.environ.copy()
    env.update({'FLASK_APP': 'app/app.py', 'FLASK_ENV': 'testing'})
    
    process = subprocess.Popen([
        sys.executable, '-m', 'flask', 'run', '--host=127.0.0.1', f'--port={config.PORT}'
    ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    
    import requests
    start_time = time.time()
    
    while time.time() - start_time < 30:
        try:
            if requests.get(f'{base_url}/api/auth/health', timeout=1).status_code == 200:
                yield base_url
                break
        except requests.RequestException:
            pass
        time.sleep(0.5)
    else:
        _terminate_server(process)
        pytest.fail("服务器启动超时")
    
    _terminate_server(process)


def _terminate_server(process):
    """终止服务器进程"""
    if process and process.poll() is None:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=5)
        except (subprocess.TimeoutExpired, ProcessLookupError):
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            process.wait()


@pytest.fixture(scope="session")
def test_results_dir():
    """创建测试结果目录"""
    # 使用配置文件中的CURL_TEST_DIR配置，并添加时间戳
    config = TestingConfig()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    result_dir = os.path.join(config.CURL_TEST_DIR, timestamp)
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


@pytest.fixture(scope="session")
def curl_commands_file(test_results_dir):
    """创建curl命令记录文件"""
    commands_file = os.path.join(test_results_dir, 'curl_commands.txt')
    # 清空或创建文件
    with open(commands_file, 'w') as f:
        f.write("Curl测试命令记录\n")
        f.write("=" * 50 + "\n")
    
    return commands_file


@pytest.fixture(scope="session")
def cookie_file():
    """提供cookie文件路径"""
    return '/tmp/test_cookie.txt'


@pytest.fixture(scope="class")
def test_environment(start_api_server, test_results_dir, curl_commands_file, cookie_file):
    """提供完整的测试环境配置"""
    environment = {
        'base_url': start_api_server,
        'test_results_dir': test_results_dir,
        'curl_commands_file': curl_commands_file,
        'cookie_file': cookie_file
    }
    return environment