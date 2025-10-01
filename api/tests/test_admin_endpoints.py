import json
import os
from .test_curl_base import CurlTestBase
from config import Config

"""
管理员端点测试
使用 pytest 框架执行黑盒测试
"""


class TestAdminEndpoints(CurlTestBase):
    """管理员端点测试类 - 无需登录和会话的测试"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        # 调用父类的setup_class
        super().setup_class()
        
        cls.test_results_dir = Config.TEST_DIR
        cls.curl_commands_file = os.path.join(cls.test_results_dir, "admin_curl_commands.log")
        
        # 测试设置
        cls.test_setup = {
            'base_url': cls.base_url,
            'curl_commands_file': cls.curl_commands_file,
            'result_dir': cls.test_results_dir
        }

    
    def test_01_get_students(self):
        """测试用例1: 获取学生列表"""
        self.run_api_test(
            1, "获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/admin/students/', '|', 'jq'],
            "admin_01_get_students.json",
            self.test_setup
        )
    
    def test_02_create_student(self):
        """测试用例2: 创建学生"""
        self.run_api_test(
            2, "创建学生",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/students/',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S9999", "student_name": "张三", "class_id": 1, "password": "pass123"}',
             '|', 'jq'],
            "admin_02_create_student.json",
            self.test_setup
        )
    
    def test_03_get_student(self):
        """测试用例3: 获取特定学生"""
        self.run_api_test(
            3, "获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S0201', '|', 'jq'],
            "admin_03_get_student.json",
            self.test_setup
        )
    
    def test_04_update_student(self):
        """测试用例4: 更新学生信息"""
        self.run_api_test(
            4, "更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/students/S0201',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "更新的学生姓名"}',
             '|', 'jq'],
            "admin_04_update_student.json",
            self.test_setup
        )
    
    def test_05_delete_student(self):
        """测试用例5: 删除学生"""
        self.run_api_test(
            5, "删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S0201', '|', 'jq'],
            "admin_05_delete_student.json",
            self.test_setup
        )
    
    def test_06_get_teachers(self):
        """测试用例6: 获取教师列表"""
        self.run_api_test(
            6, "获取教师列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/', '|', 'jq'],
            "admin_06_get_teachers.json",
            self.test_setup
        )
    
    def test_07_create_teacher(self):
        """测试用例7: 创建教师"""
        self.run_api_test(
            7, "创建教师",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teachers/',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": "T9999", "teacher_name": "李老师", "subject_id": 1, "password": "pass123"}',
             '|', 'jq'],
            "admin_07_create_teacher.json",
            self.test_setup
        )
    
    def test_08_get_classes(self):
        """测试用例8: 获取班级列表"""
        self.run_api_test(
            8, "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/', '|', 'jq'],
            "admin_08_get_classes.json",
            self.test_setup
        )
    
    def test_09_create_class(self):
        """测试用例9: 创建班级"""
        self.run_api_test(
            9, "创建班级",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/classes/',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "测试班"}',
             '|', 'jq'],
            "admin_09_create_class.json",
            self.test_setup
        )
    
    def test_10_get_subjects(self):
        """测试用例10: 获取科目列表"""
        self.run_api_test(
            10, "获取科目列表",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/', '|', 'jq'],
            "admin_10_get_subjects.json",
            self.test_setup
        )
    
    def test_11_create_subject(self):
        """测试用例11: 创建科目"""
        self.run_api_test(
            11, "创建科目",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/subjects/',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "测试科目"}',
             '|', 'jq'],
            "admin_11_create_subject.json",
            self.test_setup
        )
    
    def test_12_get_exam_types(self):
        """测试用例12: 获取考试类型列表"""
        self.run_api_test(
            12, "获取考试类型列表",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/', '|', 'jq'],
            "admin_12_get_exam_types.json",
            self.test_setup
        )
    
    def test_13_create_exam_type(self):
        """测试用例13: 创建考试类型"""
        self.run_api_test(
            13, "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exam_types/',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "期中考试"}',
             '|', 'jq'],
            "admin_13_create_exam_type.json",
            self.test_setup
        )
    
    def test_14_get_teacher_classes(self):
        """测试用例14: 获取教师班级关联列表"""
        self.run_api_test(
            14, "获取教师班级关联列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/', '|', 'jq'],
            "admin_14_get_teacher_classes.json",
            self.test_setup
        )
    
    def test_15_create_teacher_class(self):
        """测试用例15: 创建教师班级关联"""
        self.run_api_test(
            15, "创建教师班级关联",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teacher_classes/',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": "1", "class_id": 1}',
             '|', 'jq'],
            "admin_15_create_teacher_class.json",
            self.test_setup
        )
    
    def test_16_get_student(self):
        """测试用例16: 获取特定学生（不存在的学生）"""
        self.run_api_test(
            16, "获取特定学生（不存在的学生）",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S9999', '|', 'jq'],
            "admin_16_get_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_17_update_student(self):
        """测试用例17: 更新不存在的学生"""
        self.run_api_test(
            17, "更新不存在的学生",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/students/S9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "不存在的学生"}',
             '|', 'jq'],
            "admin_17_update_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_18_delete_student(self):
        """测试用例18: 删除不存在的学生"""
        self.run_api_test(
            18, "删除不存在的学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S9999', '|', 'jq'],
            "admin_18_delete_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
