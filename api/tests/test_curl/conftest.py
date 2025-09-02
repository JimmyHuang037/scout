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
    base_url = f'http://127.0.0.1:{config.PORT}'  # 使用127.0.0.1而不是localhost
    env = os.environ.copy()
    env.update({'FLASK_ENV': 'testing'})
    
    # 使用直接运行app.py的方式启动服务器
    api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app.py'))
    process = subprocess.Popen([
        sys.executable, api_path
    ], env=env, preexec_fn=os.setsid)
    
    # 打印进程信息用于调试
    print(f"启动API服务器进程 PID: {process.pid}")
    
    import requests
    start_time = time.time()
    
    # 等待服务器启动，最多等待60秒
    while time.time() - start_time < 60:
        try:
            response = requests.get(f'{base_url}/api/health', timeout=5)
            if response.status_code == 200:
                print(f"API服务器启动成功，URL: {base_url}")
                yield base_url
                break
        except requests.RequestException as e:
            print(f"等待服务器启动... 错误: {e}")
            time.sleep(1)
    else:
        # 服务器启动超时，终止进程并输出错误信息
        print("服务器启动超时，正在终止进程...")
        _terminate_server(process)
        # 输出进程的stdout和stderr用于调试
        try:
            stdout, stderr = process.communicate(timeout=5)
            print(f"服务器stdout: {stdout.decode()}")
            print(f"服务器stderr: {stderr.decode()}")
        except subprocess.TimeoutExpired:
            print("无法获取服务器输出")
        pytest.fail("服务器启动超时")
    
    # 测试完成后终止服务器
    print("测试完成，正在关闭服务器...")
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