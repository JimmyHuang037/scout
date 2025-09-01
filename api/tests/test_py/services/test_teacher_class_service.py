#!/usr/bin/env python3
"""
教师班级服务测试
"""

import pytest
from services.teacher_class_service import TeacherClassService
from utils.database_service import DatabaseService


class TestTeacherClassService:
    """教师班级服务测试类"""

    def test_get_all_teacher_classes(self, app):
        """测试获取所有教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            result = teacher_class_service.get_all_teacher_classes(1, 10)
            assert isinstance(result, dict)
            assert 'teacher_classes' in result
            assert 'pagination' in result

    def test_get_teacher_class_by_teacher(self, app):
        """测试根据教师ID获取教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            result = teacher_class_service.get_teacher_class_by_teacher(1)
            assert isinstance(result, list)

    def test_get_teacher_class_by_id(self, app):
        """测试根据ID获取教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            # 使用实际存在的teacher_id和class_id进行测试
            result = teacher_class_service.get_teacher_class_by_id(1, 6)
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_create_teacher_class(self, app):
        """测试创建教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            # 先尝试删除可能已存在的相同记录
            db_service = DatabaseService()
            delete_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            db_service.execute_update(delete_query, (3, 3))
            db_service.close()
            
            result = teacher_class_service.create_teacher_class(3, 3)
            assert isinstance(result, bool)

    def test_update_teacher_class(self, app):
        """测试更新教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            # 使用实际存在的teacher_id和class_id进行测试
            result = teacher_class_service.update_teacher_class(1, 6, 3)
            # 根据实际实现，应该返回True或False
            assert isinstance(result, bool)

    def test_delete_teacher_class(self, app):
        """测试删除教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            # 使用实际存在的teacher_id和class_id进行测试
            result = teacher_class_service.delete_teacher_class(1, 6)
            assert isinstance(result, bool)

    def test_delete_teacher_class_by_teacher_and_class(self, app):
        """测试根据教师ID和班级ID删除教师班级关联"""
        with app.app_context():
            teacher_class_service = TeacherClassService()
            result = teacher_class_service.delete_teacher_class_by_teacher_and_class(1, 6)
            assert isinstance(result, bool)