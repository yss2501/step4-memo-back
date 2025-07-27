#!/usr/bin/env python3
"""
.envファイルのDATABASE_URLを修正するスクリプト
"""
import os
import re

def fix_database_url():
    """DATABASE_URLを修正"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print("❌ .envファイルが見つかりません")
        return
    
    # .envファイルを読み込み
    with open(env_file, 'r') as f:
        content = f.read()
    
    print("=== 現在の.env内容 ===")
    print(content)
    
    # DATABASE_URLを修正
    # パスワード内の特殊文字をURLエンコード
    new_content = re.sub(
        r'DATABASE_URL=postgresql://([^:]+):([^@]+)@([^/]+)/(.+)',
        r'DATABASE_URL=postgresql://\1:tech0-junk%21@\3/\4?sslmode=require',
        content
    )
    
    # 変更があった場合のみ保存
    if new_content != content:
        # バックアップを作成
        with open(f"{env_file}.backup", 'w') as f:
            f.write(content)
        
        # 新しい内容を保存
        with open(env_file, 'w') as f:
            f.write(new_content)
        
        print("\n=== 修正後の.env内容 ===")
        print(new_content)
        print("✅ .envファイルを修正しました（バックアップ: .env.backup）")
    else:
        print("❌ 修正が必要な形式が見つかりませんでした")

if __name__ == "__main__":
    fix_database_url()