#!/usr/bin/env python3
"""
班级服务测试
"""

import pytest
from services.class_service import ClassService


class TestClassService:
    """班级服务测试类"""

    def test_get_all_classes(self, app):
        """测试获取所有班级"""
        with app.app_context():
            # 重新初始化服务以确保在正确的应用上下文中创建数据库连接
            class_service = ClassService.__new__(ClassService)
            class_service.__init__()
            result = class_service.get_all_classes(1, 10)
            assert isinstance(result, dict)
            assert 'classes' in result
            assert 'pagination' in result

    def test_get_class_by_id(self, app):
        """测试根据ID获取班级"""
        with app.app_context():
            # 重新初始化服务以确保在正确的应用上下文中创建数据库连接
            class_service = ClassService.__new__(ClassService)
            class_service.__init__()
            result = class_service.get_class_by_id(1)
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_create_class(self, app):
        """测试创建班级"""
        with app.app_context():
            # 重新初始化服务以确保在正确的应用上下文中创建数据库连接
            class_service = ClassService.__new__(ClassService)
            class_service.__init__()
            class_data = {
                'class_name': 'Test Class'
            }
            result = class_service.create_class(class_data)
            assert isinstance(result, dict)

    def test_update_class(self, app):
        """测试更新班级"""
        with app.app_context():
            # 重新初始化服务以确保在正确的应用上下文中创建数据库连接
            class_service = ClassService.__new__(ClassService)
            class_service.__init__()
            class_data = {
                'class_name': 'Updated Class'
            }
            result = class_service.update_class(1, class_data)
            assert isinstance(result, bool)

    def test_delete_class(self, app):
        """测试删除班级"""
        with app.app_context():
            # 重新初始化服务以确保在正确的应用上下文中创建数据库连接
            class_service = ClassService.__new__(ClassService)
            class_service.__init__()
            result = class_service.delete_class(1)
            assert isinstance(result, bool)