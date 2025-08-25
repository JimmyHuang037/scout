#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查是否需要恢复数据库
RESTORE_DB=false
GENERATE_COVERAGE=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        restore)
            RESTORE_DB=true
            shift
            ;;
        coverage)
            GENERATE_COVERAGE=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            echo "用法: $0 [restore] [coverage]"
            echo "  restore   恢复测试数据库"
            echo "  coverage  生成覆盖率报告"
            exit 1
            ;;
    esac
done

# 恢复数据库（如果需要）
if [ "$RESTORE_DB" = true ]; then
    echo "正在恢复测试数据库..."
    cd ../db
    if [ -f "school_management_backup_20250823_233411.sql" ]; then
        ./restore_db.sh school_management_backup_20250823_233411.sql school_management_test
    else
        echo "警告: 备份文件不存在，使用最新备份文件"
        ./restore_db.sh
    fi
    cd "$SCRIPT_DIR"
fi

# 运行测试
if [ "$GENERATE_COVERAGE" = true ]; then
    echo "正在运行测试并生成覆盖率报告..."
    python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term
else
    echo "正在运行测试..."
    python -m pytest tests/ -v
fi

echo "测试完成"