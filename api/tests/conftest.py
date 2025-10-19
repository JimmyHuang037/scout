import glob
import os
import subprocess
import pytest
import shutil

"""
test_curl测试模块的配置文件
只保留数据库恢复功能
"""


@pytest.fixture(scope="session", autouse=True)
def cleanup_logs():
    """在测试会话开始前清理日志文件"""
    # 清空 app.log 文件内容
    app_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", "app.log")
    app_log_path = os.path.abspath(app_log_path)
    
    # 确保 app.log 文件存在，如果不存在则创建
    if os.path.exists(app_log_path):
        open(app_log_path, 'w').close()  # 清空文件内容
    else:
        # 确保 logs 目录存在
        os.makedirs(os.path.dirname(app_log_path), exist_ok=True)
        # 创建空的 app.log 文件
        open(app_log_path, 'w').close()
    
    # 删除 logs/test 目录下的所有文件
    test_logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", "test")
    test_logs_dir = os.path.abspath(test_logs_dir)
    
    if os.path.exists(test_logs_dir):
        # 删除目录中的所有文件和子目录
        for filename in os.listdir(test_logs_dir):
            file_path = os.path.join(test_logs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        # 如果目录不存在，创建它
        os.makedirs(test_logs_dir, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def restore_database():
    """在测试会话开始前恢复数据库"""
    # 等待 cleanup_logs fixture 执行完成后再执行数据库恢复
    # 数据库恢复逻辑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_restore_script = os.path.abspath(os.path.join(current_dir, "..", "..", "db", "restore_db.sh"))
    
    # 检查恢复脚本是否存在
    if not os.path.exists(db_restore_script):
        raise FileNotFoundError(f"数据库恢复脚本 {db_restore_script} 不存在")
    
    # 执行数据库恢复脚本，使用--latest和--auto参数自动恢复最新的备份到school_management数据库
    try:
        result = subprocess.run([db_restore_script, "--latest", "school_management", "--auto"], 
                                capture_output=True, 
                                text=True, 
                                check=True)
        print("数据库恢复成功完成")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"数据库恢复失败: {e.stderr}")