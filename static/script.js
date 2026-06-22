/**
 * V3 预测系统 JavaScript
 */

// 预测函数
function predict() {
    // 获取输入数据
    const odds = {
        b365_home_open: document.getElementById('b365_home_open').value,
        b365_draw_open: document.getElementById('b365_draw_open').value,
        b365_away_open: document.getElementById('b365_away_open').value,
        b365_home_close: document.getElementById('b365_home_close').value,
        b365_draw_close: document.getElementById('b365_draw_close').value,
        b365_away_close: document.getElementById('b365_away_close').value,
        wh_home_open: document.getElementById('wh_home_open').value,
        wh_draw_open: document.getElementById('wh_draw_open').value,
        wh_away_open: document.getElementById('wh_away_open').value,
        wh_home_close: document.getElementById('wh_home_close').value,
        wh_draw_close: document.getElementById('wh_draw_close').value,
        wh_away_close: document.getElementById('wh_away_close').value,
        ou_open: document.getElementById('ou_open').value,
        ou_close: document.getElementById('ou_close').value
    };

    // 验证输入
    if (!validateInput(odds)) {
        alert('请填写完整的赔率数据！');
        return;
    }

    // 显示加载动画
    showLoading();

    // 发送预测请求
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(odds)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showResult(data.result);
        } else {
            showError(data.error);
        }
    })
    .catch(error => {
        showError(error.message);
    });
}

// 验证输入
function validateInput(odds) {
    const required = [
        'b365_home_close', 'b365_draw_close', 'b365_away_close',
        'wh_home_close', 'wh_draw_close', 'wh_away_close'
    ];

    for (let field of required) {
        if (!odds[field] || odds[field] <= 0) {
            return false;
        }
    }

    return true;
}

// 显示加载动画
function showLoading() {
    const resultSection = document.getElementById('result-section');
    resultSection.style.display = 'block';
    
    const resultContent = document.getElementById('result-content');
    resultContent.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>正在分析赔率数据...</p>
        </div>
    `;
}

// 显示结果
function showResult(result) {
    const resultContent = document.getElementById('result-content');
    
    let html = `
        <!-- 最终预测 -->
        <div class="final-prediction">
            <h3>🎯 最终预测</h3>
            <div class="confidence">${result.final.confidence.toFixed(1)}%</div>
            <div class="prediction-text">预测结果：${result.final.prediction}</div>
            <div style="margin-top: 15px;">
                基于样本：${result.final.total_matches}场
            </div>
        </div>

        <!-- 胜平负分布 -->
        <div class="result-box">
            <h3>📊 胜平负分布</h3>
            <table>
                <tr>
                    <th>结果</th>
                    <th>概率</th>
                    <th>样本数</th>
                </tr>
                <tr>
                    <td>主胜</td>
                    <td>${result.final.home_pct.toFixed(1)}%</td>
                    <td>${result.final.total_matches}场</td>
                </tr>
                <tr>
                    <td>平局</td>
                    <td>${result.final.draw_pct.toFixed(1)}%</td>
                    <td>-</td>
                </tr>
                <tr>
                    <td>客胜</td>
                    <td>${result.final.away_pct.toFixed(1)}%</td>
                    <td>-</td>
                </tr>
            </table>
        </div>

        <!-- 大小球预测 -->
        <div class="result-box">
            <h3>⚽ 大小球预测</h3>
            <table>
                <tr>
                    <th>盘口</th>
                    <th>概率</th>
                </tr>
                <tr>
                    <td>大2.5球</td>
                    <td>${result.final.over_25_pct.toFixed(1)}%</td>
                </tr>
                <tr>
                    <td>小2.5球</td>
                    <td>${(100 - result.final.over_25_pct).toFixed(1)}%</td>
                </tr>
            </table>
            <p style="margin-top: 10px;">
                平均总进球：${result.final.avg_total_goals.toFixed(2)}球
            </p>
        </div>

        <!-- 推荐比分 -->
        <div class="result-box">
            <h3>🎯 推荐比分（主胜）</h3>
            <table>
                <tr>
                    <th>比分</th>
                    <th>场次</th>
                </tr>
                ${result.final.top_scores.map(score => `
                <tr>
                    <td>${score.home}-${score.away}</td>
                    <td>${score.count}场</td>
                </tr>
                `).join('')}
            </table>
        </div>

        <!-- 步骤1分析 -->
        <div class="result-box">
            <h3>${result.step1.title}</h3>
            <table>
                <tr>
                    <th>层级</th>
                    <th>样本数</th>
                    <th>主胜率</th>
                    <th>平局率</th>
                    <th>客胜率</th>
                </tr>
                ${result.step1.layers.map(layer => `
                <tr>
                    <td>${layer.name}</td>
                    <td>${layer.total}场</td>
                    <td>${layer.home_pct.toFixed(1)}%</td>
                    <td>${layer.draw_pct.toFixed(1)}%</td>
                    <td>${layer.away_pct.toFixed(1)}%</td>
                </tr>
                `).join('')}
            </table>
        </div>

        <!-- 步骤4：杠杆率分析 -->
        <div class="result-box">
            <h3>${result.step4.title}</h3>
            <p style="margin-bottom: 15px;">
                B365杠杆率：${result.step4.b365_leverage.toFixed(2)} | 
                WH杠杆率：${result.step4.wh_leverage.toFixed(2)}
            </p>
            
            <h4 style="margin-bottom: 10px;">B365杠杆率分层：</h4>
            <table>
                <tr>
                    <th>层级</th>
                    <th>杠杆率范围</th>
                    <th>样本数</th>
                    <th>主胜率</th>
                </tr>
                ${result.step4.b365_layers.map(layer => `
                <tr>
                    <td>${layer.name}</td>
                    <td>${layer.leverage_range}</td>
                    <td>${layer.total}场</td>
                    <td>${layer.home_pct.toFixed(1)}%</td>
                </tr>
                `).join('')}
            </table>

            <h4 style="margin-top: 20px; margin-bottom: 10px;">WH杠杆率分层：</h4>
            <table>
                <tr>
                    <th>层级</th>
                    <th>杠杆率范围</th>
                    <th>样本数</th>
                    <th>主胜率</th>
                </tr>
                ${result.step4.wh_layers.map(layer => `
                <tr>
                    <td>${layer.name}</td>
                    <td>${layer.leverage_range}</td>
                    <td>${layer.total}场</td>
                    <td>${layer.home_pct.toFixed(1)}%</td>
                </tr>
                `).join('')}
            </table>
        </div>

        <!-- 步骤6：爆冷风险 -->
        <div class="result-box">
            <h3>${result.step6.title}</h3>
            <p style="margin-bottom: 15px;">
                最小赔率：${result.step6.min_odds_type}（${result.step6.min_odds.toFixed(2)}）
            </p>
            
            <h4 style="margin-bottom: 10px;">基础样本分析：</h4>
            <table>
                <tr>
                    <th>项目</th>
                    <th>数值</th>
                </tr>
                <tr>
                    <td>样本量</td>
                    <td>${result.step6.base_sample.total}场</td>
                </tr>
                <tr>
                    <td>主胜率</td>
                    <td>${result.step6.base_sample.home_pct.toFixed(1)}%</td>
                </tr>
                <tr>
                    <td>爆冷率</td>
                    <td>${result.step6.base_sample.upset_pct.toFixed(1)}%</td>
                </tr>
            </table>

            <h4 style="margin-top: 20px; margin-bottom: 10px;">平赔高发TOP 5：</h4>
            <table>
                <tr>
                    <th>平赔</th>
                    <th>平局场次</th>
                </tr>
                ${result.step6.draw_hotspots.slice(0, 5).map(h => `
                <tr>
                    <td>${h.draw_odds.toFixed(2)}</td>
                    <td>${h.count}场</td>
                </tr>
                `).join('')}
            </table>

            <h4 style="margin-top: 20px; margin-bottom: 10px;">客胜高发TOP 5：</h4>
            <table>
                <tr>
                    <th>客胜</th>
                    <th>客胜场次</th>
                </tr>
                ${result.step6.away_hotspots.slice(0, 5).map(h => `
                <tr>
                    <td>${h.away_odds.toFixed(2)}</td>
                    <td>${h.count}场</td>
                </tr>
                `).join('')}
            </table>
        </div>

        <!-- 风险提示 -->
        <div class="risk-warning">
            <h4>⚠️ 风险提示</h4>
            <ul>
                <li>基础样本爆冷率：${result.step6.base_sample.upset_pct.toFixed(1)}%</li>
                ${result.step6.current_risk.draw_in_hotspot ? '<li style="color: red;">当前平赔在平局高发范围内，平局风险较高</li>' : ''}
                ${result.step6.current_risk.away_in_hotspot ? '<li style="color: red;">当前客胜在客胜高发范围内，客胜风险较高</li>' : ''}
                <li>建议关注临场变化和门将状态</li>
            </ul>
        </div>
    `;

    resultContent.innerHTML = html;
}

// 显示错误
function showError(error) {
    const resultContent = document.getElementById('result-content');
    resultContent.innerHTML = `
        <div class="risk-warning">
            <h4>❌ 错误</h4>
            <p>${error}</p>
        </div>
    `;
}

// 页面加载完成后获取数据统计
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/matches')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`数据库总场次：${data.total_matches}场`);
        }
    });
});