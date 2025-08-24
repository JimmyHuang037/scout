from flask import Blueprint, jsonify, request
from ..database import get_db

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 教师专用API端点
@teacher_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取当前教师个人信息"""
    # 在实际应用中，这里会从JWT token或session中获取当前教师ID
    # 这里暂时返回示例数据
    return jsonify({
        'success': True,
        'data': {
            'teacher_id': 1,
            'teacher_name': '示例教师',
            'subject_id': 1,
            'subject_name': '语文'
        }
    })


@teacher_bp.route('/students', methods=['GET'])
def get_my_students():
    """获取当前教师所教班级的学生信息"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # 获取该教师所教班级的学生总数
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Students s
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """, (current_teacher_id,))
        
        total = cursor.fetchone()['count']
        
        # 获取该教师所教班级的学生列表
        cursor.execute("""
            SELECT s.student_id, s.student_name, s.class_id, c.class_name
            FROM Students s
            JOIN Classes c ON s.class_id = c.class_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
            ORDER BY s.class_id, s.student_id
            LIMIT %s OFFSET %s
        """, (current_teacher_id, per_page, offset))
        
        students = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': students,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/scores', methods=['GET'])
def get_scores():
    """获取所教班级的成绩"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        student_id = request.args.get('student_id')
        subject_id = request.args.get('subject_id')
        exam_type_id = request.args.get('exam_type_id')
        
        # 构建查询
        query = """
            SELECT sc.score_id, sc.student_id, s.student_name, 
                   sc.subject_id, sub.subject_name,
                   sc.exam_type_id, et.exam_type_name, sc.score
            FROM Scores sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN Subjects sub ON sc.subject_id = sub.subject_id
            JOIN ExamTypes et ON sc.exam_type_id = et.type_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        params = [current_teacher_id]
        
        # 添加筛选条件
        if student_id:
            query += " AND sc.student_id = %s"
            params.append(student_id)
            
        if subject_id:
            query += " AND sc.subject_id = %s"
            params.append(subject_id)
            
        if exam_type_id:
            query += " AND sc.exam_type_id = %s"
            params.append(exam_type_id)
            
        query += " ORDER BY sc.student_id, sc.subject_id, sc.exam_type_id"
        
        cursor.execute(query, params)
        scores = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': scores
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/scores', methods=['POST'])
def create_score():
    """录入成绩"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        exam_type_id = data.get('exam_type_id')
        score = data.get('score')
        
        if not all([student_id, subject_id, exam_type_id, score is not None]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: student_id, subject_id, exam_type_id, score'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # 检查学生是否在教师所教班级中
        current_teacher_id = 1  # 示例教师ID
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Students s
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE s.student_id = %s AND tc.teacher_id = %s
        """, (student_id, current_teacher_id))
        
        if cursor.fetchone()['count'] == 0:
            return jsonify({
                'success': False,
                'error': 'Student not in your class'
            }), 403
        
        # 插入成绩
        cursor.execute("""
            INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
            VALUES (%s, %s, %s, %s)
        """, (student_id, subject_id, exam_type_id, score))
        
        db.commit()
        
        # 获取插入的成绩ID
        score_id = cursor.lastrowid
        
        return jsonify({
            'success': True,
            'message': 'Score created successfully',
            'data': {
                'score_id': score_id,
                'student_id': student_id,
                'subject_id': subject_id,
                'exam_type_id': exam_type_id,
                'score': score
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/scores/<int:score_id>', methods=['PUT'])
def update_score(score_id):
    """更新成绩"""
    try:
        data = request.get_json()
        score = data.get('score')
        
        if score is None:
            return jsonify({
                'success': False,
                'error': 'Score is required'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # 检查成绩是否存在且属于教师所教班级
        current_teacher_id = 1  # 示例教师ID
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Scores sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE sc.score_id = %s AND tc.teacher_id = %s
        """, (score_id, current_teacher_id))
        
        if cursor.fetchone()['count'] == 0:
            return jsonify({
                'success': False,
                'error': 'Score not found or not in your class'
            }), 404
        
        # 更新成绩
        cursor.execute("""
            UPDATE Scores 
            SET score = %s 
            WHERE score_id = %s
        """, (score, score_id))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Score updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/exam-class', methods=['GET'])
def get_exam_class():
    """获取班级成绩等级分布"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 构建查询
        query = """
            SELECT ec.*
            FROM exam_class ec
            JOIN Classes c ON ec.class_name = c.class_name
            JOIN TeacherClasses tc ON c.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        params = [current_teacher_id]
        
        # 添加筛选条件
        if exam_type_id:
            query += " AND ec.exam_type = %s"
            params.append(exam_type_id)
            
        if class_id:
            query += " AND c.class_id = %s"
            params.append(class_id)
            
        query += " ORDER BY ec.class_name"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/exam-results', methods=['GET'])
def get_exam_results():
    """获取考试结果"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 构建查询
        query = """
            SELECT er.*
            FROM exam_results er
            JOIN Students s ON er.student_name = s.student_name
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        params = [current_teacher_id]
        
        # 添加筛选条件
        if exam_type_id:
            query += " AND er.exam_type = %s"
            params.append(exam_type_id)
            
        if class_id:
            query += " AND s.class_id = %s"
            params.append(class_id)
            
        query += " ORDER BY er.ranking"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/performance', methods=['GET'])
def get_performance():
    """获取教学表现统计"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        
        # 构建查询
        query = """
            SELECT tp.*
            FROM teacher_performance tp
            JOIN Teachers t ON tp.teacher_name = t.teacher_name
            WHERE t.teacher_id = %s
        """
        params = [current_teacher_id]
        
        # 添加筛选条件
        if exam_type_id:
            query += " AND tp.exam_type = %s"
            params.append(exam_type_id)
            
        query += " ORDER BY tp.ranking"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500