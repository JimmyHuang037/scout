import os


def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def ensure_parent_dir_exists(file_path):
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        ensure_dir_exists(parent_dir)