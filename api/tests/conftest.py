import glob
import os
import subprocess
import pytest
"""
test_curl测试模块的配置文件
只保留数据库恢复功能
"""



@pytest.fixture(scope="session", autouse=True)
def restore_database():
    """在测试会话开始前恢复数据库"""
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