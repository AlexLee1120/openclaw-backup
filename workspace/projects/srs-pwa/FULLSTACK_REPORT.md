# 全端整合與自動化部署建議報告

## 📋 專案架構分析 (Full-Stack Architecture)
*   **前端：** GitHub Pages (靜態託管 `index.html`, `app.html`, `sw.js`)。
*   **後端：** Railway (Python Flask `app.py`)。
*   **郵件：** Resend API (自動發送體驗版與購買後的 CSV)。
*   **金流：** 綠界科技 (ECPay)。

## 🔍 目前診斷 (Architect Insight)
1.  **404 衝突解決：** 剛才我們將 GitHub Pages 的表單改為直接跳轉 `app.html` 是為了快速解決 404，但這會「繞過」你的 Railway 後端，導致 **Resend 郵件無法寄出**（因為沒有經過 Flask 的 `/send-trial` 路由）。
2.  **API 網域問題：** 前端目前的代碼使用的是相對路徑（如 `/send-trial`），在 GitHub Pages 上運作時會指向 `github.io/send-trial` (不存在)，而非你的 Railway 伺服器。
3.  **Vibe Coding 整合：** 你的 `app.py` 中已經包含了完整的 ECPay 與 Resend 邏輯，我們應該讓前端正式對接到這個後端。

---

## 🚀 最終優化與上線計劃 (Action Plan)

### 1. 前後端正式對接 (現在進行)
我將修改 `index.html` 與 `app.html`，將 API 請求正式指向你的 Railway 網址（推測為 `https://vocab-flashcards-production.up.railway.app` 或類似網址，需從 Railway 設定中確認 `APP_DOMAIN`）。
*   **效果：** 點擊「立即體驗」後，後端會觸發 Resend 寄信，同時將用戶導向 App。

### 2. PWA 功能硬化 (Hardening)
*   將我優化過的 **SRS Pro (IndexedDB + SM2)** 代碼正式合併到 `app.html`。
*   更新 `sw.js`，加入對 Railway API 的優雅降級處理。

### 3. 多智能體任務分配 (MAS Tasks)
*   **✍️ 內容編寫員：** 已完成 30 個隨機單字 CSV。建議將此 CSV 直接放入 Railway 的靜態目錄，方便用戶下載。
*   **📊 數據師 Joyce：** 建議在 Railway 設定中開啟 **Webhooks**，讓 Joyce 能夠在 Telegram 即時收到「新用戶申請體驗」的通知。
*   **🎬 影音總監：** 腳本已就緒，等待最終網址確認後即可開拍。

---

## 💡 Alex，我需要你提供：
1.  **Railway 公開網址：** 請到 Railway 的 `Settings` > `Domains` 複製那個 `xxx.up.railway.app` 的網址給我。
2.  **授權最終合併：** 我是否可以將「前端指向 Railway API」的修改正式推送到 GitHub？

**一旦完成對接，你的「單字卡帝國」就具備了自動化獲客（Email）與自動化變現（ECPay）的完整商業閉環！** 🤓🚀