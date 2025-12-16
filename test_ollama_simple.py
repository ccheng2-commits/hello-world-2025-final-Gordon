#!/usr/bin/env python3
"""
超級簡單的 Ollama 測試腳本
不需要安裝任何額外的 Python 庫！
"""

import subprocess

def ask_ai(question):
    """
    用最簡單的方法問 AI 問題
    直接調用命令行，不需要安裝 Python 庫
    """
    print(f"你問: {question}")
    print("AI 正在思考...\n")
    
    # 調用 ollama 命令行
    result = subprocess.run(
        ['ollama', 'run', 'qwen2.5:3b', question],
        capture_output=True,
        text=True,
        timeout=60  # 最多等待 60 秒
    )
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"錯誤: {result.stderr}"


if __name__ == '__main__':
    print("=" * 60)
    print("🤖 Ollama 本地 LLM 測試程序")
    print("=" * 60)
    print("\n這個程序不需要安裝任何 Python 庫！")
    print("直接使用 Ollama 命令行工具。\n")
    
    # 第一次測試
    print("【第一次測試】")
    print("-" * 60)
    answer1 = ask_ai("你好，請用一句話介紹一下你自己")
    print(f"AI: {answer1}\n")
    
    # 第二次測試
    print("【第二次測試】")
    print("-" * 60)
    answer2 = ask_ai("什麼是人工智能？請用簡單的語言解釋。")
    print(f"AI: {answer2}\n")
    
    print("=" * 60)
    print("✅ 測試完成！")
    print("=" * 60)
    print("\n提示：")
    print("1. 如果想繼續對話，直接運行：ollama run qwen2.5:3b")
    print("2. 或者修改這個腳本，添加更多問題")









