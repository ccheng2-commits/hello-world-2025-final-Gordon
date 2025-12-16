#!/usr/bin/env python3
"""
🤖 與本地 AI 對話程序
超級簡單版本 - 不需要安裝任何額外的 Python 庫
"""

import subprocess
import sys

def ask_ai(question, model='qwen2.5:3b'):
    """
    問 AI 問題並獲取回答
    
    Args:
        question: 你的問題
        model: 使用的模型名稱（默認是 qwen2.5:3b）
    
    Returns:
        AI 的回答
    """
    try:
        print("💭 AI 正在思考...", end="", flush=True)
        
        # 調用 ollama
        result = subprocess.run(
            ['ollama', 'run', model, question],
            capture_output=True,
            text=True,
            timeout=120  # 最多等待 2 分鐘
        )
        
        print()  # 換行
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"❌ 錯誤: {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "⏰ 超時了，請稍後再試"
    except Exception as e:
        return f"❌ 發生錯誤: {str(e)}"


def main():
    """主程序"""
    print("=" * 60)
    print("🤖 本地 AI 對話助手")
    print("=" * 60)
    print(f"\n使用的模型: qwen2.5:3b")
    print("提示：")
    print("  - 直接輸入問題，按 Enter 發送")
    print("  - 輸入 '退出'、'quit' 或 'exit' 結束對話")
    print("  - 輸入 '清空' 或 'clear' 清空屏幕")
    print("  - 輸入 '模型' 查看可用模型")
    print("\n" + "-" * 60 + "\n")
    
    # 檢查 Ollama 是否可用
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            print("❌ 錯誤：找不到 Ollama，請先安裝 Ollama")
            print("   安裝方法：brew install ollama")
            return
    except FileNotFoundError:
        print("❌ 錯誤：找不到 Ollama，請先安裝 Ollama")
        print("   安裝方法：brew install ollama")
        return
    
    # 檢查模型是否存在
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True)
        if 'qwen2.5:3b' not in result.stdout:
            print("⚠️  警告：qwen2.5:3b 模型未找到")
            print("   正在下載模型（這可能需要幾分鐘）...")
            subprocess.run(['ollama', 'pull', 'qwen2.5:3b'])
            print("✅ 模型下載完成！\n")
    except:
        pass
    
    # 對話循環
    conversation_count = 0
    
    while True:
        try:
            # 獲取用戶輸入
            user_input = input("你: ").strip()
            
            # 檢查空輸入
            if not user_input:
                continue
            
            # 處理特殊命令
            if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
                print("\n👋 再見！")
                break
            
            elif user_input.lower() in ['清空', 'clear']:
                import os
                os.system('clear' if os.name != 'nt' else 'cls')
                print("=" * 60)
                print("🤖 本地 AI 對話助手")
                print("=" * 60 + "\n")
                continue
            
            elif user_input.lower() in ['模型', 'models', 'list']:
                print("\n正在檢查可用模型...")
                result = subprocess.run(['ollama', 'list'], 
                                      capture_output=True, 
                                      text=True)
                print(result.stdout)
                continue
            
            # 發送問題給 AI
            conversation_count += 1
            answer = ask_ai(user_input)
            
            # 顯示回答
            print(f"AI: {answer}\n")
            print("-" * 60)
        
        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤: {e}")
            print("請稍後再試...\n")


if __name__ == '__main__':
    main()









