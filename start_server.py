#!/usr/bin/env python3
"""
FastAPIサーバーの起動スクリプト（デバッグ情報付き）
"""
import sys
import os

def check_environment():
    """環境を確認"""
    print("=== 環境確認 ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # 必要なモジュールの確認
    try:
        import bcrypt
        print("✅ bcrypt: OK")
    except ImportError as e:
        print(f"❌ bcrypt: {e}")
        
    try:
        from jose import jwt
        print("✅ jose: OK")
    except ImportError as e:
        print(f"❌ jose: {e}")
        
    try:
        import fastapi
        print(f"✅ fastapi: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ fastapi: {e}")
    
    # 環境変数の確認
    print("\n=== 環境変数確認 ===")
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"✅ DATABASE_URL: {database_url[:50]}...")
    else:
        print("❌ DATABASE_URL: 設定されていません")
    
    jwt_secret = os.getenv("JWT_SECRET_KEY", "default")
    print(f"✅ JWT_SECRET_KEY: {jwt_secret[:10]}...")

if __name__ == "__main__":
    check_environment()
    print("\n=== FastAPIサーバー起動 ===")
    
    # FastAPIサーバーを起動
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)