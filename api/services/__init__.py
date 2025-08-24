"""服务层模块初始化文件"""
from .database_service import DatabaseService, get_db, close_db
from .student_service import StudentService
from .teacher_service import TeacherService
from .score_service import ScoreService

__all__ = [
    'DatabaseService', 
    'get_db', 
    'close_db',
    'StudentService',
    'TeacherService',
    'ScoreService'
]