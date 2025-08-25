#!/usr/bin/env python3
"""
日志工具测试
"""

import pytest
import os
import tempfile
from utils.logger import setup_logger


class TestLogger:
    """日志工具测试类"""

    def test_setup_logger(self):
        """测试创建日志记录器"""
        # 创建临时日志文件
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as tmp_file:
            log_file = tmp_file.name

        try:
            # 测试创建日志记录器
            logger = setup_logger('test_logger', log_file)
            assert logger is not None
            assert logger.name == 'test_logger'
            assert len(logger.handlers) >= 2  # 文件处理器和控制台处理器

            # 测试日志记录
            logger.info('Test log message')
            logger.error('Test error message')

            # 验证日志文件存在
            assert os.path.exists(log_file)

        finally:
            # 清理临时文件
            if os.path.exists(log_file):
                os.unlink(log_file)

    def test_setup_logger_with_directory_creation(self):
        """测试创建日志记录器时自动创建目录"""
        # 创建临时目录和日志文件路径
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_dir = os.path.join(tmp_dir, 'logs')
            log_file = os.path.join(log_dir, 'test.log')

            # 确保目录不存在
            assert not os.path.exists(log_dir)

            # 测试创建日志记录器
            logger = setup_logger('test_logger', log_file)
            assert logger is not None

            # 验证目录已创建
            assert os.path.exists(log_dir)