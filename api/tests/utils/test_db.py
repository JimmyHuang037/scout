#!/usr/bin/env python3
"""
数据库工具模块测试
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class TestDB:
    """数据库工具模块测试类"""

    def test_db_module_import(self):
        """测试数据库模块导入"""
        try:
            from utils.database_service import get_db, close_db, DatabaseService
            assert get_db is not None
            assert close_db is not None
            assert DatabaseService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import database_service module: {str(e)}")

    def test_database_service_class(self, app):
        """测试DatabaseService类"""
        with app.app_context():
            try:
                from utils.database_service import DatabaseService
                db_service = DatabaseService()
                assert db_service is not None
                # 测试数据库连接是否正常
                db_service.close()
            except Exception as e:
                pytest.fail(f"Failed to create DatabaseService instance: {str(e)}")