# 📚 DEVONthink 4 連接本地 LLM 配置指南

本指南將幫助您在 DEVONthink 4 中配置使用本地的 Ollama LLM 模型。

---

## 📋 前置條件

在開始之前，請確認：

- ✅ **Ollama 已安裝**：`ollama --version`
- ✅ **模型已下載**：`ollama list` 應該顯示 `qwen2.5:3b`
- ✅ **Ollama 服務正在運行**：應該自動運行在後台

---

## 🔍 步驟 1: 確認 Ollama API 服務器運行

Ollama 默認提供一個 HTTP API 服務器在端口 `11434`。

### 檢查服務器狀態

打開終端，運行：

```bash
# 檢查 Ollama 是否在運行
lsof -i :11434

# 或者測試 API
curl http://localhost:11434/api/tags
```

如果看到輸出，說明服務器正在運行。✅

### 如果服務器未運行

啟動 Ollama 服務：

```bash
# 啟動服務（通常會自動啟動）
ollama serve

# 或者直接在後台運行
nohup ollama serve > /dev/null 2>&1 &
```

---

## 🔧 步驟 2: 在 DEVONthink 4 中配置 Ollama

### 方法 A: 通過設置界面配置（推薦）

1. **打開 DEVONthink 4**

2. **進入設置**
   - 點擊菜單欄：`DEVONthink` → `Settings...`（或按 `⌘,`）
   - 或者：`DEVONthink` → `Preferences...`

3. **找到 AI 設置**
   - 在設置窗口中，找到並點擊 **`AI`** 標籤頁
   - 然後點擊 **`Chat`** 選項

4. **選擇 Ollama 作為引擎**
   - 在 `Chat` 設置中，找到 **`Engine`** 或 **`Provider`** 下拉菜單
   - 選擇 **`Ollama`** 或 **`Local`** 或 **`Custom API`**

5. **配置連接信息**
   
   根據 DEVONthink 4 的版本，可能需要輸入以下信息：
   
   - **API 端點（Endpoint）**: `http://localhost:11434`
   - **API 路徑（API Path）**: `/api/chat` 或 `/api/generate`
   - **模型名稱（Model）**: `qwen2.5:3b`
   
   具體配置選項可能包括：
   ```
   Base URL: http://localhost:11434
   Model: qwen2.5:3b
   API Key: （本地不需要，留空）
   ```

6. **測試連接**
   - 點擊 **`Test`** 或 **`Check Connection`** 按鈕
   - 如果成功，應該會看到確認消息

### 方法 B: 如果找不到 Ollama 選項

如果 DEVONthink 4 的設置中沒有直接的 Ollama 選項，可以嘗試：

#### 選項 1: 使用 OpenAI 兼容模式

Ollama 支持 OpenAI 兼容的 API。在 DEVONthink 中：

1. 選擇 **`OpenAI`** 作為引擎
2. 設置：
   - **Base URL**: `http://localhost:11434/v1`
   - **API Key**: `ollama`（可以是任意值，Ollama 會忽略）
   - **Model**: `qwen2.5:3b`

#### 選項 2: 使用自定義 API

如果支持自定義 API 配置：

1. 選擇 **`Custom API`** 或 **`HTTP API`**
2. 配置：
   - **Endpoint**: `http://localhost:11434/api/chat`
   - **Method**: `POST`
   - **Headers**: `Content-Type: application/json`
   - **Body Template**: 
     ```json
     {
       "model": "qwen2.5:3b",
       "messages": [{"role": "user", "content": "{{prompt}}"}],
       "stream": false
     }
     ```

---

## 🧪 步驟 3: 測試連接

### 測試 Ollama API（在終端）

在配置 DEVONthink 之前，先測試 API 是否正常工作：

```bash
# 測試 API 連接
curl http://localhost:11434/api/chat \
  -d '{
    "model": "qwen2.5:3b",
    "messages": [
      {
        "role": "user",
        "content": "你好，請說一句話證明你正常工作。"
      }
    ],
    "stream": false
  }'
```

如果看到 JSON 回應，說明 API 正常工作。✅

### 在 DEVONthink 中測試

1. 在 DEVONthink 中選擇一個文檔
2. 打開 **Chat** 面板（通常在右側）
3. 輸入一個簡單問題，例如："請總結這個文檔"
4. 查看是否有回應

---

## 📝 詳細配置參數參考

### Ollama API 端點信息

- **服務器地址**: `http://localhost:11434`
- **聊天 API**: `http://localhost:11434/api/chat`
- **生成 API**: `http://localhost:11434/api/generate`
- **列表模型**: `http://localhost:11434/api/tags`

### 常用模型名稱

- `qwen2.5:3b` - 中文友好（推薦）
- `llama3.2:3b` - 英文為主
- `phi3:mini` - 輕量級，速度快

---

## 🔍 故障排除

### 問題 1: DEVONthink 無法連接到 Ollama

**解決方案：**

1. 確認 Ollama 服務正在運行：
   ```bash
   lsof -i :11434
   ```
   
2. 如果沒有運行，啟動服務：
   ```bash
   ollama serve
   ```

3. 檢查防火牆設置（通常本地連接不需要）

### 問題 2: 連接超時

**解決方案：**

- 確保 Ollama 服務器地址正確：`http://localhost:11434`
- 不要使用 `127.0.0.1`，使用 `localhost`
- 檢查是否有其他程序佔用 11434 端口

### 問題 3: 模型名稱找不到

**解決方案：**

1. 確認模型已下載：
   ```bash
   ollama list
   ```

2. 如果沒有，下載模型：
   ```bash
   ollama pull qwen2.5:3b
   ```

3. 使用正確的模型名稱（包括版本號，如 `qwen2.5:3b`）

### 問題 4: API 格式不兼容

**解決方案：**

如果 DEVONthink 需要的 API 格式與 Ollama 不同，可以：

1. 使用 OpenAI 兼容模式（如果支持）：
   - Base URL: `http://localhost:11434/v1`

2. 或者創建一個簡單的代理服務器（見下方）

---

## 🛠️ 進階：創建 API 代理（可選）

如果 DEVONthink 的 API 格式與 Ollama 不完全兼容，可以創建一個簡單的代理服務器。

我為您準備了一個簡單的代理腳本（如果需要可以創建）。

---

## ✅ 配置檢查清單

完成配置後，確認以下項目：

- [ ] Ollama 服務正在運行（端口 11434）
- [ ] 模型已下載（`ollama list` 顯示模型）
- [ ] DEVONthink 4 中已選擇 Ollama 或配置了自定義 API
- [ ] API 端點設置為 `http://localhost:11434`
- [ ] 模型名稱設置為 `qwen2.5:3b`
- [ ] 測試連接成功
- [ ] 在 DEVONthink 中可以正常使用 Chat 功能

---

## 📚 參考資料

### Ollama API 文檔

Ollama 提供了完整的 API 文檔：

```bash
# 查看 API 文檔
curl http://localhost:11434/api

# 查看可用模型
curl http://localhost:11434/api/tags
```

### DEVONthink 4 文檔

- DEVONthink 4 用戶手冊中的 "AI" 或 "Chat" 章節
- DEVONthink 官方論壇可能有其他用戶的配置經驗

---

## 🎯 快速配置命令

如果您想快速測試，可以在終端運行：

```bash
# 1. 確認 Ollama 運行
ollama serve &

# 2. 確認模型存在
ollama list

# 3. 測試 API
curl http://localhost:11434/api/tags
```

然後在 DEVONthink 4 中：
- 設置 → AI → Chat
- 選擇 Ollama 或配置自定義 API
- 輸入：`http://localhost:11434`
- 模型：`qwen2.5:3b`

---

## 💡 使用建議

1. **性能優化**
   - DEVONthink 的 AI 功能通常用於總結和問答
   - 對於長文檔，可能處理時間較長，請耐心等待

2. **隱私保護**
   - 使用本地 LLM 的最大優勢是完全離線和隱私保護
   - 所有數據都在本地處理，不會上傳到雲端

3. **多模型切換**
   - 可以下載多個模型，根據需要切換
   - 在 DEVONthink 設置中更改模型名稱即可

---

## 🆘 需要幫助？

如果遇到問題：

1. 檢查 Ollama 服務器日誌：
   ```bash
   # 查看 Ollama 進程
   ps aux | grep ollama
   ```

2. 重啟 Ollama 服務：
   ```bash
   pkill ollama
   ollama serve
   ```

3. 檢查 DEVONthink 的錯誤日誌（在應用設置中）

4. 查看本文檔的故障排除部分

---

**祝您配置順利！** 🎉









