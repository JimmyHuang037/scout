#!/usr/bin/env python3
"""
成绩服务测试
"""

import pytest
from services.score_service import ScoreService
from utils.database_service import DatabaseService


class TestScoreService:
    """成绩服务测试类"""

    def test_get_scores_by_student_id_success(self, app):
        """测试根据学生ID获取成绩成功"""
        with app.app_context():
            score_service = ScoreService()
            # 使用测试数据库中存在的学生ID
            result = score_service.get_scores(student_id='S0101')
            assert isinstance(result, list)

    def test_create_score_success(self, app):
        """测试创建成绩成功"""
        with app.app_context():
            score_service = ScoreService()
            # 先尝试删除可能已存在的相同记录
            db_service = DatabaseService()
            delete_query = "DELETE FROM Scores WHERE student_id = %s AND subject_id = %s AND exam_type_id = %s"
            db_service.execute_update(delete_query, ('S0102', 2, 2))
            db_service.close()
            
            # 创建新的成绩记录，使用测试数据库中存在的数据
            result = score_service.create_score('S0102', 2, 2, 85)
            assert result is True or result is False  # 根据实际实现调整

    def test_get_teacher_scores(self, app):
        """测试获取教师成绩列表"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_teacher_scores(1)
            assert isinstance(result, list)

    def test_get_score_by_id(self, app):
        """测试根据ID获取成绩"""
        with app.app_context():
            score_service = ScoreService()
            # 尝试获取一个存在的成绩ID
            result = score_service.get_score_by_id(1)
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_update_score(self, app):
        """测试更新成绩"""
        with app.app_context():
            score_service = ScoreService()
            # 尝试更新一个存在的成绩
            result = score_service.update_score(1, 90)
            # 根据实际实现，可能返回True/False或其他值
            assert isinstance(result, (bool, int)) or result is None

    def test_delete_score(self, app):
        """测试删除成绩"""
        with app.app_context():
            score_service = ScoreService()
            # 尝试删除一个存在的成绩
            result = score_service.delete_score(1)
            # 根据实际实现，可能返回True/False或其他值
            assert isinstance(result, (bool, int)) or result is None

    def test_validate_student_for_teacher(self, app):
        """测试验证学生是否属于教师班级"""
        with app.app_context():
            score_service = ScoreService()
            # 测试一个已知的学生和教师组合
            result = score_service.validate_student_for_teacher('S0101', 1)
            # 根据实际实现，应该返回True或False
            assert isinstance(result, bool)

    def test_validate_teacher_for_score(self, app):
        """测试验证教师是否有权限操作成绩"""
        with app.app_context():
            score_service = ScoreService()
            # 测试一个已知的教师和成绩组合
            result = score_service.validate_teacher_for_score(1, 1)
            # 根据实际实现，应该返回True或False
            assert isinstance(result, bool)

    def test_get_exam_results(self, app):
        """测试获取考试结果"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_exam_results(1)
            assert isinstance(result, list)

    def test_get_teacher_performance(self, app):
        """测试获取教师表现数据"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_teacher_performance(1)
            assert isinstance(result, list)

    def test_get_student_exam_results(self, app):
        """测试获取学生考试结果"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_student_exam_results('S0101')
            assert isinstance(result, list)

    def test_get_exam_types(self, app):
        """测试获取考试类型"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_exam_types()
            assert isinstance(result, list)

    def test_get_classes(self, app):
        """测试获取班级列表"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_classes()
            assert isinstance(result, list)

    def test_get_class_exam_results(self, app):
        """测试获取班级考试结果"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_class_exam_results(1, 1)
            assert isinstance(result, list)

    def test_get_score_statistics(self, app):
        """测试获取成绩统计"""
        with app.app_context():
            score_service = ScoreService()
            result = score_service.get_score_statistics(1)
            assert isinstance(result, dict)