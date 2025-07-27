#!/usr/bin/env python3
"""
Supabase接続のテストスクリプト
"""
import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def test_different_connection_configs():
    """異なる接続設定をテスト"""
    load_dotenv()
    
    # 元のURL
    original_url = os.getenv("DATABASE_URL")
    print(f"元のURL: {original_url}")
    
    # テストする接続設定のリスト
    test_configs = [
        {
            "name": "元の設定",
            "url": original_url,
            "connect_args": {}
        },
        {
            "name": "SSL設定付き",
            "url": original_url,
            "connect_args": {
                "sslmode": "require",
                "connect_timeout": 10
            }
        },
        {
            "name": "パスワードURLエンコード",
            "url": original_url.replace("tech0-junk!", "tech0-junk%21"),
            "connect_args": {
                "sslmode": "require",
                "connect_timeout": 10
            }
        },
        {
            "name": "プール設定なし",
            "url": original_url,
            "connect_args": {
                "sslmode": "require",
                "connect_timeout": 30
            }
        }
    ]
    
    for config in test_configs:
        print(f"\n=== {config['name']} ===")
        try:
            engine = create_engine(
                config["url"],
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args=config["connect_args"]
            )
            
            # 接続テスト
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.fetchone()[0]
                print(f"✅ 接続成功: {test_value}")
                
                # 簡単なクエリテスト
                result = conn.execute(text("SELECT COUNT(*) FROM coworkers"))
                count = result.fetchone()[0]
                print(f"✅ クエリ成功: coworkersテーブルに {count} 行")
                
        except Exception as e:
            print(f"❌ 接続失敗: {e}")
            
        # 少し待機
        time.sleep(1)

if __name__ == "__main__":
    test_different_connection_configs()