# 测试框架
1. 采用pytest做框架
2. 数据库 school management or test 都是 localhost root Newuser1 访问。
3. 测试时候，采用两个数据库2. 当测试时候，采用testing config, 用5010端口，schoolmanage_test.db
4. 测试时候，采用两个数据库2. api/test/test_py 是白盒测试，对所有py做测试
5. api/test/test_curl 是黑盒测试，用curl对blueprint的所有api功能进行测试。