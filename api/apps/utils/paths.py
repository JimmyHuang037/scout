import os


def ensure_dir_exists(dir_path):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        dir_path (str): 目录路径
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def ensure_parent_dir_exists(file_path):
    """
    确保文件的父目录存在，如果不存在则创建
    
    Args:
        file_path (str): 文件路径
    """
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        ensure_dir_exists(parent_dir)