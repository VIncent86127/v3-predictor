#!/bin/bash

# V3预测系统 - GitHub推送脚本

echo "==================================="
echo "V3预测系统 - GitHub推送"
echo "==================================="

# 初始化git仓库
cd v3-predictor
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: V3 Football Odds Prediction System

Features:
- Complete V3 model with 7-step analysis
- Local web interface with Flask
- Support for Bet365 and William Hill odds
- 16000+ historical matches database
- Detailed prediction reports

Tech Stack:
- Python 3 + Flask
- SQLite database
- HTML/CSS/JavaScript
"

# 添加远程仓库
git remote add origin https://github.com/VIncent86127/v3-predictor.git

# 推送到GitHub
git branch -M main
git push -u origin main

echo ""
echo "✅ 推送完成！"
echo "GitHub地址：https://github.com/VIncent86127/v3-predictor"
