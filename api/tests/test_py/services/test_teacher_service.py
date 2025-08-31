#!/usr/bin/env python3
"""教师服务测试"""
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
            # 创建服务实例用于获取教师列表
            service = TeacherService()
            
            # 首先获取所有教师列表，然后使用其中的一个教师ID进行测试
            all_teachers = service.get_all_teachers(page=1, per_page=5)
            assert all_teachers is not None
            assert 'teachers' in all_teachers
            assert len(all_teachers['teachers']) > 0
            
            # 使用第一个教师的ID进行测试
            first_teacher = all_teachers['teachers'][0]
            teacher_id = first_teacher['teacher_id']
            
            # 为每个方法调用创建独立的服务实例，避免数据库连接问题
            service2 = TeacherService()
            # 调用被测试方法
            result = service2.get_teacher_by_id(teacher_id)
            
            # 验证结果
            assert result is not None, f"Expected teacher data but got None for teacher_id {teacher_id}"
            assert 'teacher_id' in result
            assert result['teacher_id'] == teacher_id
            assert 'teacher_name' in result
    def test_get_all_teachers_success(self, app):
        """测试获取所有教师成功"""
        with app.app_context():
            # 为 get_all_teachers 方法调用创建独立的服务实例
            service = TeacherService()
            
            # 调用被测试方法 - 使用真实数据
            result = service.get_all_teachers(page=1, per_page=10)
            
            # 打印调试信息
            print(f"获取所有教师的结果: {result}")
            
            # 验证结果
            assert result is not None
            assert 'teachers' in result
            assert 'pagination' in result
            # 验证分页信息
            assert result['pagination']['page'] == 1
            assert result['pagination']['per_page'] == 10