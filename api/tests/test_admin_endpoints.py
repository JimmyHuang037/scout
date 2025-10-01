import json
import os
import pytest
from .test_curl_base import CurlTestBase
from config import Config

"""
管理员端点测试
使用 pytest 框架执行黑盒测试
"""


@pytest.mark.order("last")
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

    # ==================== 学生管理模块 ====================
    
    def test_student_01_get_list(self):
        """测试用例student_01: 获取学生列表"""
        self.run_api_test(
            "student_01", "获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/admin/students/', '|', 'jq'],
            "admin_student_01_get_students.json",
            self.test_setup
        )
    
    def test_student_02_create(self):
        """测试用例student_02: 创建学生"""
        self.run_api_test(
            "student_02", "创建学生",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/students/',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_id": "S9999", "student_name": "张三", "class_id": 1, "password": "pass123"}',
             '|', 'jq'],
            "admin_student_02_create_student.json",
            self.test_setup
        )
    
    def test_student_03_get_specific(self):
        """测试用例student_03: 获取特定学生"""
        self.run_api_test(
            "student_03", "获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S0201', '|', 'jq'],
            "admin_student_03_get_student.json",
            self.test_setup
        )
    
    def test_student_04_update(self):
        """测试用例student_04: 更新学生信息"""
        self.run_api_test(
            "student_04", "更新学生信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/students/S0201',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "更新的学生姓名"}',
             '|', 'jq'],
            "admin_student_04_update_student.json",
            self.test_setup
        )
    
    def test_student_05_delete(self):
        """测试用例student_05: 删除学生"""
        self.run_api_test(
            "student_05", "删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S0201', '|', 'jq'],
            "admin_student_05_delete_student.json",
            self.test_setup
        )
    
    def test_student_06_get_not_found(self):
        """测试用例student_06: 获取不存在的学生"""
        self.run_api_test(
            "student_06", "获取不存在的学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S9999', '|', 'jq'],
            "admin_student_06_get_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_student_07_update_not_found(self):
        """测试用例student_07: 更新不存在的学生"""
        self.run_api_test(
            "student_07", "更新不存在的学生",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/students/S9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"student_name": "不存在的学生"}',
             '|', 'jq'],
            "admin_student_07_update_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_student_08_delete_not_found(self):
        """测试用例student_08: 删除不存在的学生"""
        self.run_api_test(
            "student_08", "删除不存在的学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S9999', '|', 'jq'],
            "admin_student_08_delete_student_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 教师管理模块 ====================
    
    def test_teacher_01_get_list(self):
        """测试用例teacher_01: 获取教师列表"""
        self.run_api_test(
            "teacher_01", "获取教师列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/', '|', 'jq'],
            "admin_teacher_01_get_teachers.json",
            self.test_setup
        )
    
    def test_teacher_02_create(self):
        """测试用例teacher_02: 创建教师"""
        self.run_api_test(
            "teacher_02", "创建教师",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teachers/',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 9999, "teacher_name": "李老师", "subject_id": 1, "password": "pass123"}',
             '|', 'jq'],
            "admin_teacher_02_create_teacher.json",
            self.test_setup
        )
    
    def test_teacher_03_get_specific(self):
        """测试用例teacher_03: 获取特定教师"""
        self.run_api_test(
            "teacher_03", "获取特定教师",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/1', '|', 'jq'],
            "admin_teacher_03_get_teacher.json",
            self.test_setup
        )
    
    def test_teacher_04_update(self):
        """测试用例teacher_04: 更新教师信息"""
        self.run_api_test(
            "teacher_04", "更新教师信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teachers/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "更新的教师姓名"}',
             '|', 'jq'],
            "admin_teacher_04_update_teacher.json",
            self.test_setup
        )
    
    def test_teacher_05_delete(self):
        """测试用例teacher_05: 删除教师"""
        self.run_api_test(
            "teacher_05", "删除教师",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teachers/1', '|', 'jq'],
            "admin_teacher_05_delete_teacher.json",
            self.test_setup
        )
    
    def test_teacher_06_get_not_found(self):
        """测试用例teacher_06: 获取不存在的教师"""
        self.run_api_test(
            "teacher_06", "获取不存在的教师",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/9999', '|', 'jq'],
            "admin_teacher_06_get_teacher_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_07_update_not_found(self):
        """测试用例teacher_07: 更新不存在的教师"""
        self.run_api_test(
            "teacher_07", "更新不存在的教师",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teachers/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "不存在的教师"}',
             '|', 'jq'],
            "admin_teacher_07_update_teacher_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_08_delete_not_found(self):
        """测试用例teacher_08: 删除不存在的教师"""
        self.run_api_test(
            "teacher_08", "删除不存在的教师",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teachers/9999', '|', 'jq'],
            "admin_teacher_08_delete_teacher_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 班级管理模块 ====================
    
    def test_class_01_get_list(self):
        """测试用例class_01: 获取班级列表"""
        self.run_api_test(
            "class_01", "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/', '|', 'jq'],
            "admin_class_01_get_classes.json",
            self.test_setup
        )
    
    def test_class_02_create(self):
        """测试用例class_02: 创建班级"""
        self.run_api_test(
            "class_02", "创建班级",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/classes/',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "测试班"}',
             '|', 'jq'],
            "admin_class_02_create_class.json",
            self.test_setup
        )
    
    def test_class_03_get_specific(self):
        """测试用例class_03: 获取特定班级"""
        self.run_api_test(
            "class_03", "获取特定班级",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/1', '|', 'jq'],
            "admin_class_03_get_class.json",
            self.test_setup
        )
    
    def test_class_04_update(self):
        """测试用例class_04: 更新班级信息"""
        self.run_api_test(
            "class_04", "更新班级信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/classes/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "更新的班级名称"}',
             '|', 'jq'],
            "admin_class_04_update_class.json",
            self.test_setup
        )
    
    def test_class_05_delete(self):
        """测试用例class_05: 删除班级"""
        self.run_api_test(
            "class_05", "删除班级",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/classes/1', '|', 'jq'],
            "admin_class_05_delete_class.json",
            self.test_setup
        )
    
    def test_class_06_get_not_found(self):
        """测试用例class_06: 获取不存在的班级"""
        self.run_api_test(
            "class_06", "获取不存在的班级",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/9999', '|', 'jq'],
            "admin_class_06_get_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_class_07_update_not_found(self):
        """测试用例class_07: 更新不存在的班级"""
        self.run_api_test(
            "class_07", "更新不存在的班级",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/classes/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "不存在的班级"}',
             '|', 'jq'],
            "admin_class_07_update_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_class_08_delete_not_found(self):
        """测试用例class_08: 删除不存在的班级"""
        self.run_api_test(
            "class_08", "删除不存在的班级",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/classes/9999', '|', 'jq'],
            "admin_class_08_delete_class_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 科目管理模块 ====================
    
    def test_subject_01_get_list(self):
        """测试用例subject_01: 获取科目列表"""
        self.run_api_test(
            "subject_01", "获取科目列表",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/', '|', 'jq'],
            "admin_subject_01_get_subjects.json",
            self.test_setup
        )
    
    def test_subject_02_create(self):
        """测试用例subject_02: 创建科目"""
        self.run_api_test(
            "subject_02", "创建科目",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/subjects/',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "测试科目"}',
             '|', 'jq'],
            "admin_subject_02_create_subject.json",
            self.test_setup
        )
    
    def test_subject_03_get_specific(self):
        """测试用例subject_03: 获取特定科目"""
        self.run_api_test(
            "subject_03", "获取特定科目",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/1', '|', 'jq'],
            "admin_subject_03_get_subject.json",
            self.test_setup
        )
    
    def test_subject_04_update(self):
        """测试用例subject_04: 更新科目信息"""
        self.run_api_test(
            "subject_04", "更新科目信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/subjects/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "更新的科目名称"}',
             '|', 'jq'],
            "admin_subject_04_update_subject.json",
            self.test_setup
        )
    
    def test_subject_05_delete(self):
        """测试用例subject_05: 删除科目"""
        self.run_api_test(
            "subject_05", "删除科目",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/subjects/1', '|', 'jq'],
            "admin_subject_05_delete_subject.json",
            self.test_setup
        )
    
    def test_subject_06_get_not_found(self):
        """测试用例subject_06: 获取不存在的科目"""
        self.run_api_test(
            "subject_06", "获取不存在的科目",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/9999', '|', 'jq'],
            "admin_subject_06_get_subject_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_subject_07_update_not_found(self):
        """测试用例subject_07: 更新不存在的科目"""
        self.run_api_test(
            "subject_07", "更新不存在的科目",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/subjects/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "不存在的科目"}',
             '|', 'jq'],
            "admin_subject_07_update_subject_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_subject_08_delete_not_found(self):
        """测试用例subject_08: 删除不存在的科目"""
        self.run_api_test(
            "subject_08", "删除不存在的科目",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/subjects/9999', '|', 'jq'],
            "admin_subject_08_delete_subject_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 考试类型管理模块 ====================
    
    def test_exam_type_01_get_list(self):
        """测试用例exam_type_01: 获取考试类型列表"""
        self.run_api_test(
            "exam_type_01", "获取考试类型列表",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/', '|', 'jq'],
            "admin_exam_type_01_get_exam_types.json",
            self.test_setup
        )
    
    def test_exam_type_02_create(self):
        """测试用例exam_type_02: 创建考试类型"""
        self.run_api_test(
            "exam_type_02", "创建考试类型",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/exam_types/',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "期中考试"}',
             '|', 'jq'],
            "admin_exam_type_02_create_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_03_get_specific(self):
        """测试用例exam_type_03: 获取特定考试类型"""
        self.run_api_test(
            "exam_type_03", "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/1', '|', 'jq'],
            "admin_exam_type_03_get_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_04_update(self):
        """测试用例exam_type_04: 更新考试类型信息"""
        self.run_api_test(
            "exam_type_04", "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam_types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "更新的考试类型"}',
             '|', 'jq'],
            "admin_exam_type_04_update_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_05_delete(self):
        """测试用例exam_type_05: 删除考试类型"""
        self.run_api_test(
            "exam_type_05", "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam_types/1', '|', 'jq'],
            "admin_exam_type_05_delete_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_06_get_not_found(self):
        """测试用例exam_type_06: 获取不存在的考试类型"""
        self.run_api_test(
            "exam_type_06", "获取不存在的考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/9999', '|', 'jq'],
            "admin_exam_type_06_get_exam_type_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_exam_type_07_update_not_found(self):
        """测试用例exam_type_07: 更新不存在的考试类型"""
        self.run_api_test(
            "exam_type_07", "更新不存在的考试类型",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam_types/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "不存在的考试类型"}',
             '|', 'jq'],
            "admin_exam_type_07_update_exam_type_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_exam_type_08_delete_not_found(self):
        """测试用例exam_type_08: 删除不存在的考试类型"""
        self.run_api_test(
            "exam_type_08", "删除不存在的考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam_types/9999', '|', 'jq'],
            "admin_exam_type_08_delete_exam_type_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 教师班级关联管理模块 ====================
    
    def test_teacher_class_01_get_list(self):
        """测试用例teacher_class_01: 获取教师班级关联列表"""
        self.run_api_test(
            "teacher_class_01", "获取教师班级关联列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/', '|', 'jq'],
            "admin_teacher_class_01_get_teacher_classes.json",
            self.test_setup
        )
    
    def test_teacher_class_02_create(self):
        """测试用例teacher_class_02: 创建教师班级关联"""
        self.run_api_test(
            "teacher_class_02", "创建教师班级关联",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teacher_classes/',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 2, "class_id": 3}',
             '|', 'jq'],
            "admin_teacher_class_02_create_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_03_get_specific(self):
        """测试用例teacher_class_03: 获取特定教师班级关联"""
        self.run_api_test(
            "teacher_class_03", "获取特定教师班级关联",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/2/2', '|', 'jq'],
            "admin_teacher_class_03_get_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_04_update(self):
        """测试用例teacher_class_04: 更新教师班级关联"""
        self.run_api_test(
            "teacher_class_04", "更新教师班级关联",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teacher_classes/4/6',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 2}',
             '|', 'jq'],
            "admin_teacher_class_04_update_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_05_delete(self):
        """测试用例teacher_class_05: 删除教师班级关联"""
        self.run_api_test(
            "teacher_class_05", "删除教师班级关联",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teacher_classes/4/8', 
             '-H', 'Content-Type: application/json',
             '-d', '{"class_id": 1}',
             '|', 'jq'],
            "admin_teacher_class_05_delete_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_06_get_not_found(self):
        """测试用例teacher_class_06: 获取不存在的教师班级关联"""
        self.run_api_test(
            "teacher_class_06", "获取不存在的教师班级关联",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/9999', '|', 'jq'],
            "admin_teacher_class_06_get_teacher_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_class_07_update_not_found(self):
        """测试用例teacher_class_07: 更新不存在的教师班级关联"""
        self.run_api_test(
            "teacher_class_07", "更新不存在的教师班级关联",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teacher_classes/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 9999, "class_id": 9999}',
             '|', 'jq'],
            "admin_teacher_class_07_update_teacher_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_class_08_delete_not_found(self):
        """测试用例teacher_class_08: 删除不存在的教师班级关联"""
        self.run_api_test(
            "teacher_class_08", "删除不存在的教师班级关联",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teacher_classes/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_id": 9999}',
             '|', 'jq'],
            "admin_teacher_class_08_delete_teacher_class_not_found.json",
            self.test_setup,
            expect_error=True
        )