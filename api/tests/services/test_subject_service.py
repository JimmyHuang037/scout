#!/usr/bin/env python3
"""
科目服务测试
"""

import pytest
from services.subject_service import SubjectService
from app.factory import create_app


class TestSubjectService:
    """科目服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_all_subjects(self, app):
        """测试获取科目列表"""
        with app.app_context():
            # 创建SubjectService实例
            subject_service = SubjectService()
            
            # 调用被测试方法 - 使用真实数据
            result = subject_service.get_all_subjects(page=1, per_page=10)
            
            # 验证结果
            assert result is not None
            assert 'subjects' in result
            assert 'pagination' in result
            assert result['pagination']['page'] == 1
            # 检查返回的科目列表是否为列表类型
            assert isinstance(result['subjects'], list)