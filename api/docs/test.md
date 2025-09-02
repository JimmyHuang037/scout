# 测试文档

## 运行测试

### 基本测试命令

```bash
# 运行所有测试
cd /home/jimmy/repo/scout/api && python -m pytest

# 运行特定模块的测试
cd /home/jimmy/repo/scout/api && python -m pytest tests/test_py/services/

# 运行特定测试文件
cd /home/jimmy/repo/scout/api && python -m pytest tests/test_py/services/test_student_service.py

# 运行测试并将结果输出到文件（推荐）
cd /home/jimmy/repo/scout/api && python -m pytest > test_results.txt 2>&1 && cat test_results.txt
```

### 查看测试覆盖率

```bash
# 运行测试并生成覆盖率报告
cd /home/jimmy/repo/scout/api && coverage run -m pytest && coverage report

# 生成详细HTML覆盖率报告
cd /home/jimmy/repo/scout/api && coverage run -m pytest && coverage html
```

## 测试规则

1. 每次运行测试时会自动恢复测试数据库到初始状态
2. 测试使用独立的测试数据库`school_management_test`
3. 测试数据在每次运行时都会从备份文件中恢复
4. 所有测试应在Flask应用上下文中运行
5. 测试应使用真实存在的测试数据，避免使用不存在的ID
6. 运行测试时推荐将结果输出到文件，方便查看详细信息：
   ```bash
   cd /home/jimmy/repo/scout/api && python -m pytest > test_results.txt 2>&1 && cat test_results.txt
   ```

## 测试账户信息

在测试数据库中，有以下默认账户可用于测试：

### 管理员账户
- 用户ID: `admin`
- 密码: `admin`

### 教师账户
- 用户ID: `1` (以及其他ID如2, 8, 14, 20...)
- 密码: `test123` (ID为1的教师) 或 `123456` (其他教师)

### 学生账户
- 用户ID: `S0201` (及其他S开头的ID，如S0202, S0203...)
- 密码: `pass123`

这些账户在测试环境中由测试框架自动创建，并在每次测试运行时通过数据库恢复过程重新初始化。

## 常见问题

### 1. 数据库相关问题
- 确保测试数据库已正确创建
- 检查数据库连接配置是否正确
- 确认备份文件存在且可访问

### 2. Flask应用上下文问题
- 确保测试在应用上下文中运行
- 使用`with app.app_context():`包装需要应用上下文的代码

### 3. 测试数据问题
- 使用测试数据库中真实存在的数据
- 避免硬编码不存在的ID
- 对于创建操作，先确保清理可能存在的重复数据