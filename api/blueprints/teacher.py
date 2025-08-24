from flask import Blueprintcd /home/jimmy/repo/scout/api && python app.pycd /home/jimmy/repo/scout/api && python app.py
from api.blueprints.teacher.profile import get_profile
from api.blueprints.teacher.students import get_my_students
from api.blueprints.teacher.scores import get_scores
from api.blueprints.teacher.score_create import create_score
from api.blueprints.teacher.score_update import update_score
from api.blueprints.teacher.exam_class import get_exam_class
from api.blueprints.teacher.exam_results import get_exam_results
from api.blueprints.teacher.performance import get_performance

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

@teacher_bp.route('/')
def teacher_index():
    """教师API根路径"""
    return {
        'message': 'Teacher API',
        'version': '1.0.0'
    }

# 教师专用API端点
@teacher_bp.route('/profile', methods=['GET'])
def teacher_profile():
    return get_profile()

@teacher_bp.route('/students', methods=['GET'])
def teacher_students():
    return get_my_students()

@teacher_bp.route('/scores', methods=['GET'])
def teacher_scores():
    return get_scores()

@teacher_bp.route('/scores', methods=['POST'])
def teacher_scores_create():
    return create_score()

@teacher_bp.route('/scores/<int:score_id>', methods=['PUT'])
def teacher_scores_update(score_id):
    return update_score(score_id)

@teacher_bp.route('/exam/class', methods=['GET'])
def teacher_exam_class():
    return get_exam_class()

@teacher_bp.route('/exam/results', methods=['GET'])
def teacher_exam_results():
    return get_exam_results()

@teacher_bp.route('/performance', methods=['GET'])
def teacher_performance():
    return get_performance()