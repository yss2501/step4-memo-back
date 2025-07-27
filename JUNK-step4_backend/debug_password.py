#!/usr/bin/env python3
"""
パスワード検証の詳細デバッグスクリプト
"""
import os
import bcrypt
from dotenv import load_dotenv

def debug_password_verification():
    """パスワード検証の詳細をデバッグ"""
    load_dotenv()
    
    print("=== パスワード検証デバッグ ===")
    
    # テスト用データ
    test_password = "password"
    stored_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    
    print(f"入力パスワード: '{test_password}'")
    print(f"保存済みハッシュ: '{stored_hash}'")
    print(f"パスワード長: {len(test_password)}")
    print(f"ハッシュ長: {len(stored_hash)}")
    print(f"パスワード型: {type(test_password)}")
    print(f"ハッシュ型: {type(stored_hash)}")
    
    # bcryptの直接テスト
    print("\n=== bcryptの直接テスト ===")
    try:
        # パスワードをbytesに変換
        password_bytes = test_password.encode('utf-8')
        hash_bytes = stored_hash.encode('utf-8')
        
        print(f"パスワード(bytes): {password_bytes}")
        print(f"ハッシュ(bytes): {hash_bytes}")
        
        # bcrypt.checkpwを直接実行
        result = bcrypt.checkpw(password_bytes, hash_bytes)
        print(f"bcrypt.checkpw結果: {result}")
        
    except Exception as e:
        print(f"bcrypt.checkpwエラー: {e}")
    
    # 新しいハッシュを生成してテスト
    print("\n=== 新しいハッシュでのテスト ===")
    try:
        # 新しいハッシュを生成
        new_salt = bcrypt.gensalt()
        new_hash = bcrypt.hashpw(test_password.encode('utf-8'), new_salt)
        new_hash_str = new_hash.decode('utf-8')
        
        print(f"新しいハッシュ: {new_hash_str}")
        
        # 新しいハッシュで検証
        verify_result = bcrypt.checkpw(test_password.encode('utf-8'), new_hash)
        print(f"新しいハッシュでの検証: {verify_result}")
        
    except Exception as e:
        print(f"新しいハッシュ生成エラー: {e}")
    
    # auth.pyのverify_password関数をテスト
    print("\n=== auth.pyの関数テスト ===")
    try:
        from app.utils.auth import verify_password, get_password_hash
        
        # 現在の関数でテスト
        result = verify_password(test_password, stored_hash)
        print(f"verify_password結果: {result}")
        
        # 新しいハッシュを生成してテスト
        new_hash = get_password_hash(test_password)
        print(f"get_password_hash結果: {new_hash}")
        
        new_verify = verify_password(test_password, new_hash)
        print(f"新しいハッシュでのverify_password: {new_verify}")
        
    except Exception as e:
        print(f"auth.py関数エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_password_verification()