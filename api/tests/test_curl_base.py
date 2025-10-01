import json
import os
import subprocess
import sys
import time
import pytest
import shlex
from config import Config
class CurlTestBase:
    @classmethod
    def setup_class(cls):
        """测试类级别的设置"""
        cls.base_url = f"http://{Config.HOST}:{Config.PORT}"
        cls.curl_commands_file = os.path.join(Config.TEST_DIR, "curl_commands.log")
        
        # 确保测试结果目录存在
        os.makedirs(Config.TEST_DIR, exist_ok=True)

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
                error_msg = json_data.get('message', '未知错误')
                if expect_error:
                    print(f"测试 {test_number} 成功（预期错误）: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    return True
                else:
                    print(f"测试 {test_number} 失败: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    pytest.fail(error_msg, pytrace=False)
            elif not json_data.get('success', False):
                error_msg = json_data.get('message', '未知错误')
                if expect_error:
                    print(f"测试 {test_number} 成功（预期错误）: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    return True
                else:
                    print(f"测试 {test_number} 失败: {error_msg}")
                    sys.stdout.flush()  # 确保输出被立即刷新
                    pytest.fail(error_msg, pytrace=False)
            else:
                print(f"测试 {test_number} 成功")
                sys.stdout.flush()  # 确保输出被立即刷新
                return True
        except json.JSONDecodeError:
            # 如果不是JSON格式，直接保存原始输出
            with open(output_path, 'w') as f:
                f.write(result.stdout)
            
            if expect_error:
                print(f"测试 {test_number} 成功（预期错误，非JSON响应）")
                sys.stdout.flush()  # 确保输出被立即刷新
                return True
            else:
                print(f"测试 {test_number} 失败（非JSON响应）")
                sys.stdout.flush()  # 确保输出被立即刷新
                pytest.fail("非JSON响应", pytrace=False)
        except Exception as e:
            print(f"测试 {test_number} 异常: {str(e)}")
            sys.stdout.flush()  # 确保输出被立即刷新
            pytest.fail(str(e), pytrace=False)