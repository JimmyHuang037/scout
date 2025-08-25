#!/usr/bin/env python3
"""
测试配置文件，包含所有测试所需的fixtures
"""

import pytest
import sys
import os
import subprocess
import glob
import logging
from datetime import datetime

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 设置日志级别，完全屏蔽app和mysql.connector的日志
logging.getLogger('app').setLevel(logging.CRITICAL)
logging.getLogger('mysql.connector').setLevel(logging.CRITICAL)

from app.factory import create_app
from utils.db import DatabaseService


def pytest_configure(config):
    """pytest配置初始化，用于恢复测试数据库"""
    # 检查是否需要恢复数据库
    if not config.getoption("--no-db-restore", False):
        restore_test_database()


def pytest_unconfigure(config):
    """pytest结束时的清理工作，显示数据库表记录数"""
    if not config.getoption("--no-db-restore", False):
        show_database_stats()


def restore_test_database():
    """恢复测试数据库"""
    try:
        # 获取项目根目录
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        db_dir = os.path.join(project_root, 'db')
        backup_dir = os.path.join(db_dir, 'backup')
        
        # 确保backup目录存在
        if not os.path.exists(backup_dir):
            print(f"警告: 备份目录 {backup_dir} 不存在")
            return
            
        # 切换到db目录
        original_cwd = os.getcwd()
        os.chdir(db_dir)
        
        # 使用指定的备份文件
        backup_filename = 'school_management_backup_20250825_220152.sql'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # 检查指定的备份文件是否存在
        if not os.path.exists(backup_path):
            print(f"警告: 指定的备份文件 {backup_path} 不存在")
            # 查找最新的备份文件作为回退方案
            backup_files = glob.glob(os.path.join(backup_dir, 'school_management_backup_*.sql'))
            if not backup_files:
                print("警告: 没有找到备份文件")
                return
                
            # 按修改时间排序，获取最新的备份文件
            latest_backup = max(backup_files, key=os.path.getmtime)
            backup_filename = os.path.basename(latest_backup)
            print(f"使用最新的备份文件: {backup_filename}")
        
        # 调用restore_db.sh脚本恢复数据库
        result = subprocess.run(
            ['./restore_db.sh', backup_filename, 'school_management_test'],
            capture_output=True,
            text=True,
            input='y\n'  # 自动确认恢复操作
        )
        
        if result.returncode == 0:
            print("测试数据库恢复成功")
        else:
            print(f"数据库恢复失败: {result.stderr}")
            
    except Exception as e:
        print(f"恢复数据库时出错: {str(e)}")
    finally:
        # 恢复原来的工作目录
        if 'original_cwd' in locals():
            os.chdir(original_cwd)


def show_database_stats():
    """显示测试数据库中各表的记录数"""
    try:
        app = create_app('testing')
        with app.app_context():
            db_service = DatabaseService()
            
            # 查询各表记录数
            tables = ['Classes', 'Students', 'Teachers', 'Subjects', 'ExamTypes', 'Scores', 'TeacherClasses']
            stats = []
            
            for table in tables:
                try:
                    query = f"SELECT COUNT(*) as count FROM {table}"
                    result = db_service.execute_query(query, fetch_one=True)
                    count = result['count'] if result else 0
                    stats.append((table, count))
                except Exception:
                    stats.append((table, 'Error'))
            
            db_service.close()
            
            # 显示统计信息
            print("\n测试数据库表记录数统计:")
            print("=" * 30)
            for table, count in stats:
                print(f"{table:15} : {count}")
            print("=" * 30)
            
    except Exception as e:
        print(f"显示数据库统计信息时出错: {str(e)}")


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--no-db-restore",
        action="store_true",
        default=False,
        help="运行测试时不恢复数据库"
    )




@pytest.fixture
def app():
    """创建测试应用实例"""
    # 使用测试配置创建应用
    app = create_app('testing')
    
    # 创建应用上下文
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """创建已认证的测试客户端"""
    # 模拟登录
    login_data = {
        'user_id': 'admin',
        'password': 'admin123'
    }
    
    # 发送登录请求
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    # 返回客户端，此时应该已认证
    return client


# 删除旧文件
