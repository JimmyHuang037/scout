#!/bin/bash

# 数据库恢复脚本
# 用法: ./restore_db.sh [备份文件名]
# 如果不指定文件名，则列出备份目录中的所有备份文件供选择

# 设置变量
DB_USER="root"
DB_PASS="Newuser1"
DB_NAME="school_management"
BACKUP_DIR="/home/jimmy/repo/scout/db/backup"

# 检查备份目录是否存在
if [ ! -d "$BACKUP_DIR" ]; then
    echo "错误: 备份目录 $BACKUP_DIR 不存在"
    exit 1
fi

# 如果没有提供参数，则列出可用的备份文件
if [ $# -eq 0 ]; then
    echo "可用的备份文件:"
    BACKUP_FILES=($(ls -t "$BACKUP_DIR"/*.sql 2>/dev/null))
    
    if [ ${#BACKUP_FILES[@]} -eq 0 ]; then
        echo "错误: 备份目录中没有找到 .sql 文件"
        exit 1
    fi
    
    echo "0) 取消"
    for i in "${!BACKUP_FILES[@]}"; do
        FILENAME=$(basename "${BACKUP_FILES[$i]}")
        FILESIZE=$(ls -lh "${BACKUP_FILES[$i]}" | awk '{print $5}')
        echo "$((i+1))) $FILENAME (大小: $FILESIZE)"
    done
    
    echo ""
    read -p "请选择要恢复的备份文件编号: " CHOICE
    
    if [ "$CHOICE" -eq 0 ]; then
        echo "操作已取消"
        exit 0
    elif [ "$CHOICE" -gt 0 ] && [ "$CHOICE" -le ${#BACKUP_FILES[@]} ]; then
        BACKUP_FILE="${BACKUP_FILES[$((CHOICE-1))]}"
    else
        echo "无效的选择"
        exit 1
    fi
else
    # 使用提供的文件名
    BACKUP_FILE="$BACKUP_DIR/$1"
    
    # 检查指定的备份文件是否存在
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "错误: 备份文件 $BACKUP_FILE 不存在"
        exit 1
    fi
fi

# 显示将要恢复的文件信息
FILENAME=$(basename "$BACKUP_FILE")
FILESIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')
FILELINES=$(wc -l < "$BACKUP_FILE")
echo ""
echo "将要恢复的备份文件信息:"
echo "文件名: $FILENAME"
echo "文件大小: $FILESIZE"
echo "行数: $FILELINES"
echo ""

# 确认操作
read -p "确定要恢复这个备份吗？这将覆盖当前数据库中的所有数据！(y/N): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "操作已取消"
    exit 0
fi

# 执行恢复
echo "正在恢复数据库 $DB_NAME..."
echo "请稍候..."

# 检查 MySQL 连接
mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_NAME';" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "错误: 无法连接到 MySQL 服务器"
    exit 1
fi



# 执行恢复操作
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$BACKUP_FILE"

# 检查恢复是否成功
if [ $? -eq 0 ]; then
    echo "数据库恢复成功完成!"
    
    # 显示恢复后的数据库记录数
    echo ""
    echo "恢复后的数据库记录数:"
    mysql -u "$DB_USER" -p"$DB_PASS" -e "
        USE $DB_NAME;
        SELECT 'Classes' AS 'Table', COUNT(*) AS 'Record Count' FROM Classes
        UNION ALL
        SELECT 'ExamTypes' AS 'Table', COUNT(*) AS 'Record Count' FROM ExamTypes
        UNION ALL
        SELECT 'Scores' AS 'Table', COUNT(*) AS 'Record Count' FROM Scores
        UNION ALL
        SELECT 'Students' AS 'Table', COUNT(*) AS 'Record Count' FROM Students
        UNION ALL
        SELECT 'Subjects' AS 'Table', COUNT(*) AS 'Record Count' FROM Subjects
        UNION ALL
        SELECT 'TeacherClasses' AS 'Table', COUNT(*) AS 'Record Count' FROM TeacherClasses
        UNION ALL
        SELECT 'Teachers' AS 'Table', COUNT(*) AS 'Record Count' FROM Teachers
        ORDER BY 'Table';
    " 2>/dev/null | column -t
else
    echo "数据库恢复失败!"
    exit 1
fi