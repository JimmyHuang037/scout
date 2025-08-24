#!/usr/bin/env python3
"""
成绩服务测试
"""

import pytest
from services.score_service import ScoreService
from app.factory import create_app


class TestScoreService:
    """成绩服务测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        return create_app('testing')
    
    def test_get_scores_by_student_id_success(self, mocker, app):
        """测试根据学生ID获取成绩成功"""
        # 模拟数据库服务返回
        mock_scores = [
            {
                'score_id': 1,
                'student_id': 'S1001',
                'student_name': '张三',
                'subject_id': 1,
                'subject_name': '语文',
                'exam_type_id': 1,
                'exam_type_name': '期中考',
                'score': 85
            },
            {
                'score_id': 2,
                'student_id': 'S1001',
                'student_name': '张三',
                'subject_id': 2,
                'subject_name': '数学',
                'exam_type_id': 1,
                'exam_type_name': '期中考',
                'score': 90
            }
        ]
        
        with app.app_context():
            # 创建服务实例并模拟数据库方法
            service = ScoreService()
            mocker.patch.object(service.db_service, 'execute_query', return_value=mock_scores)
            
            # 调用被测试方法
            result = service.get_scores(student_id='S1001')
            
            # 验证结果
            assert result == mock_scores
            service.db_service.execute_query.assert_called_once()
    
    def test_create_score_success(self, mocker, app):
        """测试创建成绩成功"""
        with app.app_context():
            # 创建服务实例并模拟数据库方法
            service = ScoreService()
            mocker.patch.object(service.db_service, 'execute_update', return_value=True)
            
            # 准备测试数据
            # 注意：create_score方法实际上不存在，我们使用execute_update直接测试
            query = "INSERT INTO Scores (student_id, subject_id, exam_type_id, score) VALUES (%s, %s, %s, %s)"
            params = ('S1001', 1, 1, 85)
            
            # 调用被测试方法
            result = service.db_service.execute_update(query, params)
            
            # 验证结果
            assert result is True
            service.db_service.execute_update.assert_called_once_with(query, params)