# V3预测系统 - 快速启动指南

## 🚀 快速开始

### 方法1：直接运行（推荐）

```bash
cd /home/ubuntu/.openclaw/workspace/v3-predictor
python app.py
```

然后访问：http://localhost:5000

### 方法2：使用数据库真实路径

```bash
cd /home/ubuntu/.openclaw/workspace/v3-predictor
python -c "
from predictor.v3_model_optimized import V3PredictorOptimized
import os

# 使用真实数据库路径
db_path = '/home/ubuntu/.openclaw/workspace/football_odds_complete.db'
predictor = V3PredictorOptimized(db_path)

# 测试赔率
odds = {
    'b365_home_open': 1.67,
    'b365_draw_open': 3.70,
    'b365_away_open': 5.00,
    'b365_home_close': 1.44,
    'b365_draw_close': 4.33,
    'b365_away_close': 7.50,
    'wh_home_open': 1.55,
    'wh_draw_open': 3.80,
    'wh_away_open': 5.50,
    'wh_home_close': 1.44,
    'wh_draw_close': 4.20,
    'wh_away_close': 7.00,
    'ou_open': 2.5,
    'ou_close': 2.5
}

result = predictor.predict(odds)
print('预测结果:', result['final']['prediction'])
print('置信度:', result['final']['confidence'])
print('风险级别:', result['risk_assessment']['risk_level'])
"
```

## 📊 测试案例

### 阿根廷 vs 奥地利（2026-06-23 01:00）

**赔率数据**：
- B365：初盘 1.67/3.70/5.00，临场 1.44/4.33/7.50
- WH：初盘 1.55/3.80/5.50，临场 1.44/4.20/7.00

**预期结果**：
- 预测：主胜
- 置信度：68-70%（调整后）
- 风险级别：low或medium
- 杠杆率：B365 3.01（临界），WH 2.92（安全）

## 🔧 配置说明

### 数据库路径

默认路径：`data/football_odds_complete.db`

如果数据库在其他位置，修改 `app.py`：

```python
DB_PATH = '/your/path/to/football_odds_complete.db'
```

### 端口设置

默认端口：5000

修改端口：

```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## ⚠️ 注意事项

1. **杠杆率预警**
   - 杠杆率≥3.0会自动降级置信度
   - 需要特别关注平局风险

2. **双机构一致性**
   - 完全一致（差异<0.01）会升级置信度
   - 分歧较大（差异>0.05）会降级置信度

3. **样本量**
   - 样本量<10场时，数据可靠性降低
   - 建议样本量≥50场

## 📈 更新日志

### v2.0.0 (2026-06-22)
- 新增杠杆率预警系统
- 新增双机构一致性评级
- 新增风险评估系统
- 自动置信度调整

## 🔗 相关链接

- GitHub: https://github.com/VIncent86127/v3-predictor
- 问题反馈: https://github.com/VIncent86127/v3-predictor/issues