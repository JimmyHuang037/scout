#!/usr/bin/env python3
"""
数据库工具测试
"""


class TestDB:
    """数据库工具测试类"""

    def test_db_module_import(self):
        """测试数据库模块导入"""
        # 确保模块可以正确导入
        from utils.db import get_db, close_db, DatabaseService
        assert get_db is not None
        assert close_db is not None
        assert DatabaseService is not None

    def test_database_service_class(self):
        """测试DatabaseService类存在"""
        from utils.db import DatabaseService
        assert hasattr(DatabaseService, '__init__')
        assert hasattr(DatabaseService, 'execute_query')
        assert hasattr(DatabaseService, 'execute_update')
        assert hasattr(DatabaseService, 'get_count')
        assert hasattr(DatabaseService, 'close')
