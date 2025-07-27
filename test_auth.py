#!/usr/bin/env python3
"""
認証機能のテスト用スクリプト
"""
import asyncio
from app.utils.auth import get_password_hash, verify_password

def test_password_functions():
    """パスワード関数のテスト"""
    print("=== パスワード関数テスト ===")
    
    # テスト用パスワード
    plain_password = "password"
    
    # ハッシュ化
    print(f"元のパスワード: {plain_password}")
    hashed = get_password_hash(plain_password)
    print(f"ハッシュ化パスワード: {hashed}")
    
    # 検証
    is_valid = verify_password(plain_password, hashed)
    print(f"検証結果: {is_valid}")
    
    # 間違ったパスワードでテスト
    wrong_password = "wrong_password"
    is_invalid = verify_password(wrong_password, hashed)
    print(f"間違ったパスワードでの検証: {is_invalid}")
    
    return hashed

if __name__ == "__main__":
    test_password_functions()