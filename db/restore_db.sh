#!/bin/bash

# 数据库恢复脚本
# 用法: ./restore_db.sh [备份文件名] [数据库名] [--auto] [--latest]
# 如果不指定文件名，则列出备份目录中的所有备份文件供选择
# 如果不指定数据库名，则使用默认数据库名
# 如果添加 --auto 参数，则自动执行恢复操作，无需用户确认
# 如果添加 --latest 参数，则自动选择最新的备份文件

# 设置变量
DB_USER="root"
DB_PASS="Newuser1"
DB_NAME="school_management"
BACKUP_DIR="$(dirname "$0")/backup"
AUTO_MODE=false
LATEST_MODE=false

# 检查参数
for arg in "$@"; do
    if [ "$arg" = "--auto" ]; then
        AUTO_MODE=true
    elif [ "$arg" = "--latest" ]; then
        LATEST_MODE=true
    fi
done

# 如果提供了数据库名参数，则使用它
if [ $# -ge 2 ] && [ "$2" != "--auto" ] && [ "$2" != "--latest" ]; then
    DB_NAME="$2"
elif [ $# -ge 3 ]; then
    # 检查第三个参数
    if [ "$3" != "--auto" ] && [ "$3" != "--latest" ]; then
        DB_NAME="$3"
    elif [ $# -ge 4 ]; then
        # 检查第四个参数
        if [ "$4" != "--auto" ] && [ "$4" != "--latest" ]; then
            DB_NAME="$4"
        fi
    fi
fi

# 检查备份目录是否存在
if [ ! -d "$BACKUP_DIR" ]; then
    echo "错误: 备份目录 $BACKUP_DIR 不存在"
    exit 1
fi

# 如果没有提供文件名参数，但使用了--latest参数，则自动选择最新的备份文件
if [ $# -eq 0 ] || ( [ $# -eq 1 ] && ( [ "$1" = "--auto" ] || [ "$1" = "--latest" ] ) ) || ( [ $# -eq 2 ] && ( [ "$2" = "--auto" ] || [ "$2" = "--latest" ] ) ); then
    if [ "$LATEST_MODE" = true ]; then
        # 自动选择最新的备份文件
        BACKUP_FILES=($(ls -t "$BACKUP_DIR"/*.sql 2>/dev/null))
        
        if [ ${#BACKUP_FILES[@]} -eq 0 ]; then
            echo "错误: 备份目录中没有找到 .sql 文件"
            exit 1
        fi
        
        BACKUP_FILE="${BACKUP_FILES[0]}"
    else
        # 列出可用的备份文件供用户选择
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
    fi
else
    # 使用提供的文件名（排除 --auto 和 --latest 参数）
    PROVIDED_FILE=""
    for arg in "$@"; do
        if [ "$arg" != "--auto" ] && [ "$arg" != "--latest" ]; then
            PROVIDED_FILE="$arg"
            break
        fi
    done
    
    # 如果找到的参数是数据库名而不是文件名，则继续查找文件名
    if [ "$PROVIDED_FILE" = "$DB_NAME" ]; then
        for arg in "$@"; do
            if [ "$arg" != "--auto" ] && [ "$arg" != "--latest" ] && [ "$arg" != "$DB_NAME" ]; then
                PROVIDED_FILE="$arg"
                break
            fi
        done
    fi
    
    if [ -n "$PROVIDED_FILE" ] && [ "$PROVIDED_FILE" != "$DB_NAME" ]; then
        BACKUP_FILE="$BACKUP_DIR/$PROVIDED_FILE"
    elif [ "$LATEST_MODE" = true ]; then
        # 自动选择最新的备份文件
        BACKUP_FILES=($(ls -t "$BACKUP_DIR"/*.sql 2>/dev/null))
        
        if [ ${#BACKUP_FILES[@]} -eq 0 ]; then
            echo "错误: 备份目录中没有找到 .sql 文件"
            exit 1
        fi
        
        BACKUP_FILE="${BACKUP_FILES[0]}"
    else
        # 列出可用的备份文件供用户选择
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
    fi
    
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
echo "目标数据库: $DB_NAME"
echo ""

# 确认操作（除非在自动模式下）
if [ "$AUTO_MODE" = false ]; then
    echo ""
    echo "=== 恢复确认 ==="
    printf "%-20s %s\n" "备份文件:" "$FILENAME"
    printf "%-20s %s\n" "文件大小:" "$FILESIZE"
    printf "%-20s %s\n" "行数:" "$FILELINES"
    printf "%-20s %s\n" "目标数据库:" "$DB_NAME"
    echo "=================="
    read -p "确定要恢复这个备份吗？这将覆盖数据库中的所有数据！(y/N): " CONFIRM

    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo "操作已取消"
        exit 0
    fi
else
    echo "自动模式: 正在恢复数据库 $DB_NAME..."
fi

# 执行恢复
echo "正在恢复数据库 $DB_NAME..."
echo "请稍候..."

# 检查 MySQL 连接
mysql --connect-timeout=5 -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_NAME';" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "错误: 无法连接到 MySQL 服务器或认证失败"
    exit 1
fi

# 检查数据库是否存在，如果不存在则创建
DB_EXISTS=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_NAME';" 2>/dev/null | grep -c "$DB_NAME")
if [ "$DB_EXISTS" -eq 0 ]; then
    echo "数据库 $DB_NAME 不存在，正在创建..."
    mysql -u "$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE $DB_NAME;" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建数据库 $DB_NAME"
        exit 1
    fi
    echo "数据库 $DB_NAME 创建成功"
fi

# 执行恢复操作
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$BACKUP_FILE"

# 检查恢复是否成功
if [ $? -eq 0 ]; then
    echo "数据库恢复成功完成!"
    
    # 显示恢复后的数据库记录数
    echo ""
    echo "恢复后的数据库记录数:"
    TABLE_COUNT_QUERY="
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
    "
    echo "$TABLE_COUNT_QUERY" | mysql -u "$DB_USER" -p"$DB_PASS" 2>/dev/null | column -t
else
    echo "数据库恢复失败!"
    exit 1
fi