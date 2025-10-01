import os
from .test_curl_base import CurlTestBase
from config import Config
"""
教师端点测试
使用 pytest 框架执行黑盒测试
"""



class TestTeacherEndpoints(CurlTestBase):
    """教师端点测试类 - 无需登录和会话的测试"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.test_results_dir = Config.TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "teacher_curl_commands.log")
        
        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
        }


    
    def test_01_get_scores(self):
        """测试用例1: 教师获取学生成绩列表"""
        self.run_api_test(
            1, "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/scores', '|', 'jq'],
            "teacher_01_get_scores.json",
            self.test_setup
        )
    
    def test_02_update_score_success(self):
        """测试用例2: 教师更新学生成绩 - 正常情况"""
        self.run_api_test(
            2, "教师更新学生成绩 - 正常情况",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/1/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 92}',
             '|', 'jq'],
            "teacher_02_update_score_success.json",
            self.test_setup
        )
    
    def test_03_update_score_not_found(self):
        """测试用例3: 教师更新学生成绩 - 更新不存在的成绩"""
        self.run_api_test(
            3, "教师更新学生成绩 - 更新不存在的成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/1/scores/999',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 85}',
             '|', 'jq'],
            "teacher_03_update_score_not_found.json",
            self.test_setup
        )
    
    def test_04_update_score_invalid_range(self):
        """测试用例4: 教师更新学生成绩 - 分数超出范围"""
        self.run_api_test(
            4, "教师更新学生成绩 - 分数超出范围",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/1/scores/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 150}',
             '|', 'jq'],
            "teacher_04_update_score_invalid_range.json",
            self.test_setup
        )
    
    def test_05_get_classes(self):
        """测试用例5: 获取班级列表"""
        self.run_api_test(
            5, "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes', '|', 'jq'],
            "teacher_05_get_classes.json",
            self.test_setup
        )
    
    def test_06_get_class_by_id(self):
        """测试用例6: 根据ID获取班级"""
        self.run_api_test(
            6, "根据ID获取班级",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes/1', '|', 'jq'],
            "teacher_06_get_class_by_id.json",
            self.test_setup
        )
    
    def test_07_get_class_not_found(self):
        """测试用例7: 获取不存在的班级"""
        self.run_api_test(
            7, "获取不存在的班级",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes/999', '|', 'jq'],
            "teacher_07_get_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_08_get_students(self):
        """测试用例8: 教师获取学生列表"""
        self.run_api_test(
            8, "教师获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/students', '|', 'jq'],
            "teacher_08_get_students.json",
            self.test_setup
        )
    
    def test_09_get_student_by_id(self):
        """测试用例9: 教师根据ID获取学生"""
        self.run_api_test(
            9, "教师根据ID获取学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/students/S0601', '|', 'jq'],
            "teacher_09_get_student_by_id.json",
            self.test_setup
        )
    
    def test_10_get_student_not_found(self):
        """测试用例10: 教师获取不存在的学生"""
        self.run_api_test(
            10, "教师获取不存在的学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/students/NOTEXIST', '|', 'jq'],
            "teacher_10_get_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_11_get_class_students(self):
        """测试用例11: 教师获取班级学生列表（无权限访问的班级）"""
        self.run_api_test(
            11, "教师获取班级学生列表（无权限访问的班级）",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes/1/students', '|', 'jq'],
            "teacher_11_get_class_students.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_12_get_class_6_students(self):
        """测试用例12: 教师获取班级6学生列表（有权限访问的班级）"""
        self.run_api_test(
            12, "教师获取班级6学生列表（有权限访问的班级）",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes/6/students', '|', 'jq'],
            "teacher_12_get_class_6_students.json",
            self.test_setup
        )
    
    def test_13_get_all_classes_students(self):
        """测试用例13: 教师获取所有班级学生列表"""
        self.run_api_test(
            13, "教师获取所有班级学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes/students', '|', 'jq'],
            "teacher_13_get_all_classes_students.json",
            self.test_setup
        )