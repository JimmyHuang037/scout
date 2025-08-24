#!/bin/bash
# 测试运行脚本

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行所有测试
echo "运行所有测试..."
python -m pytest tests/ -v

# 检查是否提供了参数
if [ "$1" == "coverage" ]; then
    echo "运行测试并生成覆盖率报告..."
    python -m pytest tests/ --cov=app --cov=services --cov=blueprints --cov=utils --cov-report=html
fi