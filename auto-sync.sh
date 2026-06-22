#!/bin/bash
# V3预测系统 - 自动同步脚本
# 每次修改后自动提交并推送到GitHub

PROJECT_DIR="/home/ubuntu/.openclaw/workspace/v3-predictor"
COMMIT_MSG="${1:-Auto update: V3 prediction model}"

cd "$PROJECT_DIR"

# 检查是否有改动
if git diff-index --quiet HEAD --; then
    echo "✅ No changes detected"
    exit 0
fi

# 添加所有改动
git add .

# 提交
git commit -m "$COMMIT_MSG"

# 推送
git push origin main

echo "✅ Changes pushed to GitHub"
echo "🌐 https://github.com/VIncent86127/v3-predictor"