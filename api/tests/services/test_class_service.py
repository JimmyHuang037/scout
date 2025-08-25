#!/usr/bin/env python3
"""
班级服务测试
"""

import pytest
from unittest.mock import patch
from services.class_service import ClassService


class TestClassService:
    """班级服务测试类"""

    @patch('services.class_service.DatabaseService')
    def test_get_classes(self, mock_db_service):
        """测试获取班级列表"""
        # 创建ClassService实例
        class_service = ClassService()
        
        # 验证DatabaseService被正确初始化
        mock_db_service.assert_called_once()
        
        # 验证方法存在
        assert hasattr(class_service, 'get_all_classes')