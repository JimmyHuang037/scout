#!/usr/bin/env python3
"""
认证工具测试
"""

import pytest
from utils.auth import require_auth, require_role


class TestAuth:
    """认证工具测试类"""

    def test_require_auth_with_no_session(self, app):
        """测试未认证时的权限检查"""
        with app.test_request_context():
            result = require_auth()
            assert result is not None
            assert result[1] == 401

    def test_require_role_with_no_session(self, app):
        """测试无角色信息时的角色检查"""
        with app.test_request_context():
            result = require_role('teacher')
            assert result is not None
            assert result[1] == 401

    def test_require_role_with_wrong_role(self, app):
        """测试角色不匹配时的角色检查"""
        with app.test_request_context() as ctx:
            ctx.session['user_id'] = '1'
            ctx.session['role'] = 'student'
            result = require_role('teacher')
            assert result is not None
            assert result[1] == 403

    def test_require_role_with_correct_role(self, app):
        """测试角色匹配时的角色检查"""
        with app.test_request_context() as ctx:
            ctx.session['user_id'] = '1'
            ctx.session['role'] = 'teacher'
            result = require_role('teacher')
            assert result is None