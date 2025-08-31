#!/usr/bin/env python3
"""
教师班级服务测试
"""

import pytest
from services.teacher_class_service import TeacherClassService
from app.factory import create_app


class TestTeacherClassService:
    """教师班级服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_all_teacher_classes(self, app):
        """测试获取教师班级列表"""
        with app.app_context():
            # 创建TeacherClassService实例
            teacher_class_service = TeacherClassService()
            
            # 调用被测试方法 - 使用真实数据
            result = teacher_class_service.get_all_teacher_classes(page=1, per_page=10)
            
            # 验证结果
            assert result is not None
            assert 'teacher_classes' in result
            assert 'pagination' in result
            assert result['pagination']['page'] == 1
            # 检查返回的教师班级列表是否为列表类型
            assert isinstance(result['teacher_classes'], list)