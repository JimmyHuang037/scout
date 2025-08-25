#!/usr/bin/env python3
"""
考试类型服务测试
"""

import pytest
from unittest.mock import patch
from services.exam_type_service import ExamTypeService


class TestExamTypeService:
    """考试类型服务测试类"""

    @patch('services.exam_type_service.DatabaseService')
    def test_get_exam_types(self, mock_db_service):
        """测试获取考试类型列表"""
        # 创建ExamTypeService实例
        exam_type_service = ExamTypeService()
        
        # 验证DatabaseService被正确初始化
        mock_db_service.assert_called_once()
        
        # 验证方法存在
        assert hasattr(exam_type_service, 'get_all_exam_types')