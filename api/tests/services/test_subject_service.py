#!/usr/bin/env python3
"""
科目服务测试
"""

import pytest
from unittest.mock import patch
from services.subject_service import SubjectService


class TestSubjectService:
    """科目服务测试类"""

    @patch('services.subject_service.DatabaseService')
    def test_get_subjects(self, mock_db_service):
        """测试获取科目列表"""
        # 创建SubjectService实例
        subject_service = SubjectService()
        
        # 验证DatabaseService被正确初始化
        mock_db_service.assert_called_once()
        
        # 验证方法存在
        assert hasattr(subject_service, 'get_all_subjects')