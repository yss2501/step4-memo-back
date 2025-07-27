#!/usr/bin/env python3
"""
データベースのパスワードハッシュを修正するスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def fix_password_hashes():
    """パスワードハッシュを正しいものに更新"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 正しいパスワードハッシュ（"password"のbcryptハッシュ）
    correct_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    
    with SessionLocal() as db:
        print("=== パスワードハッシュ修正 ===")
        
        # 全てのauth_userのパスワードを更新
        result = db.execute(text("""
            UPDATE auth_users 
            SET password_hash = :hash
        """), {"hash": correct_hash})
        
        affected_rows = result.rowcount
        db.commit()
        
        print(f"✅ {affected_rows}行のパスワードハッシュを更新しました")
        
        # 確認
        print("\n=== 更新後の確認 ===")
        result = db.execute(text("""
            SELECT au.id, au.coworker_id, c.name, 
                   LEFT(au.password_hash, 30) as hash_preview
            FROM auth_users au 
            JOIN coworkers c ON au.coworker_id = c.id
            LIMIT 5
        """))
        
        for row in result:
            print(f"ID:{row[1]} {row[2]}: {row[3]}...")

if __name__ == "__main__":
    try:
        fix_password_hashes()
        print("\n✅ 修正完了！これで全ユーザーのパスワードが 'password' になりました。")
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()