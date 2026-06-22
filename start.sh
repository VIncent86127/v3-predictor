#!/bin/bash

# V3预测系统启动脚本

echo "========================================"
echo "V3预测系统 - 优化版"
echo "========================================"
echo ""

# 检查数据库
DB_PATH="/home/ubuntu/.openclaw/workspace/football_odds_complete.db"
if [ ! -f "$DB_PATH" ]; then
    echo "⚠️  数据库不存在: $DB_PATH"
    echo "请先准备数据库文件"
    exit 1
fi

echo "✅ 数据库路径: $DB_PATH"
echo ""

# 创建软链接
mkdir -p data
ln -sf "$DB_PATH" data/football_odds_complete.db

echo "✅ 数据库链接已创建"
echo ""

# 启动服务
echo "🚀 启动预测服务..."
echo "访问地址: http://localhost:5001"
echo """

cd "$(dirname "$0")"
python3 app.py