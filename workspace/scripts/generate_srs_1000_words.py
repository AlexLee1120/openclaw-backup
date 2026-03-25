import urllib.request
import json
import time
import os
import sys

# 使用剛才設定好的第二把 Gemini API 金鑰 (作為高頻數據產出專用)
API_KEY = "AIzaSyADUczhW4uheFIe9SCvk6IY-_1F_-fxUPU"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
OUTPUT_FILE = "/Users/alex-ai/.openclaw/workspace/assets/srs-data/SRS_Pro_核心單字_1000字完整版.csv"

# 確保目錄存在
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# 寫入 CSV 標頭
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("單字,詞性,中文解釋,例句,例句翻譯\n")

print("🚀 [背景任務] 開始生成 1000 個 SRS Pro 核心單字 (分為 20 批次，每批 50 字)...")

for i in range(1, 21):
    prompt = f"""
    任務：生成 50 個適合台灣高中生「學測英文 (4000-7000單字)」的高頻核心單字。這是第 {i} 批。
    要求：
    1. 必須是不同的單字，不要與常見的國中單字重複太多。
    2. 嚴格遵守 CSV 格式，欄位順序：單字,詞性,中文解釋,例句,例句翻譯
    3. 例句必須符合高中生生活情境或學測常見語境，難度適中。
    4. 詞性請用縮寫 (如 n., v., adj., adv.)。
    5. 不要包含任何 Markdown 標記 (如 ```csv)、不要輸出表頭，只輸出資料行！
    """

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }
    
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read()
            res_json = json.loads(res_body)
            
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                text = res_json['candidates'][0]['content']['parts'][0]['text']
                # 清理可能的 markdown 標籤
                text = text.replace("```csv", "").replace("```", "").strip()
                
                # 過濾掉空行與不小心生成的表頭
                lines = text.split('\n')
                clean_lines = [line.strip() for line in lines if line.strip() and not line.startswith("單字,詞性")]
                
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write("\n".join(clean_lines) + "\n")
                    
                print(f"✅ 批次 {i}/20 寫入完成 (約 50 字)")
            else:
                print(f"⚠️ 批次 {i} 回傳格式異常，跳過。")
                
    except Exception as e:
        print(f"❌ 批次 {i} 發生錯誤: {e}")
        time.sleep(5)  # 發生錯誤時多休息一下
        
    time.sleep(2)  # 避免觸發 API Rate Limit

print(f"🎉 [背景任務] 1000 字字庫生成完畢！檔案儲存於: {OUTPUT_FILE}")
