#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import os
import sys
import shlex
from config.config import TestingConfig


class CurlTestBase:
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        cls.base_url = f"http://127.0.0.1:{TestingConfig.PORT}"
        cls.curl_commands_file = getattr(TestingConfig, 'CURL_TEST_DIR', '/tmp') + "/curl_commands.log"
        
        # 确保测试结果目录存在
        test_results_dir = getattr(TestingConfig, 'CURL_TEST_DIR', '/tmp')
        os.makedirs(test_results_dir, exist_ok=True)

    def login_admin(self, base_url, cookie_file):
        """管理员登录"""
        print("登录管理员账户...")
        sys.stdout.flush()  # 确保输出被立即刷新
        login_url = f"{base_url}/api/auth/login"
        login_data = {
            "user_id": "admin",
            "password": "admin"
        }
        
        # 构建curl命令
        curl_cmd = [
            "curl", "-s", "-X", "POST", login_url,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(login_data),
            "-c", cookie_file
        ]
        
        # 记录curl命令
        with open(self.curl_commands_file, 'a') as f:
            f.write(f"Login command: {' '.join(curl_cmd)}\n")
        
        try:
            # 执行curl命令
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
            
            # 打印登录结果
            print(f"登录结果: returncode={result.returncode}, stdout={result.stdout}, stderr={result.stderr}")
            sys.stdout.flush()  # 确保输出被立即刷新
            
            if result.returncode == 0:
                try:
                    response_data = json.loads(result.stdout)
                    if response_data.get("success"):
                        print("管理员登录成功")
                        sys.stdout.flush()  # 确保输出被立即刷新
                        return True
                    else:
                        print(f"管理员登录失败: {response_data.get('message', 'Unknown error')}")
                        sys.stdout.flush()  # 确保输出被立即刷新
                        return False
                except json.JSONDecodeError:
                    print(f"管理员登录失败，非JSON响应: {result.stdout}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    return False
            else:
                print(f"管理员登录失败，curl执行错误: {result.stderr}")
                sys.stdout.flush()  # 确保输出被立即刷新
                return False
        except subprocess.TimeoutExpired:
            print("管理员登录超时")
            sys.stdout.flush()  # 确保输出被立即刷新
            return False
        except Exception as e:
            print(f"管理员登录异常: {str(e)}")
            sys.stdout.flush()  # 确保输出被立即刷新
            return False

    def logout(self, base_url, cookie_file):
        """登出"""
        print("登出账户...")
        sys.stdout.flush()  # 确保输出被立即刷新
        logout_url = f"{base_url}/api/auth/logout"
        
        curl_cmd = [
            "curl", "-s", "-X", "POST", logout_url,
            "-b", cookie_file
        ]
        
        # 记录curl命令
        with open(self.curl_commands_file, 'a') as f:
            f.write(f"Logout command: {' '.join(curl_cmd)}\n")
        
        try:
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
            print(f"登出结果: {result.stdout}")
            sys.stdout.flush()  # 确保输出被立即刷新
            return result.returncode == 0
        except Exception as e:
            print(f"登出异常: {str(e)}")
            sys.stdout.flush()  # 确保输出被立即刷新
            return False

    def _record_curl_command(self, test_number, description, command):
        """记录curl命令到文件"""
        with open(self.curl_commands_file, 'a') as f:
            f.write(f"Test {test_number}: {' '.join(command)}\n")

    def run_api_test(self, test_number, description, command, output_file, test_setup, expect_error=False):
        """运行单个API测试"""
        print(f"\n{test_number}. {description}")
        print(f"执行命令: {' '.join(command)}")
        sys.stdout.flush()  # 确保输出被立即刷新

        # 记录curl命令
        self._record_curl_command(test_number, description, command)

        # 使用shlex.join来正确处理命令参数中的引号
        if '|' not in ' '.join(command):
            # 如果命令中没有管道符，添加jq处理
            full_command = shlex.join(command) + ' | jq'
        else:
            # 如果已经有管道符，直接使用原命令
            full_command = shlex.join(command)

        # 执行测试命令
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        # 保存结果
        output_path = os.path.join(test_setup['result_dir'], output_file)
        try:
            # 尝试解析为JSON
            json_data = json.loads(result.stdout)
            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            # 如果API返回错误
            if 'error' in json_data and json_data['error']:
                error_msg = f"API返回错误 - {json_data['error']}"
                if expect_error:
                    print(f"测试 {test_number} 完成（预期错误）: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    return True
                else:
                    print(f"测试 {test_number} 失败: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    assert False, f"测试 {test_number} 失败: {error_msg}"
            elif not json_data.get('success', False):
                error_msg = json_data.get('message', '未知错误')
                if expect_error:
                    print(f"测试 {test_number} 完成（预期错误）: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    return True
                else:
                    print(f"测试 {test_number} 失败: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    assert False, f"测试 {test_number} 失败: {error_msg}"
            else:
                print(f"测试 {test_number} 完成")
                sys.stdout.flush()  # 确保输出被立即刷新
                return True

        except json.JSONDecodeError:
            # 如果不是JSON响应，直接保存
            with open(output_path, 'w') as f:
                f.write(result.stdout)
            
            # 检查是否有错误输出
            if result.returncode != 0 or result.stderr:
                error_msg = result.stderr or "命令执行失败"
                print(f"测试 {test_number} 失败: {error_msg}")
                sys.stdout.flush()  # 确保输出被立即刷新
                assert False, f"测试 {test_number} 失败: {error_msg}"
            else:
                print(f"测试 {test_number} 完成")
                sys.stdout.flush()  # 确保输出被立即刷新
                return True

        except Exception as e:
            print(f"测试 {test_number} 异常: {str(e)}")
            sys.stdout.flush()  # 确保输出被立即刷新
            assert False, f"测试 {test_number} 异常: {str(e)}"