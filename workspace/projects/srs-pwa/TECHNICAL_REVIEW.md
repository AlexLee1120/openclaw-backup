# SRS 單字學習卡 PWA - 技術審查報告

## 📋 專案概況
*   **技術棧：** 純 HTML/JS + Tailwind CSS + Lucide Icons。
*   **核心功能：** PWA 離線支援、SRS 間隔重複演算法、自動發音 (Web Speech API)、CSV 匯入、進度儲存 (LocalStorage)。
*   **部署現狀：** 原始碼託管於 GitHub `AlexLee1120/vocab-flashcards`。

## 🔍 技術審查結果 (Architect Perspective)

### 1. SRS 演算法 (Core Logic)
*   **現狀：** 採用了簡化版的隊列移動邏輯（Again = 插入第 2 張, Hard = 插入隊列中段, Good = 移至隊尾, Easy = 移出隊列）。
*   **優點：** 輕量、即時反饋感強。
*   **改進空間：** 為了長期記憶，未來可考慮引入真正基於時間戳記的 **SM2 演算法**（儲存每張卡的 E-factor 與複習日期），這將使 App 更具學術說服力（Marketing USP）。

### 2. PWA 與離線能力
*   **現狀：** `sw.js` 已實現基礎的靜態資源緩存 (Cache-first 策略)。
*   **優點：** 符合 PWA 標準，支持安裝至桌面。
*   **資安警示：** 目前 `index.html` 內含一個指向 `/send-trial` 與 `/checkout` 的 Form，這暗示需要後端 API 支援（推測是 Flask/Python），前端 PWA 需確保在離線時能優雅處理這些網絡請求。

### 3. 數據儲存
*   **現狀：** 使用 `localStorage`。
*   **風險點：** 瀏覽器清理緩存時，用戶辛苦學習的進度可能會消失。
*   **架構建議：** 遷移至 **IndexedDB**（更強大的客戶端資料庫）或提供 **Cloud Sync (GitHub API/Google Drive)** 功能，這可以作為「進階版」的賣點。

---

## 🚀 後續進行計劃 (Action Plan)

### 第一階段：穩定性與部署 (Week 1)
1.  **正式部署：** 將 `vocab-flashcards` 倉庫啟用 **GitHub Pages**。這將提供正式的 https 網址，供 PWA 安裝。
2.  **Code Hardening：** 我將提交一個 Pull Request (PR)，優化 CSV 解析邏輯（目前對複雜引號的處理可能有 Bug）並加入 IndexedDB 支援。

### 第二階段：行銷與內容啟動 (Week 2)
1.  **內容編寫員：** 開始整理 30 天單字挑戰（針對學測/TOEIC）。
2.  **創意總監：** 基於 App UI 生成高品質的 YouTube 宣傳圖與腳本。
3.  **Joyce (數據師)：** 在 App 內嵌入簡單的數據追蹤代碼（如 Plausible 或自建），監控用戶停留時間。

### 第三階段：YouTube 頻道連動 (Ongoing)
1.  製作教學影片，將 App 作為免費工具贈送，引流至「智慧力存」品牌。

---

## 💡 Alex，我現在需要你：
1.  **授權操作：** 你是否同意我在本地克隆你的倉庫，並開始撰寫優化代碼（如 IndexedDB 整合與 UI 小修補）？
2.  **部署確認：** 我可以直接幫你配置 GitHub Pages 嗎？（需要你提供相關權限或引導你操作）。
