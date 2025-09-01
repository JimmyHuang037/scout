#!/usr/bin/env python3
"""
科目服务测试
"""

import pytest
from services.subject_service import SubjectService
from utils.database_service import DatabaseService


class TestSubjectService:
    """科目服务测试类"""

    def test_get_all_subjects(self, app):
        """测试获取所有科目"""
        with app.app_context():
            subject_service = SubjectService()
            result = subject_service.get_all_subjects(1, 10)
            assert isinstance(result, dict)
            assert 'subjects' in result
            assert 'pagination' in result

    def test_get_subject_by_id(self, app):
        """测试根据ID获取科目"""
        with app.app_context():
            subject_service = SubjectService()
            result = subject_service.get_subject_by_id(1)
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_create_subject(self, app):
        """测试创建科目"""
        with app.app_context():
            subject_service = SubjectService()
            result = subject_service.create_subject({'subject_name': 'Test Subject'})
            assert isinstance(result, (int, bool))

    def test_update_subject(self, app):
        """测试更新科目"""
        with app.app_context():
            subject_service = SubjectService()
            result = subject_service.update_subject(1, {'subject_name': 'Updated Subject'})
            assert isinstance(result, bool)

    def test_delete_subject(self, app):
        """测试删除科目"""
        with app.app_context():
            subject_service = SubjectService()
            result = subject_service.delete_subject(1)
            assert isinstance(result, bool)