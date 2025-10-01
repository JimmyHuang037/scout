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

    # ==================== 学生管理模块 ====================
    
    def test_student_01_get_list(self):
        """测试用例1: 获取学生列表"""
        self.run_api_test(
            1, "获取学生列表",
            ['curl', '-s', f'{self.base_url}/api/admin/students/', '|', 'jq'],
            "admin_01_get_students.json",
            self.test_setup
        )
    
    def test_student_02_create(self):
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
    
    def test_student_03_get_specific(self):
        """测试用例3: 获取特定学生"""
        self.run_api_test(
            3, "获取特定学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S0201', '|', 'jq'],
            "admin_03_get_student.json",
            self.test_setup
        )
    
    def test_student_04_update(self):
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
    
    def test_student_05_delete(self):
        """测试用例5: 删除学生"""
        self.run_api_test(
            5, "删除学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S0201', '|', 'jq'],
            "admin_05_delete_student.json",
            self.test_setup
        )
    
    def test_student_06_get_not_found(self):
        """测试用例16: 获取不存在的学生"""
        self.run_api_test(
            16, "获取不存在的学生",
            ['curl', '-s', f'{self.base_url}/api/admin/students/S9999', '|', 'jq'],
            "admin_16_get_student_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_student_07_update_not_found(self):
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
    
    def test_student_08_delete_not_found(self):
        """测试用例18: 删除不存在的学生"""
        self.run_api_test(
            18, "删除不存在的学生",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/students/S9999', '|', 'jq'],
            "admin_18_delete_student_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 教师管理模块 ====================
    
    def test_teacher_01_get_list(self):
        """测试用例6: 获取教师列表"""
        self.run_api_test(
            6, "获取教师列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/', '|', 'jq'],
            "admin_06_get_teachers.json",
            self.test_setup
        )
    
    def test_teacher_02_create(self):
        """测试用例7: 创建教师"""
        self.run_api_test(
            7, "创建教师",
            ['curl', '-s', '-X', 'POST', f'{self.base_url}/api/admin/teachers/',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 9999, "teacher_name": "李老师", "subject_id": 1, "password": "pass123"}',
             '|', 'jq'],
            "admin_07_create_teacher.json",
            self.test_setup
        )
    
    def test_teacher_03_get_specific(self):
        """测试用例19: 获取特定教师"""
        self.run_api_test(
            19, "获取特定教师",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/1', '|', 'jq'],
            "admin_19_get_teacher.json",
            self.test_setup
        )
    
    def test_teacher_04_update(self):
        """测试用例20: 更新教师信息"""
        self.run_api_test(
            20, "更新教师信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teachers/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "更新的教师姓名"}',
             '|', 'jq'],
            "admin_20_update_teacher.json",
            self.test_setup
        )
    
    def test_teacher_05_delete(self):
        """测试用例21: 删除教师"""
        self.run_api_test(
            21, "删除教师",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teachers/1', '|', 'jq'],
            "admin_21_delete_teacher.json",
            self.test_setup
        )
    
    def test_teacher_06_get_not_found(self):
        """测试用例34: 获取不存在的教师"""
        self.run_api_test(
            34, "获取不存在的教师",
            ['curl', '-s', f'{self.base_url}/api/admin/teachers/9999', '|', 'jq'],
            "admin_34_get_teacher_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_07_update_not_found(self):
        """测试用例35: 更新不存在的教师"""
        self.run_api_test(
            35, "更新不存在的教师",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teachers/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_name": "不存在的教师"}',
             '|', 'jq'],
            "admin_35_update_teacher_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_08_delete_not_found(self):
        """测试用例36: 删除不存在的教师"""
        self.run_api_test(
            36, "删除不存在的教师",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teachers/9999', '|', 'jq'],
            "admin_36_delete_teacher_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 班级管理模块 ====================
    
    def test_class_01_get_list(self):
        """测试用例8: 获取班级列表"""
        self.run_api_test(
            8, "获取班级列表",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/', '|', 'jq'],
            "admin_08_get_classes.json",
            self.test_setup
        )
    
    def test_class_02_create(self):
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
    
    def test_class_03_get_specific(self):
        """测试用例22: 获取特定班级"""
        self.run_api_test(
            22, "获取特定班级",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/1', '|', 'jq'],
            "admin_22_get_class.json",
            self.test_setup
        )
    
    def test_class_04_update(self):
        """测试用例23: 更新班级信息"""
        self.run_api_test(
            23, "更新班级信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/classes/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "更新的班级名称"}',
             '|', 'jq'],
            "admin_23_update_class.json",
            self.test_setup
        )
    
    def test_class_05_delete(self):
        """测试用例24: 删除班级"""
        self.run_api_test(
            24, "删除班级",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/classes/1', '|', 'jq'],
            "admin_24_delete_class.json",
            self.test_setup
        )
    
    def test_class_06_get_not_found(self):
        """测试用例37: 获取不存在的班级"""
        self.run_api_test(
            37, "获取不存在的班级",
            ['curl', '-s', f'{self.base_url}/api/admin/classes/9999', '|', 'jq'],
            "admin_37_get_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_class_07_update_not_found(self):
        """测试用例38: 更新不存在的班级"""
        self.run_api_test(
            38, "更新不存在的班级",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/classes/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_name": "不存在的班级"}',
             '|', 'jq'],
            "admin_38_update_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_class_08_delete_not_found(self):
        """测试用例39: 删除不存在的班级"""
        self.run_api_test(
            39, "删除不存在的班级",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/classes/9999', '|', 'jq'],
            "admin_39_delete_class_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 科目管理模块 ====================
    
    def test_subject_01_get_list(self):
        """测试用例10: 获取科目列表"""
        self.run_api_test(
            10, "获取科目列表",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/', '|', 'jq'],
            "admin_10_get_subjects.json",
            self.test_setup
        )
    
    def test_subject_02_create(self):
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
    
    def test_subject_03_get_specific(self):
        """测试用例25: 获取特定科目"""
        self.run_api_test(
            25, "获取特定科目",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/1', '|', 'jq'],
            "admin_25_get_subject.json",
            self.test_setup
        )
    
    def test_subject_04_update(self):
        """测试用例26: 更新科目信息"""
        self.run_api_test(
            26, "更新科目信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/subjects/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "更新的科目名称"}',
             '|', 'jq'],
            "admin_26_update_subject.json",
            self.test_setup
        )
    
    def test_subject_05_delete(self):
        """测试用例27: 删除科目"""
        self.run_api_test(
            27, "删除科目",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/subjects/1', '|', 'jq'],
            "admin_27_delete_subject.json",
            self.test_setup
        )
    
    def test_subject_06_get_not_found(self):
        """测试用例40: 获取不存在的科目"""
        self.run_api_test(
            40, "获取不存在的科目",
            ['curl', '-s', f'{self.base_url}/api/admin/subjects/9999', '|', 'jq'],
            "admin_40_get_subject_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_subject_07_update_not_found(self):
        """测试用例41: 更新不存在的科目"""
        self.run_api_test(
            41, "更新不存在的科目",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/subjects/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"subject_name": "不存在的科目"}',
             '|', 'jq'],
            "admin_41_update_subject_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_subject_08_delete_not_found(self):
        """测试用例42: 删除不存在的科目"""
        self.run_api_test(
            42, "删除不存在的科目",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/subjects/9999', '|', 'jq'],
            "admin_42_delete_subject_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 考试类型管理模块 ====================
    
    def test_exam_type_01_get_list(self):
        """测试用例12: 获取考试类型列表"""
        self.run_api_test(
            12, "获取考试类型列表",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/', '|', 'jq'],
            "admin_12_get_exam_types.json",
            self.test_setup
        )
    
    def test_exam_type_02_create(self):
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
    
    def test_exam_type_03_get_specific(self):
        """测试用例28: 获取特定考试类型"""
        self.run_api_test(
            28, "获取特定考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/1', '|', 'jq'],
            "admin_28_get_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_04_update(self):
        """测试用例29: 更新考试类型信息"""
        self.run_api_test(
            29, "更新考试类型信息",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam_types/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "更新的考试类型"}',
             '|', 'jq'],
            "admin_29_update_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_05_delete(self):
        """测试用例30: 删除考试类型"""
        self.run_api_test(
            30, "删除考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam_types/1', '|', 'jq'],
            "admin_30_delete_exam_type.json",
            self.test_setup
        )
    
    def test_exam_type_06_get_not_found(self):
        """测试用例43: 获取不存在的考试类型"""
        self.run_api_test(
            43, "获取不存在的考试类型",
            ['curl', '-s', f'{self.base_url}/api/admin/exam_types/9999', '|', 'jq'],
            "admin_43_get_exam_type_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_exam_type_07_update_not_found(self):
        """测试用例44: 更新不存在的考试类型"""
        self.run_api_test(
            44, "更新不存在的考试类型",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/exam_types/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"exam_type_name": "不存在的考试类型"}',
             '|', 'jq'],
            "admin_44_update_exam_type_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_exam_type_08_delete_not_found(self):
        """测试用例45: 删除不存在的考试类型"""
        self.run_api_test(
            45, "删除不存在的考试类型",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/exam_types/9999', '|', 'jq'],
            "admin_45_delete_exam_type_not_found.json",
            self.test_setup,
            expect_error=True
        )

    # ==================== 教师班级关联管理模块 ====================
    
    def test_teacher_class_01_get_list(self):
        """测试用例14: 获取教师班级关联列表"""
        self.run_api_test(
            14, "获取教师班级关联列表",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/', '|', 'jq'],
            "admin_14_get_teacher_classes.json",
            self.test_setup
        )
    
    def test_teacher_class_02_create(self):
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
    
    def test_teacher_class_03_get_specific(self):
        """测试用例31: 获取特定教师班级关联"""
        self.run_api_test(
            31, "获取特定教师班级关联",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/1', '|', 'jq'],
            "admin_31_get_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_04_update(self):
        """测试用例32: 更新教师班级关联"""
        self.run_api_test(
            32, "更新教师班级关联",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teacher_classes/1',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 2, "class_id": 2}',
             '|', 'jq'],
            "admin_32_update_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_05_delete(self):
        """测试用例33: 删除教师班级关联"""
        self.run_api_test(
            33, "删除教师班级关联",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teacher_classes/1', 
             '-H', 'Content-Type: application/json',
             '-d', '{"class_id": 1}',
             '|', 'jq'],
            "admin_33_delete_teacher_class.json",
            self.test_setup
        )
    
    def test_teacher_class_06_get_not_found(self):
        """测试用例46: 获取不存在的教师班级关联"""
        self.run_api_test(
            46, "获取不存在的教师班级关联",
            ['curl', '-s', f'{self.base_url}/api/admin/teacher_classes/9999', '|', 'jq'],
            "admin_46_get_teacher_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_class_07_update_not_found(self):
        """测试用例47: 更新不存在的教师班级关联"""
        self.run_api_test(
            47, "更新不存在的教师班级关联",
            ['curl', '-s', '-X', 'PUT', f'{self.base_url}/api/admin/teacher_classes/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"teacher_id": 9999, "class_id": 9999}',
             '|', 'jq'],
            "admin_47_update_teacher_class_not_found.json",
            self.test_setup,
            expect_error=True
        )
    
    def test_teacher_class_08_delete_not_found(self):
        """测试用例48: 删除不存在的教师班级关联"""
        self.run_api_test(
            48, "删除不存在的教师班级关联",
            ['curl', '-s', '-X', 'DELETE', f'{self.base_url}/api/admin/teacher_classes/9999',
             '-H', 'Content-Type: application/json',
             '-d', '{"class_id": 9999}',
             '|', 'jq'],
            "admin_48_delete_teacher_class_not_found.json",
            self.test_setup,
            expect_error=True
        )