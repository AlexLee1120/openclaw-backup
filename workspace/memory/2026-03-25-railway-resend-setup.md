# Railway 後端與 Resend 寄信系統部署指南

## 🎯 任務目標
將 Landing Page 收集到的名單 (Email)，透過 Python Flask 後端存入資料庫，並自動觸發 **Resend API** 寄送第一封「Welcome Email (歡迎信與體驗連結)」。

## 🛠️ 執行步驟 (在您的 Railway 專案上操作)

### 1. 更新 Railway 專案架構
我已經為您寫好了一份包含「資料庫儲存」與「Resend 發信功能」的完整 `app.py` 程式碼。
📁 程式碼草稿存放於：`/Users/alex-ai/.openclaw/workspace/scripts/railway_backend_setup.py`

您需要將這份程式碼覆蓋到您 Railway 上的 Flask 專案主程式 (`app.py`)。

### 2. 環境變數設定 (Environment Variables)
在您的 Railway Dashboard 內，進入該 Python 服務的 `Variables` 標籤頁，新增以下變數：
- **`RESEND_API_KEY`**: (請前往 [resend.com](https://resend.com/) 註冊並取得您的 API Key)。
- **`PORT`**: `5000` (通常 Railway 會自動指派，但可預防性設定)。

### 3. 新增依賴套件 (requirements.txt)
確保您的 `requirements.txt` 檔案包含以下套件，以便 Flask 能處理跨網域請求 (CORS) 與呼叫外部 API：
```text
Flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
gunicorn==21.2.0
```

### 4. 自動化追蹤信件 (Drip Campaign) 的後續安排
目前的 `app.py` 已經實作了「註冊當下立刻寄送第一封歡迎信」。
至於後續的【週一、週三、週五、週六】四天自動化行銷信件，我們可以在下一個階段透過 **Railway 的 Cron Jobs (排程服務)** 或者直接串接第三方的 Email 行銷平台 (如 Mailchimp / ConvertKit) 透過 API 定時派發。