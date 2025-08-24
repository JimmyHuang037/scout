#!/usr/bin/env python3
"""
Pytest配置文件
包含测试夹具和全局配置
"""

import pytest
import sys
import os

# 将api目录添加到Python路径中
api_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(api_dir))

from app.factory import create_app


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