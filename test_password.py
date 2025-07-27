#!/usr/bin/env python3
"""
パスワード検証のテストスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import AuthUser, Coworker
from app.utils.auth import verify_password, get_password_hash

def test_password_verification():
    """パスワード検証をテスト"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        print("=== パスワード検証テスト ===")
        
        # 正しいハッシュを生成
        test_password = "password"
        correct_hash = get_password_hash(test_password)
        print(f"正しいハッシュ: {correct_hash}")
        
        # データベース内の全ハッシュをテスト
        auth_users = db.query(AuthUser).join(Coworker).all()
        
        for auth_user in auth_users:
            coworker_id = auth_user.coworker.id
            coworker_name = auth_user.coworker.name
            stored_hash = auth_user.password_hash
            
            # パスワード検証
            is_valid = verify_password(test_password, stored_hash)
            
            status = "✅" if is_valid else "❌"
            print(f"{status} ID:{coworker_id} ({coworker_name}): {stored_hash[:30]}... -> {is_valid}")

if __name__ == "__main__":
    try:
        test_password_verification()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()