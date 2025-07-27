#!/usr/bin/env python3
"""
データベースのパスワードハッシュを正しく修正するスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt

def fix_password_hashes_correctly():
    """パスワードハッシュを正しく生成して更新"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 正しいパスワードハッシュを生成
    test_password = "password"
    salt = bcrypt.gensalt()
    correct_hash = bcrypt.hashpw(test_password.encode('utf-8'), salt)
    correct_hash_str = correct_hash.decode('utf-8')
    
    print("=== 正しいパスワードハッシュを生成 ===")
    print(f"パスワード: '{test_password}'")
    print(f"新しいハッシュ: {correct_hash_str}")
    
    # 検証テスト
    verify_test = bcrypt.checkpw(test_password.encode('utf-8'), correct_hash)
    print(f"検証テスト: {verify_test}")
    
    if not verify_test:
        print("❌ ハッシュ生成に問題があります")
        return
    
    with SessionLocal() as db:
        print("\n=== データベース更新 ===")
        
        # 全てのauth_userのパスワードを更新
        result = db.execute(text("""
            UPDATE auth_users 
            SET password_hash = :hash
        """), {"hash": correct_hash_str})
        
        affected_rows = result.rowcount
        db.commit()
        
        print(f"✅ {affected_rows}行のパスワードハッシュを更新しました")
        
        # 確認
        print("\n=== 更新後の確認 ===")
        result = db.execute(text("""
            SELECT au.id, au.coworker_id, c.name, au.password_hash
            FROM auth_users au 
            JOIN coworkers c ON au.coworker_id = c.id
            LIMIT 3
        """))
        
        for row in result:
            stored_hash = row[3]
            # 実際に検証してみる
            verify_result = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8'))
            status = "✅" if verify_result else "❌"
            print(f"{status} ID:{row[1]} {row[2]}: 検証結果={verify_result}")

if __name__ == "__main__":
    try:
        fix_password_hashes_correctly()
        print("\n✅ 修正完了！全ユーザーのパスワードが正しく 'password' に設定されました。")
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()