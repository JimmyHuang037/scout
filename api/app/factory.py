#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用工厂模块

该模块包含创建Flask应用实例的工厂函数
"""

import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_session import Session
import traceback

# 确保logs目录存在
from config.config import config
from utils.database_service import DatabaseService


def _setup_logging(app):
    """设置应用日志配置"""
    # 确保日志目录存在
    if not os.path.exists(app.config['LOGS_DIR']):
        os.makedirs(app.config['LOGS_DIR'])
    
    # 创建文件处理器
    file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='utf-8')
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # 创建格式化器并将其添加到处理器
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # 将处理器添加到应用日志记录器
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # 记录应用启动日志
    app.logger.info('Application started')


def _setup_error_handlers(app):
    """设置应用错误处理器"""
    @app.errorhandler(Exception)
    def handle_exception(e):
        """全局异常处理器"""
        app.logger.error(f'Unhandled exception: {str(e)}')
        app.logger.error(traceback.format_exc())


def _initialize_extensions(app):
    """初始化Flask扩展"""
    CORS(app)
    Session(app)
    
    # 确保会话目录存在
    session_dir = app.config.get('SESSION_FILE_DIR')
    if session_dir and not os.path.exists(session_dir):
        os.makedirs(session_dir)


def create_app(config_name=None):
    """
    创建Flask应用实例
    
    Args:
        config_name (str): 配置名称，如果未提供则从环境变量FLASK_ENV获取，默认为'default'
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    # 如果未提供配置名称，则从配置模块获取
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    # 初始化应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 设置日志
    _setup_logging(app)
    
    # 初始化扩展
    _initialize_extensions(app)
    
    # 注册蓝图
    from blueprints.admin.exam_types import exam_type_bp
    from blueprints.admin.students import student_bp
    from blueprints.admin.subjects import subject_bp
    from blueprints.admin.teacher_classes import teacher_class_bp
    from blueprints.admin.teachers import teacher_bp
    from blueprints.auth import auth_bp
    from blueprints.student.exam import student_exam_bp
    from blueprints.student.profile import profile_bp
    from blueprints.student.scores import scores_bp
    from blueprints.teacher.exam import exam_bp
    from blueprints.teacher.exam import exam_class_bp
    from blueprints.teacher.exam import exam_results_bp
    from blueprints.teacher.exam import performance_bp
    from blueprints.teacher.scores import score_bp
    from blueprints.teacher.students import student_bp as teacher_student_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(exam_type_bp, url_prefix='/api/admin/exam-types')
    app.register_blueprint(student_bp, url_prefix='/api/admin/students')
    app.register_blueprint(subject_bp, url_prefix='/api/admin/subjects')
    app.register_blueprint(teacher_class_bp, url_prefix='/api/admin/teacher-classes')
    app.register_blueprint(teacher_bp, url_prefix='/api/admin/teachers')
    app.register_blueprint(student_exam_bp, url_prefix='/api/student/exam')
    app.register_blueprint(profile_bp, url_prefix='/api/student/profile')
    app.register_blueprint(scores_bp, url_prefix='/api/student/scores')
    app.register_blueprint(exam_bp, url_prefix='/api/teacher/exam')
    app.register_blueprint(exam_class_bp, url_prefix='/api/teacher/exam-class')
    app.register_blueprint(exam_results_bp, url_prefix='/api/teacher/exam-results')
    app.register_blueprint(performance_bp, url_prefix='/api/teacher/performance')
    app.register_blueprint(score_bp, url_prefix='/api/teacher/scores')
    app.register_blueprint(teacher_student_bp, url_prefix='/api/teacher/students')
    
    # 设置错误处理器
    _setup_error_handlers(app)
    
    return app