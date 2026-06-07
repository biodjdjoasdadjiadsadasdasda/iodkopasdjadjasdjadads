from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'count.json'

# Khởi tạo file đếm
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"total": 0, "history": []}, f)

# Endpoint để TĂNG số (quan trọng!)
@app.route('/oicaiditnhauxaorau', methods=['POST'])
def track():
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data['total'] += 1
        data['history'].append({
            "time": datetime.now().isoformat(),
            "ip": request.remote_addr
        })
        if len(data['history']) > 100:
            data['history'] = data['history'][-100:]
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    return jsonify({
        "Total Execute": data['total'], 
        "status": "success",
        "by": "kuri"
    })

# Endpoint xem số liệu dạng JSON
@app.route('/kpi', methods=['GET'])
def stats():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify({
        "Total Execute": data['total'], 
        "status": "success",
        "by": "kuri"
    })

# Dashboard đẹp + nút xóa (ẩn danh)
@app.route('/phuonganh', methods=['GET', 'POST'])
def phuonganh():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Xử lý xóa toàn bộ
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'reset':
            with open(DATA_FILE, 'w') as f:
                json.dump({"total": 0, "history": []}, f)
            return '''
            <html>
            <head><title>Reset Complete</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>✅ Đã xóa toàn bộ số liệu!</h1>
                <p>Tổng số execute hiện tại: 0</p>
                <a href="/phuonganh">← Quay lại dashboard</a>
            </body>
            </html>
            '''
    
    # Dashboard HTML
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📊 My girlfriend p.anh</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }}
            h1 {{ color: #667eea; font-size: 2em; }}
            .counter {{
                font-size: 80px;
                font-weight: bold;
                color: #764ba2;
                margin: 20px 0;
                background: #f0f0f0;
                border-radius: 15px;
                padding: 20px;
            }}
            .by {{ color: #ff6b6b; font-style: italic; font-size: 18px; }}
            .status {{ color: green; font-weight: bold; }}
            .reset-btn {{
                background: #dc3545;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 20px;
            }}
            .reset-btn:hover {{ background: #c82333; }}
            .footer {{ font-size: 12px; color: gray; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Script execution check</h1>
            <div class="counter">{data['total']}</div>
            <p>Total Executions</p>
            <p class="status">✅ System Active</p>
            <p class="by">✨ by kuri</p>
            <form method="POST">
                <input type="hidden" name="action" value="reset">
                <button type="submit" class="reset-btn" onclick="return confirm('⚠️ Bạn có chắc muốn XÓA TOÀN BỘ số liệu?')">
                    🗑️ Reset All Data
                </button>
            </form>
            <div class="footer">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
    </body>
    </html>
    """

@app.route('/', methods=['GET'])
def home():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify({
        "message": "Tracking API is running!",
        "endpoints": {
            "ditmemay soi cai del j?",
            "/stats": "View total executions cua hub bo"
        },
        "current_total": data['total'],
        "by": "kuri"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
