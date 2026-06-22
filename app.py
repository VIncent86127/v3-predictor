"""
V3预测系统 - Flask应用（优化版）
支持杠杆率预警、双机构一致性评级
"""

from flask import Flask, render_template, request, jsonify
from predictor.v3_model_optimized import V3PredictorOptimized
import os

app = Flask(__name__)

# 初始化预测器
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'football_odds_complete.db')
predictor = V3PredictorOptimized(DB_PATH)


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """预测接口"""
    try:
        # 获取赔率数据
        data = request.json
        
        odds = {
            'b365_home_open': float(data['b365_home_open']),
            'b365_draw_open': float(data['b365_draw_open']),
            'b365_away_open': float(data['b365_away_open']),
            'b365_home_close': float(data['b365_home_close']),
            'b365_draw_close': float(data['b365_draw_close']),
            'b365_away_close': float(data['b365_away_close']),
            'wh_home_open': float(data['wh_home_open']),
            'wh_draw_open': float(data['wh_draw_open']),
            'wh_away_open': float(data['wh_away_open']),
            'wh_home_close': float(data['wh_home_close']),
            'wh_draw_close': float(data['wh_draw_close']),
            'wh_away_close': float(data['wh_away_close']),
            'ou_open': float(data.get('ou_open', 2.5)),
            'ou_close': float(data.get('ou_close', 2.5))
        }
        
        # 运行预测
        result = predictor.predict(odds)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    print("=" * 60)
    print("V3预测系统启动（优化版）")
    print("=" * 60)
    print("访问地址: http://localhost:5000")
    print("数据库路径:", DB_PATH)
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
