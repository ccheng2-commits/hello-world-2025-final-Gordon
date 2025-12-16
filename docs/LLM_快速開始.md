# 🚀 本地 LLM 快速部署指南（小學生級教程）

## 📝 步驟 1: 確認 Ollama 已經安裝

您已經有 Ollama 了！讓我們確認一下：

```bash
# 檢查 Ollama 版本
ollama --version

# 查看已安裝的模型
ollama list
```

如果看到 `qwen2.5:3b`，說明模型已經下載好了！✅

---

## 📝 步驟 2: 第一次測試（最簡單的方法）

### 方法 A: 直接在命令行使用（最簡單！）

打開終端（Terminal），輸入：

```bash
ollama run qwen2.5:3b
```

然後你就可以直接和 AI 對話了！例如：
- 輸入：「你好」
- 輸入：「請介紹一下你自己」
- 輸入：「退出」或按 Ctrl+D 來結束對話

### 方法 B: 一次問答測試

```bash
ollama run qwen2.5:3b "你好，請用一句話介紹你自己"
```

---

## 📝 步驟 3: 用 Python 控制 LLM（進階）

如果你想在自己的 Python 程序中使用 LLM，有兩種方式：

### 方法 1: 使用命令行調用（不需要安裝 Python 庫）

創建文件 `test_llm_simple.py`：

```python
import subprocess
import json

def ask_ai(question):
    """最簡單的方法：直接調用命令行"""
    result = subprocess.run(
        ['ollama', 'run', 'qwen2.5:3b', question],
        capture_output=True,
        text=True
    )
    return result.stdout

# 測試
if __name__ == '__main__':
    print("🤖 開始測試...")
    answer = ask_ai("你好，請用一句話介紹你自己")
    print(f"\nAI 回答：\n{answer}")
```

運行：
```bash
python3 test_llm_simple.py
```

### 方法 2: 使用 Ollama API（推薦）

1. **確保 Ollama 服務正在運行**（通常它會自動啟動）

2. **安裝 Python 庫**：
```bash
# 如果在虛擬環境中
source venv/bin/activate
pip install ollama

# 或者系統級安裝（如果上面的不行）
pip3 install --user ollama
```

3. **創建測試腳本** `test_llm_api.py`：

```python
import ollama

def chat(prompt):
    """使用 Ollama API 和 AI 對話"""
    response = ollama.chat(model='qwen2.5:3b', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# 測試
if __name__ == '__main__':
    print("🤖 測試 Ollama API...")
    
    # 第一次測試
    answer = chat("你好，請用一句話介紹你自己")
    print(f"\nAI: {answer}\n")
    
    # 交互式對話
    print("開始對話（輸入 '退出' 結束）：")
    while True:
        user_input = input("\n你: ")
        if user_input.lower() in ['退出', 'quit', 'exit']:
            break
        
        answer = chat(user_input)
        print(f"AI: {answer}")
```

運行：
```bash
python3 test_llm_api.py
```

---

## 📝 步驟 4: 測試不同的模型

如果你想試試其他模型，可以：

```bash
# 查看可用的模型列表
ollama list

# 下載新模型（例如 Llama 3.2）
ollama pull llama3.2:3b

# 使用新模型
ollama run llama3.2:3b
```

---

## 🎯 推薦的模型（針對 8GB 內存的 MacBook Air M4）

| 模型名稱 | 大小 | 特點 | 下載命令 |
|---------|------|------|---------|
| **qwen2.5:3b** | 1.9GB | 中文支持最好 ⭐ | 已安裝 ✅ |
| llama3.2:3b | 2GB | 英文為主 | `ollama pull llama3.2:3b` |
| phi3:mini | 2.3GB | 速度最快 | `ollama pull phi3:mini` |

---

## ❓ 常見問題

### Q1: 如何停止 Ollama 服務？

```bash
# 查看 Ollama 進程
ps aux | grep ollama

# 停止 Ollama（如果需要）
pkill ollama
```

### Q2: 模型文件在哪裡？

模型保存在：`~/.ollama/models/`

### Q3: 如何查看模型使用多少內存？

```bash
# 查看當前運行的模型
ollama ps
```

### Q4: 如何更新 Ollama？

```bash
brew upgrade ollama
```

### Q5: Python 無法導入 ollama 庫？

如果 `pip install ollama` 失敗，試試：
- 使用虛擬環境
- 使用 `pip3 install --user ollama`
- 或使用命令行方法（不需要 Python 庫）

---

## 🎉 完成！

現在您已經可以在本地運行 LLM 了！

**下一步：**
- 試試直接運行：`ollama run qwen2.5:3b`
- 或者在 Python 程序中使用 LLM

有問題隨時問我！😊









