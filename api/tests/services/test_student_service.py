#!/usr/bin/env python3
"""
学生服务测试
"""

import pytest
from services.student_service import StudentService
from app.factory import create_app


class TestStudentService:
    """学生服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_student_by_id_success(self, app):
        """测试根据ID获取学生信息成功"""
        with app.app_context():
            # 创建服务实例
            service = StudentService()
            
            # 调用被测试方法 - 使用真实数据
            result = service.get_student_by_id('S1001')
            
            # 验证结果
            assert result is not None
            assert 'student_id' in result
            assert result['student_id'] == 'S1001'
            assert 'student_name' in result
    
    def test_get_student_by_id_not_found(self, app):
        """测试根据ID获取学生信息但未找到"""
        with app.app_context():
            # 创建服务实例
            service = StudentService()
            
            # 调用被测试方法 - 使用不存在的学生ID
            result = service.get_student_by_id('NONEXISTENT')
            
            # 验证结果
            assert result is None
    
    def test_get_all_students_success(self, app):
        """测试获取所有学生成功"""
        with app.app_context():
            # 创建服务实例
            service = StudentService()
            
            # 调用被测试方法
            result = service.get_all_students(page=1, per_page=10)
            
            # 验证结果
            assert 'students' in result
            assert 'pagination' in result
            assert result['pagination']['page'] == 1
