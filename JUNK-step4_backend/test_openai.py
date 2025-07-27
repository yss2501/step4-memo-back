#!/usr/bin/env python3
"""
OpenAI要約機能のテストスクリプト
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.openai_service import summarize_meeting_content

async def test_openai_summarization():
    """OpenAI要約機能をテスト"""
    load_dotenv()
    
    print("=== OpenAI要約機能テスト ===")
    
    # APIキーの確認
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY が設定されていません")
        print("   .envファイルに以下を追加してください:")
        print("   OPENAI_API_KEY=your_openai_api_key_here")
        return
    else:
        print(f"✅ APIキーが設定されています: {api_key[:10]}...")
    
    # テスト用の面談内容
    test_content = """
    今日の面談では、新しいプロジェクトについて話し合いました。
    
    参加者：田中さん（プロジェクトマネージャー）、佐藤さん（開発チーム）
    
    主な議題：
    1. プロジェクトのスケジュール確認
    2. 必要なリソースの検討
    3. リスクの洗い出し
    
    決定事項：
    - 開発期間を6ヶ月とする
    - チームメンバーを5名体制とする
    - 週次の進捗会議を毎週金曜日に実施
    - 次回会議は来週火曜日の14:00から
    
    課題：
    - 外部ライブラリの選定が必要
    - テスト環境の準備が遅れている
    
    その他：
    - 予算についてはCFOの承認待ち
    - デザインチームとの連携も必要
    """
    
    print("\n=== テスト内容 ===")
    print(f"入力テキスト文字数: {len(test_content)}文字")
    print(f"入力テキスト（最初の100文字）: {test_content[:100]}...")
    
    try:
        print("\n=== 要約生成中 ===")
        summary = await summarize_meeting_content(test_content)
        
        print("\n=== 生成結果 ===")
        print(f"要約文字数: {len(summary)}文字")
        print(f"要約内容:")
        print("-" * 50)
        print(summary)
        print("-" * 50)
        
        if "エラー" in summary or "失敗" in summary:
            print("\n⚠️  要約生成でエラーが発生しました")
            print("   - APIキーが有効か確認してください")
            print("   - OpenAI APIの利用制限を確認してください")
            print("   - インターネット接続を確認してください")
        else:
            print("\n✅ テスト成功！")
        
    except Exception as e:
        print(f"\n❌ テスト失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_openai_summarization())