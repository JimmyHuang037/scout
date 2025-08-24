#!/usr/bin/env python3
"""
成绩服务测试
"""

import pytest
from services.score_service import ScoreService


class TestScoreService:
    """成绩服务测试类"""
    
    def test_get_scores_by_student_id_success(self, mocker):
        """测试根据学生ID获取成绩成功"""
        # 模拟数据库服务返回
        mock_scores = [
            {
                'score_id': 1,
                'student_id': 'S1001',
                'subject_name': '语文',
                'exam_type_name': '期中考',
                'score': 85
            },
            {
                'score_id': 2,
                'student_id': 'S1001',
                'subject_name': '数学',
                'exam_type_name': '期中考',
                'score': 90
            }
        ]
        
        # 创建服务实例并模拟数据库方法
        service = ScoreService()
        mocker.patch.object(service.db_service, 'execute_query', return_value=mock_scores)
        
        # 调用被测试方法
        result = service.get_scores_by_student_id('S1001')
        
        # 验证结果
        assert result == mock_scores
        service.db_service.execute_query.assert_called_once()
    
    def test_create_score_success(self, mocker):
        """测试创建成绩成功"""
        # 创建服务实例并模拟数据库方法
        service = ScoreService()
        mocker.patch.object(service.db_service, 'execute_update', return_value=True)
        
        # 准备测试数据
        score_data = {
            'student_id': 'S1001',
            'subject_id': 1,
            'exam_type_id': 1,
            'score': 85
        }
        
        # 调用被测试方法
        result = service.create_score(score_data)
        
        # 验证结果
        assert result is True
        service.db_service.execute_update.assert_called_once()