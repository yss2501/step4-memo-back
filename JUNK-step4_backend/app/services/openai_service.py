from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# ロガー設定
logger = logging.getLogger(__name__)
api_key=os.getenv("OPENAI_API_KEY") #add nakano

# OpenAI クライアントの初期化
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

async def summarize_meeting_content(content: str) -> str:
    """OpenAI APIを使用して面談内容を要約"""
    if not content.strip():
        return "要約する内容がありません。"
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """あなたは面談内容を要約する専門のアシスタントです。
以下の点に注意して要約を作成してください：
1. 重要なポイントと決定事項を含める
2. 簡潔で読みやすい日本語で作成する
3. 箇条書きを使って整理する
4. 300文字以内で要約する"""
                },
                {
                    "role": "user", 
                    "content": f"以下の面談内容を要約してください:\n\n{content}"
                }
            ],
            max_tokens=600,
            temperature=0.3,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        summary = response.choices[0].message.content
        if summary:
            return summary.strip()
        else:
            logger.warning("OpenAI APIからの応答が空でした")
            return "要約の生成に失敗しました（応答が空）。"
            
    except Exception as e:
        logger.error(f"OpenAI API エラー: {str(e)}")
        
        # 具体的なエラーメッセージを返す
        error_str = str(e).lower()
        if "api !!key" in error_str or "un!!authorized" in error_str:
            return "APIキーが設定されていないか無効です。"
        elif "quota" in error_str or "billing" in error_str:
            return "OpenAI APIの利用制限に達しています。"
        elif "rate_limit" in error_str:
            return "API利用頻度の制限に達しました。しばらく待ってから再度お試しください。"
        elif "model" in error_str and "not found" in error_str:
            return "指定されたAIモデルが見つかりません。"
        else:
            return f"要約の生成に失敗しました: {str(e)}"