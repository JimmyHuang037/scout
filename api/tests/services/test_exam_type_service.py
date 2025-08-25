#!/usr/bin/env python3
"""
考试类型服务测试
"""

import pytest
from services.exam_type_service import ExamTypeService
from app.factory import create_app


class TestExamTypeService:
    """考试类型服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_exam_types(self, app):
        """测试获取考试类型列表"""
        with app.app_context():
            # 创建ExamTypeService实例
            exam_type_service = ExamTypeService()
            
            # 调用被测试方法 - 使用真实数据
            result = exam_type_service.get_all_exam_types(page=1, per_page=10)
            
            # 验证结果
            assert result is not None
            assert 'exam_types' in result
            assert 'pagination' in result
            assert result['pagination']['page'] == 1
            # 检查返回的考试类型列表是否为列表类型
            assert isinstance(result['exam_types'], list)