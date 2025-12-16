#!/usr/bin/env python3
"""
測試 DEVONthink 4 與 Ollama 連接的腳本
用來驗證 API 是否正常工作
"""

import requests
import json

def test_ollama_api():
    """測試 Ollama API 連接"""
    print("=" * 60)
    print("🧪 測試 Ollama API 連接")
    print("=" * 60)
    
    # API 配置
    base_url = "http://localhost:11434"
    model = "qwen2.5:3b"
    
    # 測試 1: 檢查服務器是否運行
    print("\n【測試 1】檢查服務器狀態...")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama 服務器正在運行")
            models = response.json().get("models", [])
            print(f"   可用模型數量: {len(models)}")
            for m in models:
                print(f"   - {m.get('name', 'Unknown')}")
        else:
            print(f"❌ 服務器返回錯誤: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 Ollama 服務器")
        print("   請確保 Ollama 正在運行：ollama serve")
        return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False
    
    # 測試 2: 檢查模型是否存在
    print("\n【測試 2】檢查模型是否存在...")
    model_exists = any(m.get('name') == model for m in models)
    if model_exists:
        print(f"✅ 模型 '{model}' 已安裝")
    else:
        print(f"❌ 模型 '{model}' 未找到")
        print(f"   請運行: ollama pull {model}")
        return False
    
    # 測試 3: 測試聊天 API
    print("\n【測試 3】測試聊天 API...")
    try:
        chat_url = f"{base_url}/api/chat"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "你好，請用一句話證明你正常工作。"
                }
            ],
            "stream": False
        }
        
        print("   發送測試消息...")
        response = requests.post(chat_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("message", {}).get("content", "")
            print("✅ 聊天 API 正常工作")
            print(f"   AI 回答: {answer[:100]}...")
        else:
            print(f"❌ API 返回錯誤: {response.status_code}")
            print(f"   響應: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False
    
    # 測試 4: 測試 OpenAI 兼容 API（如果 DEVONthink 使用這個）
    print("\n【測試 4】測試 OpenAI 兼容 API...")
    try:
        openai_url = f"{base_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "測試"
                }
            ],
            "stream": False
        }
        
        response = requests.post(openai_url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ OpenAI 兼容 API 正常工作")
        else:
            print(f"⚠️  OpenAI 兼容 API 不可用 (可能不影響)")
            print(f"   狀態碼: {response.status_code}")
    except Exception as e:
        print(f"⚠️  OpenAI 兼容 API 不可用: {e}")
        print("   （這通常不影響 DEVONthink 的基本連接）")
    
    # 總結
    print("\n" + "=" * 60)
    print("✅ 所有基本測試通過！")
    print("=" * 60)
    print("\n📋 DEVONthink 4 配置信息：")
    print("-" * 60)
    print(f"API 端點: {base_url}")
    print(f"模型名稱: {model}")
    print(f"聊天 API: {base_url}/api/chat")
    print("\n💡 在 DEVONthink 4 中配置時，請使用上述信息。")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    try:
        success = test_ollama_api()
        if success:
            print("\n🎉 測試成功！您可以開始配置 DEVONthink 4 了。")
        else:
            print("\n❌ 測試失敗，請檢查上述錯誤信息。")
    except KeyboardInterrupt:
        print("\n\n測試已取消。")
    except Exception as e:
        print(f"\n❌ 發生未預期的錯誤: {e}")









