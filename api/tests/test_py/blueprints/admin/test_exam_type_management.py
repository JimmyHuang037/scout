#!/usr/bin/env python3
"""
管理员考试类型管理测试
"""

import json
import time
import random
import pytest


class TestAdminExamTypeManagement:
    """管理员考试类型管理测试类"""

    def test_get_exam_types(self, admin_client):
        """测试获取考试类型列表"""
        response = admin_client.get('/api/admin/exam-types')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'exam_types' in data['data']
        assert 'pagination' in data['data']

    def test_create_exam_type(self, admin_client):
        """测试创建考试类型"""
        # 使用唯一的时间戳确保测试数据不重复
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        exam_type_data = {
            'exam_type_name': f'Test Exam Type {timestamp}_{random_num}'
        }
        response = admin_client.post('/api/admin/exam-types',
                                     data=json.dumps(exam_type_data),
                                     content_type='application/json')
        # 根据实际实现，创建成功返回201状态码和消息
        assert response.status_code in [200, 201]
        
        # 获取创建的考试类型ID用于后续测试
        created_data = json.loads(response.data)
        if 'data' in created_data and 'exam_type_id' in created_data['data']:
            type_id = created_data['data']['exam_type_id']
        else:
            # 如果响应中没有exam_type_id，则尝试通过名称查找
            get_response = admin_client.get('/api/admin/exam-types')
            exam_types = json.loads(get_response.data)['data']['exam_types']
            type_id = None
            for et in exam_types:
                if et['exam_type_name'] == f'Test Exam Type {timestamp}_{random_num}':
                    type_id = et['exam_type_id']
                    break
        
        # 验证考试类型创建成功
        assert type_id is not None

    def test_get_exam_type(self, admin_client):
        """测试获取单个考试类型信息"""
        # 获取一个已存在的考试类型 (使用ID为1的考试类型)
        response = admin_client.get("/api/admin/exam-types/1")
        # 验证响应
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data

    def test_update_exam_type(self, admin_client):
        """测试更新考试类型"""
        # 准备更新数据
        update_data = {
            'exam_type_name': 'Updated Exam Type'
        }
        # 发送PUT请求更新ID为1的考试类型
        response = admin_client.put("/api/admin/exam-types/1",
                                    data=json.dumps(update_data),
                                    content_type='application/json')
        # 验证响应状态码
        assert response.status_code in [200, 204]

    def test_delete_exam_type(self, admin_client):
        """测试删除考试类型"""
        # 创建一个新的考试类型用于删除测试
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        exam_type_data = {
            'exam_type_name': f'Test Delete Exam Type {timestamp}_{random_num}'
        }
        create_response = admin_client.post('/api/admin/exam-types',
                                            data=json.dumps(exam_type_data),
                                            content_type='application/json')
        assert create_response.status_code in [200, 201]
        
        # 获取创建的考试类型ID
        created_data = json.loads(create_response.data)
        if 'data' in created_data and 'exam_type_id' in created_data['data']:
            type_id = created_data['data']['exam_type_id']
        else:
            # 如果响应中没有exam_type_id，则尝试通过名称查找
            get_response = admin_client.get('/api/admin/exam-types')
            exam_types = json.loads(get_response.data)['data']['exam_types']
            type_id = None
            for et in exam_types:
                if et['exam_type_name'] == f'Test Delete Exam Type {timestamp}_{random_num}':
                    type_id = et['exam_type_id']
                    break
        
        # 删除考试类型
        if type_id:
            delete_response = admin_client.delete(f"/api/admin/exam-types/{type_id}")
            assert delete_response.status_code in [200, 204]

if __name__ == '__main__':
    pytest.main([__file__])