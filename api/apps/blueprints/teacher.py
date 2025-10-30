from flask import Blueprint, request, current_app
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input
from apps.services.teacher_service import TeacherService
from apps.services.class_service import ClassService
from apps.services.student_service import StudentService
from apps.services.score_service import ScoreService

teacher_bp = Blueprint('teacher', __name__)


@handle_exceptions
def get_profile(teacher_id):
    teacher_service = TeacherService()
    profile_data = teacher_service.get_teacher_profile(teacher_id)
    if not profile_data:
        return error_response('教师未找到', 404)
        
    current_app.logger.info(f"Teacher {teacher_id} profile retrieved")
    return success_response(profile_data)


@handle_exceptions
def get_my_scores(teacher_id):
    score_service = ScoreService()
    scores_data = score_service.get_teacher_scores(teacher_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved scores")
    return success_response({'scores': scores_data})


@handle_exceptions
def update_my_score(teacher_id, score_id):
    data, error = validate_json_input(['score'])
    if error:
        return error
        
    score = data.get('score')
        
    score_service = ScoreService()
    score_data = {'score': score}
    result = score_service.update_score(score_id, score_data)
    if not result:
        return error_response('成绩未找到', 404)
        
    current_app.logger.info(f"Teacher {teacher_id} updated score {score_id}")
    return success_response(result)


@handle_exceptions
def get_classes(teacher_id):
    teacher_service = TeacherService()
    classes = teacher_service.get_teacher_classes(teacher_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved classes")
    return success_response(classes)


@handle_exceptions
def get_class_students(teacher_id, class_id):
    class_service = ClassService()
    students = class_service.get_students_by_class(class_id, teacher_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved students for class {class_id}")
    return success_response(students)


@handle_exceptions
def get_class(teacher_id, class_id):
    class_service = ClassService()
    class_data = class_service.get_class_by_id(class_id)
    if not class_data:
        return error_response('班级未找到', 404)
        
    current_app.logger.info(f"Teacher {teacher_id} retrieved class {class_id}")
    return success_response(class_data)


@handle_exceptions
def get_teacher_students(teacher_id):
    student_service = StudentService()
    students_data = student_service.get_teacher_students(teacher_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved students")
    return success_response({'students': students_data})


@handle_exceptions
def get_teacher_student(teacher_id, student_id):
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    if not student_data:
        return error_response('学生未找到', 404)
        
    current_app.logger.info(f"Teacher {teacher_id} retrieved student {student_id}")
    return success_response(student_data)


@handle_exceptions
def get_exam_scores(teacher_id, exam_id):
    score_service = ScoreService()
    scores_data = score_service.get_exam_scores(teacher_id, exam_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved scores for exam {exam_id}")
    return success_response({'scores': scores_data})


teacher_bp.add_url_rule('/profile/<string:teacher_id>', view_func=get_profile, methods=['GET'])
teacher_bp.add_url_rule('/scores/<string:teacher_id>', view_func=get_my_scores, methods=['GET'])
teacher_bp.add_url_rule('/scores/<string:teacher_id>/<int:score_id>', view_func=update_my_score, methods=['PUT'])
teacher_bp.add_url_rule('/classes/<string:teacher_id>', view_func=get_classes, methods=['GET'])
teacher_bp.add_url_rule('/classes/<string:teacher_id>/<string:class_id>/students', view_func=get_class_students, methods=['GET'])
teacher_bp.add_url_rule('/classes/<string:teacher_id>/<string:class_id>', view_func=get_class, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>', view_func=get_teacher_students, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>/<string:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>/class/<string:class_id>', view_func=get_class_students, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>/all_classes_students', view_func=get_teacher_students, methods=['GET'])
teacher_bp.add_url_rule('/exams/<string:teacher_id>/<int:exam_id>/scores', view_func=get_exam_scores, methods=['GET'])