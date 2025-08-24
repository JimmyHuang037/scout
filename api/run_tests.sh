#!/bin/bash
# 测试运行脚本

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 检查是否需要恢复数据库
if [ "$1" == "restore" ] || [ "$2" == "restore" ]; then
    echo "正在恢复测试数据库..."
    cd ../db
    # 使用最新的备份文件自动恢复测试数据库
    ./restore_db.sh school_management_backup_20250823_233411.sql school_management_test << EOF
y
EOF
    cd ../api
    echo "测试数据库恢复完成"
fi

# 运行所有测试
echo "运行所有测试..."
python -m pytest tests/ -v

# 检查是否需要生成覆盖率报告
if [ "$1" == "coverage" ] || [ "$2" == "coverage" ]; then
    echo "运行测试并生成覆盖率报告..."
    python -m pytest tests/ --cov=app --cov=services --cov=blueprints --cov=utils --cov-report=html
fi