"""
Ollama 測試腳本 - 超級簡單版本
用這個腳本來測試你的 LLM 是否正常工作
"""

import ollama

def chat(prompt):
    """
    發送問題給 AI，並獲取回答
    
    Args:
        prompt: 你想問的問題（文字）
    
    Returns:
        AI 的回答（文字）
    """
    print(f"你問: {prompt}")
    print("AI 正在思考...")
    
    response = ollama.chat(model='qwen2.5:3b', messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    answer = response['message']['content']
    return answer


if __name__ == '__main__':
    print("=" * 50)
    print("🤖 歡迎使用 Ollama LLM 測試程序！")
    print("=" * 50)
    print("\n提示：輸入 '退出' 或 'quit' 可以結束程序\n")
    
    # 第一次測試 - 簡單問候
    print("【第一次測試】")
    first_test = chat("你好，請用一句話介紹一下你自己。")
    print(f"AI 回答: {first_test}\n")
    
    # 交互式對話
    print("【開始對話模式】")
    print("-" * 50)
    
    while True:
        # 讓用戶輸入問題
        user_input = input("\n你: ")
        
        # 檢查是否要退出
        if user_input.lower() in ['quit', 'exit', '退出', 'q']:
            print("\n再見！👋")
            break
        
        # 如果輸入是空的，跳過
        if not user_input.strip():
            print("請輸入一些文字...")
            continue
        
        # 獲取 AI 回答並顯示
        try:
            answer = chat(user_input)
            print(f"\nAI: {answer}")
        except Exception as e:
            print(f"❌ 出錯了: {e}")
            print("請檢查 Ollama 是否正在運行")












