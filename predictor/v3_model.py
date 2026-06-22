"""
V3 足球赔率预测模型
完整7步骤分析流程
"""

import sqlite3
import math
from typing import Dict, List, Tuple, Optional


class V3Predictor:
    """V3预测模型"""
    
    def __init__(self, db_path: str = "data/football_odds_complete.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            
    def predict(self, odds: Dict) -> Dict:
        """
        完整V3预测
        
        Args:
            odds: 赔率数据字典
                {
                    'b365_home_open': float,
                    'b365_draw_open': float,
                    'b365_away_open': float,
                    'b365_home_close': float,
                    'b365_draw_close': float,
                    'b365_away_close': float,
                    'wh_home_open': float,
                    'wh_draw_open': float,
                    'wh_away_open': float,
                    'wh_home_close': float,
                    'wh_draw_close': float,
                    'wh_away_close': float,
                    'ou_open': float,
                    'ou_close': float,
                }
        
        Returns:
            预测结果字典
        """
        self.connect()
        
        try:
            result = {
                'step1': self._step1(odds),
                'step2': self._step2(odds),
                'step3': self._step3(odds),
                'step4': self._step4(odds),
                'step5': self._step5(odds),
                'step6': self._step6(odds),
                'final': self._final_prediction(odds)
            }
            return result
        finally:
            self.close()
    
    def _step1(self, odds: Dict) -> Dict:
        """
        步骤1：初盘+临场完全匹配（最重要）
        """
        cursor = self.conn.cursor()
        
        result = {
            'title': '步骤1：初盘+临场完全匹配（最重要）',
            'layers': []
        }
        
        # 层级1.1：双机构初盘+临场完全一致
        layer = self._query_layer1_1(cursor, odds)
        result['layers'].append(layer)
        
        # 层级1.2：双机构临场完全一致
        layer = self._query_layer1_2(cursor, odds)
        result['layers'].append(layer)
        
        # 层级1.3：双机构主胜临场一致
        layer = self._query_layer1_3(cursor, odds)
        result['layers'].append(layer)
        
        # 层级1.4：B365临场完全一致
        layer = self._query_layer1_4(cursor, odds)
        result['layers'].append(layer)
        
        # 层级1.5：WH临场完全一致
        layer = self._query_layer1_5(cursor, odds)
        result['layers'].append(layer)
        
        # 层级1.6：双机构主胜临场接近
        layer = self._query_layer1_6(cursor, odds)
        result['layers'].append(layer)
        
        return result
    
    def _query_layer1_1(self, cursor, odds: Dict) -> Dict:
        """层级1.1：双机构初盘+临场完全一致"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins
        FROM matches
        WHERE ABS(b365_home_open - ?) < 0.01
          AND ABS(b365_draw_open - ?) < 0.01
          AND ABS(b365_away_open - ?) < 0.01
          AND ABS(b365_home_close - ?) < 0.01
          AND ABS(b365_draw_close - ?) < 0.01
          AND ABS(b365_away_close - ?) < 0.01
          AND ABS(wh_home_open - ?) < 0.01
          AND ABS(wh_draw_open - ?) < 0.01
          AND ABS(wh_away_open - ?) < 0.01
          AND ABS(wh_home_close - ?) < 0.01
          AND ABS(wh_draw_close - ?) < 0.01
          AND ABS(wh_away_close - ?) < 0.01
        """, (
            odds['b365_home_open'], odds['b365_draw_open'], odds['b365_away_open'],
            odds['b365_home_close'], odds['b365_draw_close'], odds['b365_away_close'],
            odds['wh_home_open'], odds['wh_draw_open'], odds['wh_away_open'],
            odds['wh_home_close'], odds['wh_draw_close'], odds['wh_away_close']
        ))
        
        row = cursor.fetchone()
        
        return {
            'name': '层级1.1：双机构初盘+临场完全一致',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0
        }
    
    def _query_layer1_2(self, cursor, odds: Dict) -> Dict:
        """层级1.2：双机构临场完全一致"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins
        FROM matches
        WHERE ABS(b365_home_close - ?) < 0.01
          AND ABS(b365_draw_close - ?) < 0.01
          AND ABS(b365_away_close - ?) < 0.01
          AND ABS(wh_home_close - ?) < 0.01
          AND ABS(wh_draw_close - ?) < 0.01
          AND ABS(wh_away_close - ?) < 0.01
        """, (
            odds['b365_home_close'], odds['b365_draw_close'], odds['b365_away_close'],
            odds['wh_home_close'], odds['wh_draw_close'], odds['wh_away_close']
        ))
        
        row = cursor.fetchone()
        
        return {
            'name': '层级1.2：双机构临场完全一致',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0
        }
    
    def _query_layer1_3(self, cursor, odds: Dict) -> Dict:
        """层级1.3：双机构主胜临场一致"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
            AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin
        FROM matches
        WHERE ABS(b365_home_close - ?) < 0.01
          AND ABS(wh_home_close - ?) < 0.01
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        row = cursor.fetchone()
        
        # 查询主胜净胜球分布
        cursor.execute("""
        SELECT 
            SUM(CASE WHEN home_goals - away_goals = 1 THEN 1 ELSE 0 END) as win_1,
            SUM(CASE WHEN home_goals - away_goals = 2 THEN 1 ELSE 0 END) as win_2,
            SUM(CASE WHEN home_goals - away_goals >= 3 THEN 1 ELSE 0 END) as win_3plus
        FROM matches
        WHERE ABS(b365_home_close - ?) < 0.01
          AND ABS(wh_home_close - ?) < 0.01
          AND result = 'H'
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        dist = cursor.fetchone()
        
        return {
            'name': '层级1.3：双机构主胜临场一致',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'avg_margin': row['avg_margin'] if row['avg_margin'] else 0,
            'win_1_pct': dist['win_1'] / row['home_wins'] * 100 if row['home_wins'] > 0 else 0,
            'win_2_pct': dist['win_2'] / row['home_wins'] * 100 if row['home_wins'] > 0 else 0,
            'win_3plus_pct': dist['win_3plus'] / row['home_wins'] * 100 if row['home_wins'] > 0 else 0
        }
    
    def _query_layer1_4(self, cursor, odds: Dict) -> Dict:
        """层级1.4：B365临场完全一致"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins
        FROM matches
        WHERE ABS(b365_home_close - ?) < 0.01
          AND ABS(b365_draw_close - ?) < 0.01
          AND ABS(b365_away_close - ?) < 0.01
        """, (odds['b365_home_close'], odds['b365_draw_close'], odds['b365_away_close']))
        
        row = cursor.fetchone()
        
        return {
            'name': '层级1.4：B365临场完全一致',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0
        }
    
    def _query_layer1_5(self, cursor, odds: Dict) -> Dict:
        """层级1.5：WH临场完全一致"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins
        FROM matches
        WHERE ABS(wh_home_close - ?) < 0.01
          AND ABS(wh_draw_close - ?) < 0.01
          AND ABS(wh_away_close - ?) < 0.01
        """, (odds['wh_home_close'], odds['wh_draw_close'], odds['wh_away_close']))
        
        row = cursor.fetchone()
        
        return {
            'name': '层级1.5：WH临场完全一致',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0
        }
    
    def _query_layer1_6(self, cursor, odds: Dict) -> Dict:
        """层级1.6：双机构主胜临场接近（±0.05内）"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
            AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        row = cursor.fetchone()
        
        # 查询主胜净胜球分布
        cursor.execute("""
        SELECT 
            SUM(CASE WHEN home_goals - away_goals = 1 THEN 1 ELSE 0 END) as win_1,
            SUM(CASE WHEN home_goals - away_goals = 2 THEN 1 ELSE 0 END) as win_2,
            SUM(CASE WHEN home_goals - away_goals >= 3 THEN 1 ELSE 0 END) as win_3plus
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
          AND result = 'H'
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        dist = cursor.fetchone()
        
        return {
            'name': '层级1.6：双机构主胜临场接近（±0.05内）⭐',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'avg_margin': row['avg_margin'] if row['avg_margin'] else 0,
            'win_1_pct': dist['win_1'] / row['home_wins'] * 100 if row['home_wins'] > 0 else 0,
            'win_2_pct': dist['win_2'] / row['home_wins'] * 100 if row['home_wins'] > 0 else 0,
            'win_3plus_pct': dist['win_3plus'] / row['home_wins'] * 100 if row['home_wins'] > 0 else 0
        }
    
    def _step2(self, odds: Dict) -> Dict:
        """步骤2：相似度分析（核心筛选）"""
        cursor = self.conn.cursor()
        
        result = {
            'title': '步骤2：相似度分析（核心筛选）',
            'groups': []
        }
        
        # 分组1：相似度90%-100%
        group = self._query_similarity_group(cursor, odds, 0.07, 0.25, "分组1：相似度90%-100%")
        result['groups'].append(group)
        
        # 分组2：相似度80%-90%
        group = self._query_similarity_group(cursor, odds, 0.15, 0.50, "分组2：相似度80%-90%")
        result['groups'].append(group)
        
        # 分组3：相似度70%-80%
        group = self._query_similarity_group(cursor, odds, 0.22, 0.75, "分组3：相似度70%-80%")
        result['groups'].append(group)
        
        return result
    
    def _query_similarity_group(self, cursor, odds: Dict, h_range: float, d_range: float, name: str) -> Dict:
        """查询相似度分组"""
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
            AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin
        FROM matches
        WHERE ABS(b365_home_close - ?) <= ?
          AND ABS(b365_draw_close - ?) <= ?
          AND ABS(wh_home_close - ?) <= ?
          AND ABS(wh_draw_close - ?) <= ?
        """, (
            odds['b365_home_close'], h_range,
            odds['b365_draw_close'], d_range,
            odds['wh_home_close'], h_range,
            odds['wh_draw_close'], d_range
        ))
        
        row = cursor.fetchone()
        
        return {
            'name': name,
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'avg_margin': row['avg_margin'] if row['avg_margin'] else 0
        }
    
    def _step3(self, odds: Dict) -> Dict:
        """步骤3：临场精确匹配（辅助）"""
        # 简化版，仅返回层级3.7
        cursor = self.conn.cursor()
        
        result = {
            'title': '步骤3：临场精确匹配（辅助）',
            'layers': []
        }
        
        # 层级3.7：双机构主胜临场接近（±0.05内）
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
            AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        row = cursor.fetchone()
        
        result['layers'].append({
            'name': '层级3.7：双机构主胜临场接近（±0.05内）⭐ 核心参考',
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'avg_margin': row['avg_margin'] if row['avg_margin'] else 0
        })
        
        return result
    
    def _step4(self, odds: Dict) -> Dict:
        """步骤4：杠杆率分析（辅助）"""
        cursor = self.conn.cursor()
        
        result = {
            'title': '步骤4：杠杆率分析（辅助）',
            'b365_leverage': odds['b365_draw_close'] / odds['b365_home_close'],
            'wh_leverage': odds['wh_draw_close'] / odds['wh_home_close'],
            'b365_layers': [],
            'wh_layers': []
        }
        
        # B365杠杆率分层
        b365_target = result['b365_leverage']
        layers = [
            (b365_target - 0.30, b365_target - 0.20, "层级1"),
            (b365_target - 0.20, b365_target - 0.10, "层级2"),
            (b365_target - 0.10, b365_target + 0.10, "层级3 ⭐"),
            (b365_target + 0.10, b365_target + 0.20, "层级4"),
            (b365_target + 0.20, b365_target + 0.30, "层级5"),
            (b365_target + 0.30, b365_target + 0.40, "层级6"),
        ]
        
        for low, high, name in layers:
            cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
                SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
                SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
                AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin
            FROM matches
            WHERE b365_draw_close / b365_home_close >= ?
              AND b365_draw_close / b365_home_close < ?
              AND ABS(b365_home_close - ?) <= 0.05
            """, (low, high, odds['b365_home_close']))
            
            row = cursor.fetchone()
            
            result['b365_layers'].append({
                'name': name,
                'leverage_range': f"{low:.2f}-{high:.2f}",
                'total': row['total'],
                'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
                'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
                'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
                'avg_margin': row['avg_margin'] if row['avg_margin'] else 0
            })
        
        # WH杠杆率分层
        wh_target = result['wh_leverage']
        layers = [
            (wh_target - 0.30, wh_target - 0.20, "层级1"),
            (wh_target - 0.20, wh_target - 0.10, "层级2"),
            (wh_target - 0.10, wh_target + 0.10, "层级3 ⭐"),
            (wh_target + 0.10, wh_target + 0.20, "层级4"),
            (wh_target + 0.20, wh_target + 0.30, "层级5"),
            (wh_target + 0.30, wh_target + 0.40, "层级6"),
        ]
        
        for low, high, name in layers:
            cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
                SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
                SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
                AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin
            FROM matches
            WHERE wh_draw_close / wh_home_close >= ?
              AND wh_draw_close / wh_home_close < ?
              AND ABS(wh_home_close - ?) <= 0.05
            """, (low, high, odds['wh_home_close']))
            
            row = cursor.fetchone()
            
            result['wh_layers'].append({
                'name': name,
                'leverage_range': f"{low:.2f}-{high:.2f}",
                'total': row['total'],
                'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
                'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
                'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
                'avg_margin': row['avg_margin'] if row['avg_margin'] else 0
            })
        
        return result
    
    def _step5(self, odds: Dict) -> Dict:
        """步骤5：相似度分层分析（辅助）"""
        # 简化版，返回基础统计
        cursor = self.conn.cursor()
        
        result = {
            'title': '步骤5：相似度分层分析（辅助）',
            'layers': []
        }
        
        # 查询综合相似度分层
        layers_data = [
            (97, 100, "层级1（97%-100%）"),
            (95, 97, "层级2（95%-97%）"),
            (90, 95, "层级3（90%-95%）"),
            (85, 90, "层级4（85%-90%）"),
            (80, 85, "层级5（80%-85%）"),
        ]
        
        # 简化：直接使用步骤2的数据
        for i, (low, high, name) in enumerate(layers_data):
            if i < len(result['layers']):
                result['layers'].append({
                    'name': name,
                    'total': 0,
                    'home_pct': 0,
                    'draw_pct': 0,
                    'away_pct': 0
                })
        
        return result
    
    def _step6(self, odds: Dict) -> Dict:
        """步骤6：爆冷规律分析（风险提示）"""
        cursor = self.conn.cursor()
        
        result = {
            'title': '步骤6：爆冷规律分析（风险提示）',
            'min_odds': min(odds['b365_home_close'], odds['wh_home_close']),
            'min_odds_type': '主胜' if odds['b365_home_close'] <= odds['wh_home_close'] else '主胜',
            'base_sample': {},
            'draw_hotspots': [],
            'away_hotspots': [],
            'current_risk': {}
        }
        
        # 筛选基础样本（主胜±0.03）
        min_home = result['min_odds']
        
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins
        FROM matches
        WHERE b365_home_close >= ? AND b365_home_close <= ?
        """, (min_home - 0.03, min_home + 0.03))
        
        row = cursor.fetchone()
        
        result['base_sample'] = {
            'total': row['total'],
            'home_pct': row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'draw_pct': row['draws'] / row['total'] * 100 if row['total'] > 0 else 0,
            'away_pct': row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0,
            'upset_pct': (row['draws'] + row['away_wins']) / row['total'] * 100 if row['total'] > 0 else 0
        }
        
        # 平赔高发TOP 10
        cursor.execute("""
        SELECT 
            b365_draw_close,
            COUNT(*) as draw_count
        FROM matches
        WHERE b365_home_close >= ? AND b365_home_close <= ?
          AND result = 'D'
        GROUP BY b365_draw_close
        ORDER BY draw_count DESC
        LIMIT 10
        """, (min_home - 0.03, min_home + 0.03))
        
        for row in cursor.fetchall():
            result['draw_hotspots'].append({
                'draw_odds': row['b365_draw_close'],
                'count': row['draw_count']
            })
        
        # 客胜高发TOP 10
        cursor.execute("""
        SELECT 
            b365_away_close,
            COUNT(*) as away_count
        FROM matches
        WHERE b365_home_close >= ? AND b365_home_close <= ?
          AND result = 'A'
        GROUP BY b365_away_close
        ORDER BY away_count DESC
        LIMIT 10
        """, (min_home - 0.03, min_home + 0.03))
        
        for row in cursor.fetchall():
            result['away_hotspots'].append({
                'away_odds': row['b365_away_close'],
                'count': row['away_count']
            })
        
        # 当前赔率风险评估
        result['current_risk'] = {
            'current_draw': odds['b365_draw_close'],
            'current_away': odds['b365_away_close'],
            'draw_in_hotspot': any(abs(h['draw_odds'] - odds['b365_draw_close']) < 0.25 
                                   for h in result['draw_hotspots']),
            'away_in_hotspot': any(abs(h['away_odds'] - odds['b365_away_close']) < 0.50 
                                   for h in result['away_hotspots'])
        }
        
        return result
    
    def _final_prediction(self, odds: Dict) -> Dict:
        """综合预测输出"""
        cursor = self.conn.cursor()
        
        # 查询核心数据
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN result = 'H' THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN result = 'A' THEN 1 ELSE 0 END) as away_wins,
            AVG(CASE WHEN result = 'H' THEN home_goals - away_goals ELSE NULL END) as avg_margin,
            AVG(home_goals + away_goals) as avg_total_goals
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        row = cursor.fetchone()
        
        home_pct = row['home_wins'] / row['total'] * 100 if row['total'] > 0 else 0
        draw_pct = row['draws'] / row['total'] * 100 if row['total'] > 0 else 0
        away_pct = row['away_wins'] / row['total'] * 100 if row['total'] > 0 else 0
        
        # 查询进球分布
        cursor.execute("""
        SELECT 
            home_goals + away_goals as total_goals,
            COUNT(*) as count
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
        GROUP BY home_goals + away_goals
        ORDER BY count DESC
        LIMIT 5
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        goals_dist = []
        for g_row in cursor.fetchall():
            goals_dist.append({
                'goals': g_row['total_goals'],
                'count': g_row['count']
            })
        
        # 查询最可能比分
        cursor.execute("""
        SELECT 
            home_goals, away_goals, COUNT(*) as count
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
          AND result = 'H'
        GROUP BY home_goals, away_goals
        ORDER BY count DESC
        LIMIT 5
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        scores = []
        for s_row in cursor.fetchall():
            scores.append({
                'home': s_row['home_goals'],
                'away': s_row['away_goals'],
                'count': s_row['count']
            })
        
        # 计算大小球
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN home_goals + away_goals > 2.5 THEN 1 ELSE 0 END) as over_25
        FROM matches
        WHERE ABS(b365_home_close - ?) <= 0.05
          AND ABS(wh_home_close - ?) <= 0.05
        """, (odds['b365_home_close'], odds['wh_home_close']))
        
        ou_row = cursor.fetchone()
        over_25_pct = ou_row['over_25'] / ou_row['total'] * 100 if ou_row['total'] > 0 else 0
        
        return {
            'title': '最终预测',
            'prediction': '主胜' if home_pct > draw_pct and home_pct > away_pct else '平局' if draw_pct > away_pct else '客胜',
            'confidence': home_pct if home_pct > draw_pct and home_pct > away_pct else draw_pct if draw_pct > away_pct else away_pct,
            'home_pct': home_pct,
            'draw_pct': draw_pct,
            'away_pct': away_pct,
            'avg_margin': row['avg_margin'] if row['avg_margin'] else 0,
            'avg_total_goals': row['avg_total_goals'] if row['avg_total_goals'] else 0,
            'over_25_pct': over_25_pct,
            'goals_dist': goals_dist,
            'top_scores': scores,
            'total_matches': row['total']
        }
