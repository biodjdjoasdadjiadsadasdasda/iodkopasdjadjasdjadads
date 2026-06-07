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

@app.route('/track', methods=['POST'])
def track():
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data['total'] += 1
        data['history'].append({
            "time": datetime.now().isoformat(),
            "ip": request.remote_addr
        })
        # Chỉ giữ 100 record gần nhất
        if len(data['history']) > 100:
            data['history'] = data['history'][-100:]
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    return jsonify({"Total Execute": data['total'], "status": "success"})

@app.route('/stats', methods=['GET'])
def stats():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify({"Total Execute": data['total'], "status": "success"})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Tracking API is running!",
        "endpoints": {
            "/track (POST)": "Increase execution count",
            "/stats (GET)": "View total executions",
            "/dashboard (GET)": "View HTML dashboard"
        }
    })

@app.route('/dashboard', methods=['GET'])
def dashboard():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Script Tracker Dashboard</title>
        <style>
            body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            .container {{ background: white; border-radius: 10px; padding: 30px; max-width: 500px; margin: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }}
            h1 {{ color: #667eea; }}
            .counter {{ font-size: 48px; font-weight: bold; color: #764ba2; margin: 20px 0; }}
            .status {{ color: green; font-weight: bold; }}
            hr {{ margin: 20px 0; }}
            .footer {{ font-size: 12px; color: gray; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Execute check</h1>
            <div class="counter">{data['total']}</div>
            <p>Total Executions</p>
            <p class="status">✅ Status: Active</p>
            <hr>
            <p>Last 5 executions:</p>
            <ul>
    """
    for record in data['history'][-5:]:
        dashboard += f"<li>{record['time']} - IP: {record['ip']}</li>"
    dashboard += f"""
            </ul>
            <div class="footer">Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
