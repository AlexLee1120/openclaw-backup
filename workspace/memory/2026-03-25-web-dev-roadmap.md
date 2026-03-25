# SRS Pro Web 端優化與 1000 字庫整合方案 (2026-03-25)

## 🎯 核心目標
將前台 (GitHub Pages) 從「30 字先鋒版」平滑升級為支援「1000 字完整版」，並確保網頁載入效能 (Performance) 與使用者體驗 (UX) 維持最佳狀態。

## 🛠️ 技術優化節點 (Tasks)

### 1. 資料解析與效能優化 (CSV Parser)
- **問題：** 1000 筆帶有例句的單字 CSV 檔案較大，如果在網頁首次載入時同步解析，可能導致畫面卡頓 (UI Blocking)。
- **解法：** 導入 `Papa Parse` 函式庫，並啟用 `Worker` 模式進行背景非同步解析 (Web Worker parsing)。
- **資料分頁 (Pagination)：** 每次只將「當天需複習 (SM2 due)」的單字載入主記憶體 (RAM)，其餘皆存放在 IndexedDB。

### 2. IndexedDB 儲存架構升級
- **目前架構：** 紀錄 30 個單字的熟練度 (EF, Interval, Repetition)。
- **優化需求：** 需為 1000 字設計 `id` (主鍵)，以便與後台 (Railway Flask) 同步使用者的學習進度。
- **實作：** 使用 `idb` 或 `Dexie.js`，建立 `Words` 與 `LearningProgress` 兩張關聯表。

### 3. UI/UX 與 3D 翻牌特效微調
- **進度條 (Progress Bar)：** 增加「今日剩餘單字數 / 總字數」的視覺回饋。
- **效能問題：** 3D 翻轉動畫 (`transform-style: preserve-3d`) 在手機 (iOS Safari) 顯示大量卡片時可能閃爍。
- **優化解法：** 使用 `will-change: transform` 或 `backface-visibility: hidden` 進行 GPU 硬體加速優化。
- **手勢支援：** 加入 Swipe 左滑 (不熟) / 右滑 (熟練) 的 Tinder-like 手勢操作，取代點擊按鈕，更符合捷運通勤族單手使用習慣。

## 🚀 部署排程
1. 前端先以 30 字 CSV 實作 Swipe 手勢與 GPU 翻牌優化 (PR#1)。
2. 後台 Python 腳本產出 1000 字 CSV 後，掛載至 CDN 或 GitHub Pages 的 `public` 資料夾。
3. 實作 Web Worker 背景解析與 IndexedDB 升級 (PR#2)。