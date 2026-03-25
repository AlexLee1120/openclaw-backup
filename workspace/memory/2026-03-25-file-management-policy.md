# 2026-03-25 - 檔案目錄與資產管理規範更新

## 🗂️ 檔案結構與資產管理邏輯
- **核心原則：** **絕對禁止**將生成的媒體檔案、草稿、或非核心配置直接存放在 `/Users/alex-ai/.openclaw/workspace/` 根目錄。
- **目錄架構：**
  - **`workspace/`**: 僅保留核心配置 (如 `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `USER.md` 等) 與目錄索引。
  - **`workspace/memory/`**: 專用於存放每日對話日誌、決策紀錄與純文字形式的專案企劃 (如 Markdown)。
  - **`workspace/assets/`**: 所有非文字型態的「產出物 (Artifacts)」皆需分類存放於此。
    - **`workspace/assets/youtube-shorts/`**: 短影音專案 (依集數建立子目錄，如 `ep1/`, `ep2/`)。
    - **`workspace/assets/images/`**: 通用型生成的 AI 繪圖或視覺素材。
    - **`workspace/assets/audio/`**: 通用型生成的語音檔 (TTS) 或音樂。
    - **`workspace/assets/reports/`**: 生成的 PDF 或 Word 分析報告。

## 🤖 小艾執行守則
每次執行完 `image_generate` (圖片生成)、`tts` (語音生成) 或任何實體檔案建立操作後，**必須第一時間將檔案使用 Shell 命令 (`mv` 或 `cp`) 搬移至對應的 `assets/` 子目錄中**，並於回報時提供清晰的絕對路徑。