#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
"""
import requests
import json

def test_teacher_login_and_scores():
    # 基础URL
    base_url = 'http://localhost:5000'
    
    # 创建会话
    session = requests.Session()
    
    # 登录教师账户
    login_data = {
        'user_id': '1',
        'password': 'test123'
    }
    
    print('正在登录教师账户...')
    login_response = session.post(f'{base_url}/api/auth/login', data=login_data)
    print(f'登录响应状态码: {login_response.status_code}')
    print(f'登录响应内容: {login_response.text}')
    
    if login_response.status_code != 200:
        print('登录失败')
        return
    
    # 获取成绩列表
    print('\n正在获取成绩列表...')
    scores_response = session.get(f'{base_url}/api/teacher/scores')
    print(f'成绩列表响应状态码: {scores_response.status_code}')
    print(f'成绩列表响应内容: {scores_response.text}')
    
    # 尝试创建新成绩
    print('\n正在创建新成绩...')
    new_score_data = {
        'student_id': 'S0201',
        'subject_id': 1,
        'exam_type_id': 1,
        'score': 85.5
    }
    create_response = session.post(f'{base_url}/api/teacher/scores', json=new_score_data)
    print(f'创建成绩响应状态码: {create_response.status_code}')
    print(f'创建成绩响应内容: {create_response.text}')

if __name__ == '__main__':
    test_teacher_login_and_scores()