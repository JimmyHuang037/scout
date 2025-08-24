#!/usr/bin/env python3
"""
学生服务测试
"""

import pytest
from services.student_service import StudentService


class TestStudentService:
    """学生服务测试类"""
    
    def test_get_student_by_id_success(self, mocker):
        """测试根据ID获取学生信息成功"""
        # 模拟数据库服务返回
        mock_result = {
            'student_id': 'S1001',
            'student_name': '张三',
            'class_id': 1,
            'class_name': '高三1班'
        }
        
        # 创建服务实例并模拟数据库方法
        service = StudentService()
        mocker.patch.object(service.db_service, 'execute_query', return_value=mock_result)
        
        # 调用被测试方法
        result = service.get_student_by_id('S1001')
        
        # 验证结果
        assert result == mock_result
        service.db_service.execute_query.assert_called_once()
    
    def test_get_student_by_id_not_found(self, mocker):
        """测试根据ID获取学生信息但未找到"""
        # 模拟数据库服务返回None
        service = StudentService()
        mocker.patch.object(service.db_service, 'execute_query', return_value=None)
        
        # 调用被测试方法
        result = service.get_student_by_id('S9999')
        
        # 验证结果
        assert result is None
        service.db_service.execute_query.assert_called_once()
    
    def test_get_all_students_success(self, mocker):
        """测试获取所有学生成功"""
        # 模拟数据库服务返回
        mock_students = [
            {
                'student_id': 'S1001',
                'student_name': '张三',
                'class_id': 1,
                'class_name': '高三1班'
            },
            {
                'student_id': 'S1002',
                'student_name': '李四',
                'class_id': 1,
                'class_name': '高三1班'
            }
        ]
        
        mock_count = 2
        
        # 创建服务实例并模拟数据库方法
        service = StudentService()
        mocker.patch.object(service.db_service, 'get_count', return_value=mock_count)
        mocker.patch.object(service.db_service, 'execute_query', return_value=mock_students)
        
        # 调用被测试方法
        result = service.get_all_students(page=1, per_page=10)
        
        # 验证结果
        assert result['students'] == mock_students
        assert result['pagination']['total'] == mock_count
        assert result['pagination']['page'] == 1
        service.db_service.get_count.assert_called_once()
        service.db_service.execute_query.assert_called_once()