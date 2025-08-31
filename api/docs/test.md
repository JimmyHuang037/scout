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