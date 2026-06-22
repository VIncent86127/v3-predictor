# V3 预测系统 - 部署指南

## 步骤1：创建GitHub仓库

1. 登录GitHub：https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写信息：
   - Repository name: `v3-predictor`
   - Description: `V3 Football Odds Prediction System`
   - 选择 Public 或 Private
   - **不要勾选** "Initialize this repository with a README"
4. 点击 "Create repository"

## 步骤2：推送代码到GitHub

创建仓库后，在本地执行：

```bash
cd /home/ubuntu/.openclaw/workspace/v3-predictor

# 添加远程仓库
git remote add origin https://github.com/VIncent86127/v3-predictor.git

# 推送代码
git push -u origin main
```

或者使用SSH：

```bash
git remote add origin git@github.com:VIncent86127/v3-predictor.git
git push -u origin main
```

## 步骤3：本地运行

### 方式1：直接运行

```bash
cd v3-predictor
pip install -r requirements.txt
python app.py
```

访问：http://localhost:5000

### 方式2：使用虚拟环境

```bash
cd v3-predictor
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

## 步骤4：使用方法

1. 打开浏览器访问 http://localhost:5000
2. 输入赔率数据：
   - Bet365初盘和临场赔率
   - William Hill初盘和临场赔率
   - 大小球盘口
3. 点击"开始预测"
4. 查看完整的V3分析报告

## 项目结构

```
v3-predictor/
├── app.py                  # Flask主应用
├── requirements.txt        # Python依赖
├── predictor/
│   └── v3_model.py        # V3模型核心代码
├── templates/
│   └── index.html         # 网页模板
├── static/
│   ├── style.css          # 样式文件
│   └── script.js          # JavaScript脚本
├── data/
│   └── football_odds_complete.db  # 历史数据库
└── README.md              # 项目说明
```

## 注意事项

1. **数据库文件**：数据库文件4.1MB已包含在项目中
2. **Python版本**：需要Python 3.7+
3. **端口**：默认使用5000端口，可在app.py中修改
4. **数据来源**：五大联赛历史赔率数据

## 故障排除

### 问题1：端口被占用

修改app.py最后一行：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为其他端口
```

### 问题2：数据库找不到

检查数据库路径：
```python
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'football_odds_complete.db')
```

### 问题3：依赖安装失败

升级pip：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 联系方式

- GitHub: https://github.com/VIncent86127
- Email: vincent86127@gmail.com
