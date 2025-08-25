#!/usr/bin/env python3
"""
班级服务测试
"""

import pytest
from services.class_service import ClassService
from app.factory import create_app


class TestClassService:
    """班级服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_all_classes(self, app):
        """测试获取班级列表"""
        with app.app_context():
            # 创建ClassService实例
            class_service = ClassService()
            
            # 调用被测试方法 - 使用真实数据
            result = class_service.get_all_classes(page=1, per_page=10)
            
            # 验证结果
            assert result is not None
            assert 'classes' in result
            assert 'pagination' in result
            assert result['pagination']['page'] == 1
            # 检查返回的班级列表是否为列表类型
            assert isinstance(result['classes'], list)