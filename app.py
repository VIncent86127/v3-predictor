"""
V3 足球赔率预测系统 - Flask主应用
"""

from flask import Flask, render_template, request, jsonify
from predictor.v3_model import V3Predictor
import os

app = Flask(__name__)

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'football_odds_complete.db')


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """预测接口"""
    try:
        data = request.json
        
        # 提取赔率数据
        odds = {
            'b365_home_open': float(data.get('b365_home_open', 0)),
            'b365_draw_open': float(data.get('b365_draw_open', 0)),
            'b365_away_open': float(data.get('b365_away_open', 0)),
            'b365_home_close': float(data.get('b365_home_close', 0)),
            'b365_draw_close': float(data.get('b365_draw_close', 0)),
            'b365_away_close': float(data.get('b365_away_close', 0)),
            'wh_home_open': float(data.get('wh_home_open', 0)),
            'wh_draw_open': float(data.get('wh_draw_open', 0)),
            'wh_away_open': float(data.get('wh_away_open', 0)),
            'wh_home_close': float(data.get('wh_home_close', 0)),
            'wh_draw_close': float(data.get('wh_draw_close', 0)),
            'wh_away_close': float(data.get('wh_away_close', 0)),
            'ou_open': float(data.get('ou_open', 2.5)),
            'ou_close': float(data.get('ou_close', 2.5)),
        }
        
        # 创建预测器
        predictor = V3Predictor(DB_PATH)
        
        # 执行预测
        result = predictor.predict(odds)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/matches', methods=['GET'])
def get_matches():
    """获取历史比赛数据"""
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取总场次
        cursor.execute("SELECT COUNT(*) FROM matches")
        total_matches = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total_matches': total_matches
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
