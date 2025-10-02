# 重构建议

基于对蓝图代码的分析，我发现了以下可以重构和改进的地方：

## 1. 输入验证的重构

许多蓝图中的输入验证逻辑是重复的。我们可以创建一个通用的输入验证函数来处理这些重复代码。

例如，在多个蓝图中都有类似的代码：
```python
data = request.get_json()
if not data:
    return error_response("请求数据不能为空", 400)
```

可以创建一个通用的验证函数来处理这种情况。

### 实现方案

已在 `apps/utils/helpers.py` 中添加了 `validate_json_input` 函数：

```python
def validate_json_input(required_fields=None):
    """
    验证JSON输入数据
    
    Args:
        required_fields (list): 必需的字段列表
        
    Returns:
        tuple: (data, error_response) 如果验证成功，error_response为None；如果验证失败，data为None
    """
    # 获取请求数据
    data = request.get_json()
    if not data:
        return None, error_response("请求数据不能为空", 400)
    
    # 检查必需字段
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                return None, error_response(f"缺少必需字段: {field}", 400)
    
    return data, None
```

### 使用示例

在蓝图中使用该函数的示例：

```python
@handle_exceptions
def create_student():
    """
    创建学生
    
    Returns:
        JSON: 创建结果
    """
    # 验证请求数据
    data, error = validate_json_input(['student_id', 'student_name', 'class_id'])
    if error:
        return error
    
    student_id = data.get('student_id')
    student_name = data.get('student_name')
    class_id = data.get('class_id')
    password = data.get('password')
    
    # ... 其余代码
```

### 已重构的蓝图

以下蓝图已经应用了新的输入验证函数：
- `apps/blueprints/admin/students.py`
- `apps/blueprints/admin/teachers.py`
- `apps/blueprints/admin/classes.py`
- `apps/blueprints/admin/subjects.py`
- `apps/blueprints/admin/exam_types.py`
- `apps/blueprints/admin/teacher_classes.py`

## 3. 错误处理的一致性

虽然使用了[@handle_exceptions](file:///home/jimmy/repo/scout/api/apps/utils/decorators.py#L36-L71)装饰器，但在某些地方仍然有手动的错误处理代码。可以考虑统一错误处理方式。

### 已完成的重构

以下文件中的手动错误处理代码已经被移除，现在完全依赖[@handle_exceptions](file:///home/jimmy/repo/scout/api/apps/utils/decorators.py#L36-L71)装饰器：

- `apps/blueprints/admin/teacher_classes.py` 中的 [create_teacher_class](file:///home/jimmy/repo/scout/api/apps/services/teacher_class_service.py#L100-L142) 函数已移除 `try/except` 块
- `apps/blueprints/auth.py` 中的 [login](file:///home/jimmy/repo/scout/api/apps/blueprints/auth.py#L15-L37)、[logout](file:///home/jimmy/repo/scout/api/apps/blueprints/auth.py#L40-L51) 和 [get_current_user](file:///home/jimmy/repo/scout/api/apps/blueprints/auth.py#L54-L71) 函数已移除手动的 `try/except` 块

## 5. 响应消息的中英文混合问题

在一些蓝图中，响应消息存在中英文混合的问题，例如在[student.py](file:///home/jimmy/repo/scout/api/apps/blueprints/student.py)中：
```python
return error_response('Student profile not found', 404)
```

应该统一使用中文消息。

### 已完成的修复

以下文件中的中英文混合消息已修复为中文：

- `apps/blueprints/student.py` 中的所有错误消息已改为中文
- `apps/blueprints/teacher.py` 中的所有错误消息已改为中文
- `apps/blueprints/auth.py` 中的所有错误消息已改为中文

## 7. 命名规范的统一

某些函数命名可以更加清晰和统一，例如[teacher.py](file:///home/jimmy/repo/scout/api/apps/services/teacher_service.py)中的[get_scores](file:///home/jimmy/repo/scout/api/apps/blueprints/teacher.py#L23-L42)函数可以重命名为[get_teacher_scores](file:///home/jimmy/repo/scout/api/apps/services/teacher_service.py#L105-L123)以提高可读性。

### 已完成的改进

以下文件中的函数命名已改进：

- `apps/blueprints/teacher.py` 中的 [get_scores](file:///home/jimmy/repo/scout/api/apps/blueprints/teacher.py#L23-L42) 函数已重命名为 [get_teacher_scores](file:///home/jimmy/repo/scout/api/apps/services/teacher_service.py#L309-L342)

## 8. 数据访问模式的统一

在[auth.py](file:///home/jimmy/repo/scout/api/apps/blueprints/auth.py)中直接使用了数据库服务，而不是通过专门的服务层，这违反了分层架构的原则。应该将数据库访问逻辑移到服务层。