#!/bin/bash

# 数据库备份脚本
# 用法: ./backup_db.sh [备份文件名]

# 设置变量
DB_USER="root"
DB_PASS="Newuser1"
DB_NAME="school_management"
BACKUP_DIR="$(dirname "$0")/backup"

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

# 设置默认备份文件名或使用提供的文件名
if [ $# -eq 0 ]; then
    BACKUP_FILE="$BACKUP_DIR/school_management_backup_$(date +"%Y%m%d_%H%M%S").sql"
else
    BACKUP_FILE="$BACKUP_DIR/$1"
fi

# 执行备份
echo "正在备份数据库 $DB_NAME..."
mysqldump -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE"

# 检查备份是否成功
if [ $? -eq 0 ]; then
    echo "数据库备份成功完成!"
    echo "备份文件: $BACKUP_FILE"
    echo "备份文件大小: $(ls -lh "$BACKUP_FILE" | awk '{print $5}')"
    echo "备份文件行数: $(wc -l < "$BACKUP_FILE") 行"
else
    echo "数据库备份失败!"
    exit 1
fi