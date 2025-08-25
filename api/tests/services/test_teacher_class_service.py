#!/usr/bin/env python3
"""
教师班级服务测试
"""

import pytest
from unittest.mock import patch
from services.teacher_class_service import TeacherClassService


class TestTeacherClassService:
    """教师班级服务测试类"""

    @patch('services.teacher_class_service.DatabaseService')
    def test_get_teacher_classes(self, mock_db_service):
        """测试获取教师班级列表"""
        # 创建TeacherClassService实例
        teacher_class_service = TeacherClassService()
        
        # 验证DatabaseService被正确初始化
        mock_db_service.assert_called_once()
        
        # 验证方法存在
        assert hasattr(teacher_class_service, 'get_all_teacher_classes')