# 此為即將部署到 Railway 的 Flask 後端應用程式 (app.py) 範例程式碼
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import sqlite3

app = Flask(__name__)
CORS(app)

RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '您的_RESEND_API_KEY')
DB_FILE = 'subscribers.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, source TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def send_welcome_email(to_email):
    headers = {
        'Authorization': f'Bearer {RESEND_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "from": "Alex @ SRS Pro <hello@您的網域.com>",
        "to": [to_email],
        "subject": "🚀 您的【SRS Pro】30 字學測動漫單字先鋒版已開通！",
        "html": """
        <h2>哈囉！歡迎來到 SRS Pro</h2>
        <p>感謝您的申請。您現在可以馬上開始體驗「矽谷 SM2 演算法」加上「動漫視覺圖鑑」的高效記憶威力了。</p>
        <p>👇 點擊下方專屬連結，馬上開始你的提分之旅：</p>
        <p><a href="https://alexlee1120.github.io/vocab-flashcards/app.html" style="padding:10px 20px;background-color:#b537f2;color:white;text-decoration:none;border-radius:5px;">開始體驗 SRS Pro</a></p>
        <p>我們接下來幾天會與您分享一些「大腦駭客」的高效學習心法，請留意信箱喔！</p>
        <br><p>Alex 敬上</p>
        """
    }
    try:
        response = requests.post('https://api.resend.com/emails', headers=headers, json=data)
        return response.status_code == 200
    except:
        return False

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email = data.get('email')
    source = data.get('source', 'landing_page')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO subscribers (email, source) VALUES (?, ?)", (email, source))
        conn.commit()
        conn.close()
        
        # 觸發發信
        if send_welcome_email(email):
            return jsonify({'message': 'Subscription successful, welcome email sent'}), 200
        else:
            return jsonify({'message': 'Subscription saved, but email sending failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
