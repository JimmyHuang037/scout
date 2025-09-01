# 测试框架
1. 采用pytest做框架
2. 数据库 school management or test 都是 localhost root Newuser1 访问。
3. 当测试时候，采用testing config, 用5010端口，schoolmanage_test.db
4. api/test/test_py 是白盒测试，对所有py做测试
5. api/test/test_curl 是黑盒测试，用curl对blueprint的所有api功能进行测试。
6. test时，logs都记录到 项目目录/logs_testing/ 目录下
7. test_curl要记录每个curl的命令，同时将每个curl的结果输出到项目目录/logs_testing/下
8. 代码注释要简洁有效，不要太多。
9. 每个方法不应该超过15行代码
10. 学生测试规则：
    - 测试文件位于 api/tests/test_py/blueprints/student/ 目录下
    - 每个测试文件应专注于特定功能模块（如考试管理、个人信息管理、成绩查询等）
    - 使用student_client fixture进行已认证的学生用户测试
    - 需要测试学生权限范围内的所有功能
11. 后续添加的admin和teacher测试应遵循与学生测试类似的规则
12. 数据库恢复命令：
    - 手动恢复测试数据库命令：cd /home/jimmy/repo/scout/db && ./restore_db.sh school_management_backup_20250831_103236.sql school_management_test --auto
    - 恢复脚本会自动使用root用户和Newuser1密码连接数据库
    - 备份文件位于 /home/jimmy/repo/scout/db/backup/ 目录下
13. 数据库表和视图设计规则：
    - 基础表（如Students, Classes等）存储核心数据
    - 为简化查询操作，创建视图（如students, classes等）关联基础表的外键信息
    - 视图中包含关联表的常用字段，减少应用层的JOIN操作
    - 应用代码应优先使用视图而非直接查询基础表进行关联操作
    - 视图命名采用小写复数形式，基础表采用首字母大写的单数形式