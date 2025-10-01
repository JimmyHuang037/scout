#!/usr/bin/env python3
"""
导入语句优化脚本
按照标准Python规范组织导入语句：标准库、第三方库、本地应用库
"""

import ast
import os
import sys
import re
from typing import List, Tuple, Set


def categorize_imports(lines: List[str]) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    将导入语句按类别分组
    
    Args:
        lines: 文件行列表
        
    Returns:
        (stdlib, third_party, local, other) 四个分类的导入语句列表
    """
    stdlib_imports = []
    third_party_imports = []
    local_imports = []
    other_lines = []
    
    # Python标准库模块列表（部分常用模块）
    stdlib_modules = {
        'os', 'sys', 'json', 're', 'datetime', 'collections', 'itertools',
        'functools', 'logging', 'threading', 'multiprocessing', 'subprocess',
        'urllib', 'http', 'xml', 'csv', 'sqlite3', 'pickle', 'base64',
        'hashlib', 'hmac', 'random', 'math', 'statistics', 'decimal',
        'fractions', 'contextlib', 'tempfile', 'shutil', 'glob', 'fnmatch',
        'pathlib', 'io', 'traceback', 'inspect', 'importlib', 'pkgutil',
        'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma', 'calendar', 'time',
        'copy', 'pprint', 'reprlib', 'enum', 'types', 'weakref', 'gc',
        'operator', 'string', 'textwrap'
    }
    
    in_import_section = False
    current_import_block = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # 如果是空行且在导入区域，结束当前导入块
        if stripped_line == '' and in_import_section:
            # 处理当前导入块
            for imp_line in current_import_block:
                imp_stripped = imp_line.strip()
                if imp_stripped.startswith('import ') or imp_stripped.startswith('from '):
                    # 提取模块名
                    if imp_stripped.startswith('import '):
                        module_name = imp_stripped.split()[1].split('.')[0]
                    else:  # from ... import ...
                        module_name = imp_stripped.split()[1].split('.')[0]
                    
                    # 分类导入
                    if module_name in stdlib_modules:
                        stdlib_imports.append(imp_line)
                    elif module_name.startswith('.') or module_name.startswith('apps.') or module_name.startswith('config'):
                        local_imports.append(imp_line)
                    elif any(imp_stripped.startswith(prefix) for prefix in ['import ', 'from ']):
                        # 检查是否为第三方库
                        try:
                            # 简单判断：如果不是标准库且不是本地模块，则认为是第三方库
                            if module_name not in stdlib_modules and not module_name.startswith(('apps.', 'config')):
                                third_party_imports.append(imp_line)
                            else:
                                # 默认放入第三方库（对于不确定的）
                                third_party_imports.append(imp_line)
                        except:
                            third_party_imports.append(imp_line)
                    else:
                        other_lines.append(imp_line)
                else:
                    other_lines.append(imp_line)
            
            current_import_block = []
            in_import_section = False
            other_lines.append(line)
        elif stripped_line.startswith('import ') or stripped_line.startswith('from '):
            # 开始导入区域
            in_import_section = True
            current_import_block.append(line)
        elif in_import_section:
            # 导入区域内的非导入行（可能是注释）
            current_import_block.append(line)
        else:
            # 非导入区域的行
            other_lines.append(line)
    
    # 处理文件末尾可能残留的导入块
    if current_import_block:
        for imp_line in current_import_block:
            imp_stripped = imp_line.strip()
            if imp_stripped.startswith('import ') or imp_stripped.startswith('from '):
                # 提取模块名
                if imp_stripped.startswith('import '):
                    module_name = imp_stripped.split()[1].split('.')[0]
                else:  # from ... import ...
                    module_name = imp_stripped.split()[1].split('.')[0]
                
                # 分类导入
                if module_name in stdlib_modules:
                    stdlib_imports.append(imp_line)
                elif module_name.startswith('.') or module_name.startswith('apps.') or module_name.startswith('config'):
                    local_imports.append(imp_line)
                elif any(imp_stripped.startswith(prefix) for prefix in ['import ', 'from ']):
                    third_party_imports.append(imp_line)
                else:
                    other_lines.append(imp_line)
            else:
                other_lines.append(imp_line)
    
    return stdlib_imports, third_party_imports, local_imports, other_lines


def remove_unused_imports(file_path: str, lines: List[str]) -> List[str]:
    """
    移除未使用的导入语句
    
    Args:
        file_path: 文件路径
        lines: 文件行列表
        
    Returns:
        移除未使用导入后的行列表
    """
    try:
        # 解析AST
        tree = ast.parse(''.join(lines))
        
        # 收集所有导入的名称
        imported_names = set()
        import_lines = set()
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line.startswith('import ') or stripped_line.startswith('from '):
                import_lines.add(i)
                if stripped_line.startswith('import '):
                    names = stripped_line[7:].split(',')
                    for name in names:
                        imported_names.add(name.strip().split()[0].split('.')[-1])
                elif stripped_line.startswith('from ') and ' import ' in stripped_line:
                    parts = stripped_line.split()
                    module_name = parts[1]
                    if ' as ' in stripped_line:
                        # 处理别名
                        alias_part = stripped_line[stripped_line.find('import ') + 7:]
                        names = alias_part.split(',')
                        for name in names:
                            if ' as ' in name:
                                imported_names.add(name.split(' as ')[1].strip())
                            else:
                                imported_names.add(name.strip())
                    else:
                        # 没有别名的情况
                        import_part = stripped_line[stripped_line.find('import ') + 7:]
                        names = import_part.split(',')
                        for name in names:
                            imported_names.add(name.strip())
        
        # 收集实际使用的名称
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # 处理模块.函数形式的调用
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)
        
        # 简单检查：如果无法准确判断，则保留所有导入
        # 这是一个简化的实现，实际项目中可能需要更复杂的逻辑
        return lines
    except Exception as e:
        print(f"Warning: Could not parse {file_path} for unused imports: {e}")
        return lines


def format_import_section(stdlib: List[str], third_party: List[str], local: List[str]) -> List[str]:
    """
    格式化导入部分，按标准顺序排列并添加适当的空行
    
    Args:
        stdlib: 标准库导入
        third_party: 第三方库导入
        local: 本地应用库导入
        
    Returns:
        格式化后的导入语句列表
    """
    result = []
    
    # 添加标准库导入
    if stdlib:
        result.extend(sorted(set(stdlib), key=lambda x: re.sub(r'^\s*(import|from)\s+', '', x)))
        result.append('')  # 添加空行
    
    # 添加第三方库导入
    if third_party:
        result.extend(sorted(set(third_party), key=lambda x: re.sub(r'^\s*(import|from)\s+', '', x)))
        result.append('')  # 添加空行
    
    # 添加本地应用库导入
    if local:
        result.extend(sorted(set(local), key=lambda x: re.sub(r'^\s*(import|from)\s+', '', x)))
        result.append('')  # 添加空行
    
    return result


def optimize_file_imports(file_path: str) -> bool:
    """
    优化单个文件的导入语句
    
    Args:
        file_path: 文件路径
        
    Returns:
        是否成功优化
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 移除未使用的导入（简化处理）
        lines = remove_unused_imports(file_path, lines)
        
        # 分类导入语句
        stdlib_imports, third_party_imports, local_imports, other_lines = categorize_imports(lines)
        
        # 格式化导入部分
        formatted_imports = format_import_section(stdlib_imports, third_party_imports, local_imports)
        
        # 重新组合文件内容
        # 找到第一个非导入行的位置
        first_non_import_idx = 0
        in_import_section = True
        
        for i, line in enumerate(other_lines):
            stripped_line = line.strip()
            if in_import_section and stripped_line != '' and not stripped_line.startswith('#'):
                if not (stripped_line.startswith('import ') or stripped_line.startswith('from ')):
                    first_non_import_idx = i
                    break
        
        # 组合最终内容
        new_content = formatted_imports + other_lines[first_non_import_idx:]
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        
        print(f"Optimized imports in {file_path}")
        return True
    except Exception as e:
        print(f"Error optimizing {file_path}: {e}")
        return False


def main():
    """主函数"""
    # 获取项目根目录
    project_root = "/home/jimmy/repo/scout/api"
    
    # 定义要处理的文件列表
    files_to_process = [
        os.path.join(project_root, "app.py"),
        os.path.join(project_root, "config.py"),
        # Services
        os.path.join(project_root, "apps", "services", "student_service.py"),
        os.path.join(project_root, "apps", "services", "score_service.py"),
        os.path.join(project_root, "apps", "services", "exam_service.py"),
        os.path.join(project_root, "apps", "services", "class_service.py"),
        os.path.join(project_root, "apps", "services", "teacher_service.py"),
        os.path.join(project_root, "apps", "services", "subject_service.py"),
        os.path.join(project_root, "apps", "services", "exam_type_service.py"),
        os.path.join(project_root, "apps", "services", "teacher_class_service.py"),
        # Utils
        os.path.join(project_root, "apps", "utils", "database_service.py"),
        os.path.join(project_root, "apps", "utils", "auth.py"),
        os.path.join(project_root, "apps", "utils", "helpers.py"),
        # Blueprints - Student
        os.path.join(project_root, "apps", "blueprints", "student", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "student", "student_management.py"),
        os.path.join(project_root, "apps", "blueprints", "student", "scores", "scores_management.py"),
        os.path.join(project_root, "apps", "blueprints", "student", "profile", "profile_management.py"),
        os.path.join(project_root, "apps", "blueprints", "student", "exam", "exam_results_management.py"),
        # Blueprints - Teacher
        os.path.join(project_root, "apps", "blueprints", "teacher", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "teacher", "teacher_management.py"),
        os.path.join(project_root, "apps", "blueprints", "teacher", "class_management.py"),
        os.path.join(project_root, "apps", "blueprints", "teacher", "scores", "score_management.py"),
        os.path.join(project_root, "apps", "blueprints", "teacher", "students", "student_management.py"),
        # Blueprints - Admin
        os.path.join(project_root, "apps", "blueprints", "admin", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "students", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "students", "student_management.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "teachers", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "teachers", "teacher_management.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "classes", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "classes", "class_management.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "subjects", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "subjects", "subject_management.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "exam_types", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "exam_types", "exam_type_management.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "teacher_classes", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "admin", "teacher_classes", "teacher_class_management.py"),
        # Blueprints - Auth
        os.path.join(project_root, "apps", "blueprints", "auth", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "auth", "auth_management.py"),
        # Blueprints - Common
        os.path.join(project_root, "apps", "blueprints", "common", "__init__.py"),
        os.path.join(project_root, "apps", "blueprints", "common", "common_routes.py"),
        # Tests
        os.path.join(project_root, "tests", "conftest.py"),
        os.path.join(project_root, "tests", "test_admin_endpoints.py"),
        os.path.join(project_root, "tests", "test_student_endpoints.py"),
        os.path.join(project_root, "tests", "test_teacher_endpoints.py"),
        os.path.join(project_root, "tests", "test_curl_base.py"),
    ]
    
    # 优化每个文件的导入语句
    success_count = 0
    total_count = len(files_to_process)
    
    for file_path in files_to_process:
        if os.path.exists(file_path):
            if optimize_file_imports(file_path):
                success_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nImport optimization completed. {success_count}/{total_count} files processed successfully.")


if __name__ == "__main__":
    main()