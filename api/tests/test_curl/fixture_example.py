#!/usr/bin/env python3
"""
Fixture 使用示例
演示 curl_commands_file 这类 fixture 是如何工作的
"""

import pytest


# 这是一个模拟的 fixture，类似于我们在 conftest.py 中定义的 curl_commands_file
@pytest.fixture
def example_fixture():
    """示例 fixture，返回一个字符串"""
    print("执行 example_fixture")
    return "这是来自 fixture 的值"


# 测试函数通过参数声明使用 fixture
def test_with_fixture(example_fixture):
    """
    当我们运行这个测试时，会发生以下步骤：
    1. pytest 检测到测试函数需要 example_fixture 参数
    2. pytest 查找名为 example_fixture 的 fixture
    3. pytest 执行 example_fixture fixture 函数
    4. pytest 将 fixture 的返回值传递给测试函数
    5. 测试函数中 example_fixture 参数的值就是 fixture 的返回值
    """
    print(f"在测试函数中使用 fixture 的值: {example_fixture}")
    assert example_fixture == "这是来自 fixture 的值"


# 在实际的 test_curl 测试中，使用方式完全一样
def test_curl_commands_file_usage(start_api_server, test_results_dir, curl_commands_file):
    """
    这是在 test_curl 测试中的实际使用方式：
    1. start_api_server - 启动 Flask API 服务器的 fixture
    2. test_results_dir - 测试结果目录路径的 fixture
    3. curl_commands_file - curl 命令记录文件路径的 fixture
    
    当 pytest 运行这个测试时：
    1. pytest 发现测试需要这三个 fixture
    2. pytest 依次执行这三个 fixture 函数
    3. pytest 将每个 fixture 的返回值传递给测试函数
    4. 在测试函数中，curl_commands_file 变量就包含了 fixture 返回的文件路径
    """
    # curl_commands_file 变量现在包含了 curl 命令记录文件的路径
    print(f"Curl 命令将被记录到: {curl_commands_file}")
    
    # 我们可以使用这个路径来做各种操作，比如：
    with open(curl_commands_file, 'a', encoding='utf-8') as f:
        f.write("\n# 这是一个测试命令记录\n")
        f.write("curl -s http://localhost:5010/api/auth/health\n")
    
    # 验证文件确实存在
    import os
    assert os.path.exists(curl_commands_file)