#!/usr/bin/env python3
"""
ログインクエリのテストスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import AuthUser, Coworker

def test_login_query():
    """ログインクエリをテスト"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        # テストするユーザーID
        test_user_ids = [1, 2, 3, 4, 5]
        
        print("=== ログインクエリテスト ===")
        
        for user_id in test_user_ids:
            print(f"\n--- ユーザーID: {user_id} ---")
            
            # 現在のauth.pyと同じクエリ
            auth_user = db.query(AuthUser).join(Coworker).filter(
                Coworker.id == user_id
            ).first()
            
            if auth_user:
                print(f"✅ AuthUser found: ID={auth_user.id}, CoworkerID={auth_user.coworker_id}")
                print(f"   Coworker: {auth_user.coworker.name} ({auth_user.coworker.email})")
                print(f"   Password hash: {auth_user.password_hash[:30]}...")
            else:
                print(f"❌ AuthUser not found for user_id {user_id}")
                
                # 直接coworkerを検索
                coworker = db.query(Coworker).filter(Coworker.id == user_id).first()
                if coworker:
                    print(f"   Coworker exists: {coworker.name}")
                else:
                    print(f"   Coworker not found")
                
                # 直接auth_userを検索
                auth_user_direct = db.query(AuthUser).filter(AuthUser.coworker_id == user_id).first()
                if auth_user_direct:
                    print(f"   AuthUser exists with coworker_id={user_id}: {auth_user_direct.id}")
                else:
                    print(f"   No AuthUser with coworker_id={user_id}")

if __name__ == "__main__":
    try:
        test_login_query()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()