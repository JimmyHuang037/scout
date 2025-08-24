from flask import Blueprint, jsonify, current_app
from api.utils.auth import decode_jwt_token  # 假设JWT token解码函数
from api.models import Teacher  # 假设Teacher模型

teacher_profile_bp = Blueprint('teacher_profile', __name__, url_prefix='/api/teacher')

@teacher_profile_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取当前教师个人信息"""
    try:
        # 从请求头中获取token
        token = current_app.config['JWT_TOKEN']
        teacher_id = decode_jwt_token(token)  # 解码token得到教师ID

        # 查询数据库获取教师信息
        teacher = Teacher.query.get(teacher_id)
        if teacher is None:
            return jsonify({
                'success': False,
                'message': '教师信息不存在'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'teacher_id': teacher.id,
                'teacher_name': teacher.name,
                'subject_id': teacher.subject_id,
                'subject_name': teacher.subject.name  # 假设Subject模型有name字段
            }
        })
    except Exception as e:
        # 异常处理
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500