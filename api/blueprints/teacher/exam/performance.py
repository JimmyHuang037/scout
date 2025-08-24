from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

teacher_performance_bp = Blueprint('teacher_performance', __name__, url_prefix='/api/teacher')

def fetch_teacher_performance(db, teacher_id, exam_type_id=None):
    """
    从数据库中获取教师表现统计信息
    
    :param db: 数据库连接对象
    :param teacher_id: 教师ID
    :param exam_type_id: 可选的考试类型ID，用于筛选数据
    :return: 查询结果列表
    """
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT tp.*
        FROM teacher_performance tp
        JOIN Teachers t ON tp.teacher_name = t.teacher_name
        WHERE t.teacher_id = %s
    """
    params = [teacher_id]

    if exam_type_id:
        query += " AND tp.exam_type = %s"
        params.append(exam_type_id)

    query += " ORDER BY tp.ranking"

    cursor.execute(query, params)
    return cursor.fetchall()

@teacher_performance_bp.route('/performance', methods=['GET'])
def get_performance():
    """获取教学表现统计"""
    try:
        db = get_db()
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        
        # 获取教师表现数据
        results = fetch_teacher_performance(db, current_teacher_id, exam_type_id)
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500