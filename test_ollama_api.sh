#!/bin/bash
# 測試 Ollama API 連接的簡單腳本
# 不需要安裝任何額外的 Python 庫

echo "=========================================="
echo "🧪 測試 Ollama API 連接"
echo "=========================================="

# 配置
BASE_URL="http://localhost:11434"
MODEL="qwen2.5:3b"

echo ""
echo "【測試 1】檢查服務器狀態..."
if curl -s "$BASE_URL/api/tags" > /dev/null 2>&1; then
    echo "✅ Ollama 服務器正在運行"
    echo ""
    echo "可用模型："
    curl -s "$BASE_URL/api/tags" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | sed 's/^/   - /'
else
    echo "❌ 無法連接到 Ollama 服務器"
    echo "   請確保 Ollama 正在運行：ollama serve"
    exit 1
fi

echo ""
echo "【測試 2】測試聊天 API..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"你好，請用一句話證明你正常工作。\"
      }
    ],
    \"stream\": false
  }")

if echo "$RESPONSE" | grep -q "message"; then
    echo "✅ 聊天 API 正常工作"
    ANSWER=$(echo "$RESPONSE" | grep -o '"content":"[^"]*"' | cut -d'"' -f4)
    echo "   AI 回答: $ANSWER"
else
    echo "❌ API 測試失敗"
    echo "   響應: $RESPONSE"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 所有測試通過！"
echo "=========================================="
echo ""
echo "📋 DEVONthink 4 配置信息："
echo "------------------------------------------"
echo "API 端點: $BASE_URL"
echo "模型名稱: $MODEL"
echo "聊天 API: $BASE_URL/api/chat"
echo ""
echo "💡 在 DEVONthink 4 中配置時，請使用上述信息。"
echo "=========================================="








