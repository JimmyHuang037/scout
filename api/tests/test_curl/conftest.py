#!/usr/bin/env python3
"""
test_curl测试模块的配置文件
包含该模块共享的fixture和配置
"""

import pytest
import subprocess
import os
import sys
import time
import signal
from config.config import TestingConfig


@pytest.fixture(scope="session", autouse=True)
def start_server(request):
    """在测试会话开始前启动服务器"""
    # 设置环境变量
    env = os.environ.copy()
    env['FLASK_ENV'] = 'testing'
    
    # 获取日志目录和文件路径
    logs_dir = TestingConfig.LOGS_DIR
    api_log_file = os.path.join(os.path.dirname(TestingConfig.LOG_FILE_PATH), 'api.log')
    
    # 确保日志目录存在
    os.makedirs(logs_dir, exist_ok=True)
    
    # 清空API日志文件
    open(api_log_file, 'w').close()
    
    # 使用直接运行app.py的方式启动服务器，并将日志输出到api.log文件
    api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app.py'))
    
    # 打开API日志文件用于追加写入
    api_log_f = open(api_log_file, 'a')
    
    # 启动进程并将stdout和stderr重定向到api.log
    process = subprocess.Popen([
        sys.executable, api_path
    ], env=env, preexec_fn=os.setsid, stdout=api_log_f, stderr=api_log_f)
    
    # 等待服务器启动
    time.sleep(3)
    
    # 注册测试会话结束时的清理函数
    def cleanup():
        try:
            # 终止进程组
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.terminate()
            process.wait(timeout=5)
        except Exception as e:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except:
                pass
        finally:
            api_log_f.close()
    
    request.addfinalizer(cleanup)
    
    return process


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
