#!/usr/bin/env python3
"""
APIエンドポイントのテスト用スクリプト
"""
import sys
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def test_database_connection():
    """データベース接続のテスト"""
    print("=== データベース接続テスト ===")
    try:
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            print("❌ DATABASE_URL環境変数が設定されていません")
            return False
            
        print(f"DATABASE_URL: {database_url[:50]}...")
        
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1 as test"))
            print(f"✅ データベース接続成功: {result.fetchone()}")
            
            # テーブルの存在確認
            tables = ['coworkers', 'auth_users', 'business_cards', 'contacts']
            for table in tables:
                try:
                    result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"✅ {table}テーブル: {count}行")
                except Exception as e:
                    print(f"❌ {table}テーブルエラー: {e}")
        return True
        
    except Exception as e:
        print(f"❌ データベース接続エラー: {e}")
        traceback.print_exc()
        return False

def test_auth_modules():
    """認証モジュールのテスト"""
    print("\n=== 認証モジュールテスト ===")
    try:
        import bcrypt
        print("✅ bcrypt: OK")
        
        from jose import jwt
        print("✅ jose: OK")
        
        from app.utils.auth import get_password_hash, verify_password, create_access_token
        print("✅ auth utils: OK")
        
        # パスワードハッシュのテスト
        test_password = "password"
        hashed = get_password_hash(test_password)
        is_valid = verify_password(test_password, hashed)
        print(f"✅ パスワード検証: {is_valid}")
        
        # JWTトークンのテスト
        token = create_access_token(data={"sub": "1"})
        print(f"✅ JWTトークン生成: {token[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 認証モジュールエラー: {e}")
        traceback.print_exc()
        return False

def test_models():
    """モデルのテスト"""
    print("\n=== モデルテスト ===")
    try:
        from app.models.models import AuthUser, Coworker, BusinessCard, Contact
        print("✅ モデルインポート: OK")
        
        from app.database.connection import get_db, SessionLocal
        print("✅ データベース依存関係: OK")
        
        # 実際のデータ取得テスト
        with SessionLocal() as db:
            coworker = db.query(Coworker).first()
            if coworker:
                print(f"✅ Coworkerデータ取得: {coworker.name}")
            else:
                print("❌ Coworkerデータが見つかりません")
                
            auth_user = db.query(AuthUser).first()
            if auth_user:
                print(f"✅ AuthUserデータ取得: ID {auth_user.id}")
            else:
                print("❌ AuthUserデータが見つかりません")
        
        return True
        
    except Exception as e:
        print(f"❌ モデルエラー: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("FastAPI エラー診断スクリプト")
    print("=" * 40)
    
    # 各テストを実行
    db_ok = test_database_connection()
    auth_ok = test_auth_modules()
    model_ok = test_models()
    
    print("\n=== 診断結果 ===")
    print(f"データベース接続: {'✅' if db_ok else '❌'}")
    print(f"認証モジュール: {'✅' if auth_ok else '❌'}")
    print(f"モデル: {'✅' if model_ok else '❌'}")
    
    if not (db_ok and auth_ok and model_ok):
        print("\n❌ エラーが検出されました。上記のエラー内容を確認してください。")
        sys.exit(1)
    else:
        print("\n✅ 全てのテストが正常です。")