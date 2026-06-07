from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'count.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"total": 0}, f)

@app.route('/track', methods=['POST'])
def track():
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data['total'] += 1
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
    return jsonify({"message": "Tracking API is running!", "endpoints": ["/track (POST)", "/stats (GET)"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
