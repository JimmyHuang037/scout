#!/usr/bin/env python3
"""
教师服务测试
"""

import pytest
from services.teacher_service import TeacherService


class TestTeacherService:
    """教师服务测试类"""
    
    def test_get_teacher_by_id_success(self, mocker):
        """测试根据ID获取教师信息成功"""
        # 模拟数据库服务返回
        mock_result = {
            'teacher_id': 1,
            'teacher_name': '王老师',
            'subject_id': 1,
            'subject_name': '语文'
        }
        
        # 创建服务实例并模拟数据库方法
        service = TeacherService()
        mocker.patch.object(service.db_service, 'execute_query', return_value=mock_result)
        
        # 调用被测试方法
        result = service.get_teacher_by_id(1)
        
        # 验证结果
        assert result == mock_result
        service.db_service.execute_query.assert_called_once()
    
    def test_get_all_teachers_success(self, mocker):
        """测试获取所有教师成功"""
        # 模拟数据库服务返回
        mock_teachers = [
            {
                'teacher_id': 1,
                'teacher_name': '王老师',
                'subject_id': 1,
                'subject_name': '语文'
            },
            {
                'teacher_id': 2,
                'teacher_name': '李老师',
                'subject_id': 2,
                'subject_name': '数学'
            }
        ]
        
        mock_count = 2
        
        # 创建服务实例并模拟数据库方法
        service = TeacherService()
        mocker.patch.object(service.db_service, 'get_count', return_value=mock_count)
        mocker.patch.object(service.db_service, 'execute_query', return_value=mock_teachers)
        
        # 调用被测试方法
        result = service.get_all_teachers(page=1, per_page=10)
        
        # 验证结果
        assert result['teachers'] == mock_teachers
        assert result['pagination']['total'] == mock_count
        assert result['pagination']['page'] == 1
        service.db_service.get_count.assert_called_once()
        service.db_service.execute_query.assert_called_once()