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

    # ==================== 个人资料相关测试 ====================
    
    def test_profile_01_get_teacher_profile(self):
        """测试用例profile_01: 教师获取个人资料"""
        self.run_api_test(
            "profile_01", "教师获取个人资料",
            ['curl', '-s', f'{self.base_url}/api/teacher/profile/1', '|', 'jq'],
            "teacher_profile_01_get_profile.json",
            self.test_setup
        )

    # ==================== 成绩管理相关测试 ====================
    
    def test_scores_01_get_scores(self):
        """测试用例scores_01: 教师获取学生成绩列表"""
        self.run_api_test(
            "scores_01", "教师获取学生成绩列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/scores/1', '|', 'jq'],
            "teacher_scores_01_get_scores.json",
            self.test_setup
        )
    
    def test_scores_02_update_score_success(self):
        """测试用例scores_02: 教师成功更新学生成绩"""
        self.run_api_test(
            "scores_02", "教师成功更新学生成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1/1', 
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 95}',
             '|', 'jq'],
            "teacher_scores_02_update_score_success.json",
            self.test_setup
        )

    def test_scores_03_update_score_not_found(self):
        """测试用例scores_03: 教师更新不存在的成绩"""
        self.run_api_test(
            "scores_03", "教师更新不存在的成绩",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1/99999', 
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 85}',
             '|', 'jq'],
            "teacher_scores_03_update_score_not_found.json",
            self.test_setup
        )

    def test_scores_04_update_score_invalid_range(self):
        """测试用例scores_04: 教师更新成绩超出有效范围"""
        self.run_api_test(
            "scores_04", "教师更新成绩超出有效范围",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/teacher/scores/1/1', 
             '-H', 'Content-Type: application/json',
             '-d', '{"score": 150}',
             '|', 'jq'],
            "teacher_scores_04_update_score_invalid_range.json",
            self.test_setup
        )

    # ==================== 班级管理相关测试 ====================
    
    def test_classes_01_get_classes(self):
        """测试用例classes_01: 教师获取班级列表"""
        self.run_api_test(
            "classes_01", "教师获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/1', '|', 'jq'],
            "teacher_classes_01_get_classes.json",
            self.test_setup
        )
    
    def test_classes_02_get_class_by_id(self):
        """测试用例classes_02: 教师获取指定班级信息"""
        self.run_api_test(
            "classes_02", "教师获取指定班级信息",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/1/1', '|', 'jq'],
            "teacher_classes_02_get_class_by_id.json",
            self.test_setup
        )
    
    def test_classes_03_get_class_not_found(self):
        """测试用例classes_03: 教师获取不存在的班级"""
        self.run_api_test(
            "classes_03", "教师获取不存在的班级",
            ['curl', '-s', f'{self.base_url}/api/teacher/classes/1/999', '|', 'jq'],
            "teacher_classes_03_get_class_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 学生管理相关测试 ====================
    
    def test_students_01_get_students(self):
        """测试用例students_01: 教师获取学生列表"""
        self.run_api_test(
            "students_01", "教师获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/1', '|', 'jq'],
            "teacher_students_01_get_students.json",
            self.test_setup
        )
    
    def test_students_02_get_student_by_id(self):
        """测试用例students_02: 教师获取指定学生信息"""
        self.run_api_test(
            "students_02", "教师获取指定学生信息",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/1/S0101', '|', 'jq'],
            "teacher_students_02_get_student_by_id.json",
            self.test_setup
        )
    
    def test_students_03_get_student_not_found(self):
        """测试用例students_03: 教师获取不存在的学生"""
        self.run_api_test(
            "students_03", "教师获取不存在的学生",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/students/NOTEXIST', '|', 'jq'],
            "teacher_students_03_get_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_students_04_get_class_students(self):
        """测试用例students_04: 教师获取班级学生列表（无权限访问的班级）"""
        self.run_api_test(
            "students_04", "教师获取班级学生列表（无权限访问的班级）",
            ['curl', '-s', f'{self.base_url}/api/teacher/1/classes/1/students', '|', 'jq'],
            "teacher_students_04_get_class_students.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_students_05_get_class_6_students(self):
        """测试用例students_05: 教师获取班级6学生列表（有权限访问的班级）"""
        self.run_api_test(
            "students_05", "教师获取班级6学生列表（有权限访问的班级）",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/1/class/6', '|', 'jq'],
            "teacher_students_05_get_class_6_students.json",
            self.test_setup
        )
    
    def test_students_06_get_all_classes_students(self):
        """测试用例students_06: 教师获取所有班级学生列表"""
        self.run_api_test(
            "students_06", "教师获取所有班级学生列表",
            ['curl', '-s', f'{self.base_url}/api/teacher/students/1/all_classes_students', '|', 'jq'],
            "teacher_students_06_get_all_classes_students.json",
            self.test_setup
        )