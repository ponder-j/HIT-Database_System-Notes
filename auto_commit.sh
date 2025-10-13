#!/bin/bash

# 切换到项目目录
cd /Users/ponder/Study/数据库系统

# 获取当前时间，格式：2025/10/13 08:31:00
TIMESTAMP=$(date +"%Y/%m/%d %H:%M:%S")

# 添加所有更改
git add .

# 检查是否有更改需要提交
if git diff --cached --quiet; then
    echo "No changes to commit at $TIMESTAMP"
    exit 0
fi

# 提交更改
git commit -m "Auto update at $TIMESTAMP"

# 推送到远程仓库
git push origin main

echo "Successfully committed and pushed at $TIMESTAMP"
