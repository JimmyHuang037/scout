#!/usr/bin/env python3
"""
教师服务测试
"""

import pytest
from services.teacher_service import TeacherService
from app.factory import create_app


class TestTeacherService:
    """教师服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_teacher_by_id_success(self, app):
        """测试根据ID获取教师信息成功"""
        with app.app_context():
            # 创建服务实例
            service = TeacherService()
            
            # 调用被测试方法 - 使用真实数据
            result = service.get_teacher_by_id(1)
            
            # 验证结果
            # 先检查结果是否为None，如果不是再检查具体内容
            assert result is not None, "Expected teacher data but got None"
            if result is not None:
                assert 'teacher_id' in result
                assert result['teacher_id'] == 1
                assert 'teacher_name' in result
    
    def test_get_all_teachers_success(self, app):
        """测试获取所有教师成功"""
        with app.app_context():
            # 创建服务实例
            service = TeacherService()
            
            # 调用被测试方法 - 使用真实数据
            result = service.get_all_teachers(page=1, per_page=10)
            
            # 验证结果
            assert result is not None
            assert 'teachers' in result
            assert 'pagination' in result
            # 验证分页信息
            assert result['pagination']['page'] == 1
            assert result['pagination']['per_page'] == 10
