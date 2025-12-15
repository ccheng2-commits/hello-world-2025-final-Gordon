# 🚀 DEVONthink 4 連接本地 LLM - 快速配置指南

## ✅ 當前狀態確認

您的系統已經準備就緒：

- ✅ **Ollama 已安裝**：版本 0.13.0
- ✅ **模型已下載**：qwen2.5:3b (1.9GB)
- ✅ **API 服務器運行中**：`http://localhost:11434`
- ✅ **API 測試通過**：可以正常對話

---

## 🎯 三個簡單步驟

### 步驟 1: 測試連接（30秒）

在終端運行我們的測試腳本：

```bash
cd /Users/gc/Documents/GitHub/hello-world-2025-final-Gordon
./test_ollama_api.sh
```

或者手動測試：

```bash
curl http://localhost:11434/api/tags
```

如果看到模型列表，說明一切正常！✅

---

### 步驟 2: 在 DEVONthink 4 中配置（2分鐘）

#### 打開 DEVONthink 4 設置

1. 打開 DEVONthink 4
2. 點擊菜單：`DEVONthink` → `Settings...`（或按 `⌘,`）

#### 找到 AI/Chat 設置

根據您的 DEVONthink 4 版本，可能有以下選項：

**選項 A: 有 "Ollama" 選項（最簡單）**

1. 點擊 **`AI`** 標籤
2. 點擊 **`Chat`** 選項
3. 在 **`Engine`** 或 **`Provider`** 中選擇 **`Ollama`**
4. 輸入配置：
   - **Server**: `http://localhost:11434`
   - **Model**: `qwen2.5:3b`
5. 點擊 **`Test`** 或 **`Apply`**

**選項 B: 使用 OpenAI 兼容模式**

1. 點擊 **`AI`** 標籤
2. 點擊 **`Chat`** 選項
3. 在 **`Engine`** 中選擇 **`OpenAI`** 或 **`Custom`**
4. 輸入配置：
   - **Base URL**: `http://localhost:11434/v1`
   - **API Key**: `ollama`（可以填任意值）
   - **Model**: `qwen2.5:3b`
5. 點擊 **`Test`** 或 **`Apply`**

**選項 C: 自定義 API**

1. 點擊 **`AI`** 標籤
2. 點擊 **`Chat`** 選項
3. 選擇 **`Custom API`** 或 **`HTTP API`**
4. 配置：
   - **Endpoint**: `http://localhost:11434/api/chat`
   - **Method**: `POST`
   - **Headers**: `Content-Type: application/json`
   - **Model Parameter**: `qwen2.5:3b`

---

### 步驟 3: 測試使用（1分鐘）

1. 在 DEVONthink 4 中選擇一個文檔
2. 打開 **Chat** 面板（通常在右側邊欄）
3. 輸入測試問題：`請總結這個文檔的主要內容`
4. 等待 AI 回答

如果看到回答，恭喜！配置成功！🎉

---

## 📋 配置參數參考表

| 配置項 | 值 |
|--------|-----|
| **API 服務器地址** | `http://localhost:11434` |
| **模型名稱** | `qwen2.5:3b` |
| **聊天 API 端點** | `http://localhost:11434/api/chat` |
| **OpenAI 兼容端點** | `http://localhost:11434/v1/chat/completions` |

---

## 🔍 如果找不到設置選項

DEVONthink 4 的界面可能因版本而異。試試這些地方：

1. **菜單欄查找**：
   - `DEVONthink` → `Settings` → `AI`
   - `DEVONthink` → `Preferences` → `AI`
   - `Edit` → `Preferences` → `AI`

2. **快捷鍵**：
   - `⌘,`（Command + 逗號）打開設置

3. **文檔中查找**：
   - 在 DEVONthink 中搜索 "AI" 或 "Chat" 或 "Ollama"

4. **查看幫助**：
   - `Help` → `DEVONthink Help`
   - 搜索 "AI" 或 "local model"

---

## ❓ 常見問題

### Q1: 找不到 AI/Chat 設置？

**A:** 
- 確認您使用的是 DEVONthink 4（不是 3 或其他版本）
- 某些版本可能沒有這個功能，需要更新到最新版本
- 查看 DEVONthink 官方文檔確認您的版本支持 AI 功能

### Q2: 連接失敗怎麼辦？

**檢查清單：**
- [ ] Ollama 服務器是否運行？運行 `lsof -i :11434` 檢查
- [ ] 如果沒運行，執行 `ollama serve`
- [ ] 模型是否存在？運行 `ollama list` 檢查
- [ ] API 地址是否正確？應該是 `http://localhost:11434`

### Q3: 如何確認 Ollama 正在運行？

```bash
# 方法 1: 檢查端口
lsof -i :11434

# 方法 2: 測試 API
curl http://localhost:11434/api/tags

# 方法 3: 查看進程
ps aux | grep ollama
```

### Q4: 想使用其他模型？

```bash
# 查看所有模型
ollama list

# 下載新模型
ollama pull llama3.2:3b

# 在 DEVONthink 設置中更改模型名稱
```

---

## 🎉 完成！

配置完成後，您就可以在 DEVONthink 4 中使用本地 LLM 了！

### 使用場景：

- 📄 **文檔總結**：選中文檔，讓 AI 總結
- ❓ **問答**：針對文檔內容提問
- 📝 **內容生成**：根據上下文生成文本
- 🔍 **研究輔助**：分析多個文檔

### 優勢：

- ✅ **完全離線**：所有處理都在本地
- ✅ **隱私保護**：數據不會上傳到雲端
- ✅ **快速響應**：在您的 MacBook Air M4 上運行順暢
- ✅ **免費使用**：不需要付費 API

---

## 📚 更多資源

- **詳細配置指南**：查看 `DEVONthink4_配置指南.md`
- **測試腳本**：運行 `./test_ollama_api.sh`
- **Ollama 文檔**：https://github.com/ollama/ollama

---

**祝您使用愉快！** 如有問題，請查看詳細配置指南或測試腳本。








