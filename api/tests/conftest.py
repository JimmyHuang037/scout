import glob
import os
import subprocess
import shutil
import pytest
"""
test_curl测试模块的配置文件
只保留数据库恢复功能
"""



@pytest.fixture(scope="session", autouse=True)
def restore_database():
    """在测试会话开始前恢复数据库"""
    # 清理日志文件
    cleanup_logs()
    
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


def cleanup_logs():
    """清理日志文件和测试日志目录"""
    # 获取项目根目录
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 清理 app.log 文件
    app_log_path = os.path.join(project_root, "logs", "app.log")
    if os.path.exists(app_log_path):
        # 清空文件内容而不是删除文件
        with open(app_log_path, 'w') as f:
            f.write('')
        print(f"已清理 {app_log_path}")
    
    # 清理 logs/test 目录
    test_logs_dir = os.path.join(project_root, "logs", "test")
    if os.path.exists(test_logs_dir):
        # 删除目录下的所有文件和子目录，但保留目录本身
        for filename in os.listdir(test_logs_dir):
            file_path = os.path.join(test_logs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'删除 {file_path} 失败. 原因: {e}')
        print(f"已清理 {test_logs_dir} 目录")