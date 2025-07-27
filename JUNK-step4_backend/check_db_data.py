#!/usr/bin/env python3
"""
データベースのデータ確認スクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def check_database_data():
    """データベースのデータを確認"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        print("=== データベース内容確認 ===")
        
        # coworkersテーブル
        print("\n1. coworkersテーブル:")
        result = db.execute(text("SELECT id, name, email, department_id FROM coworkers"))
        coworkers = result.fetchall()
        if coworkers:
            for row in coworkers:
                print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Dept: {row[3]}")
        else:
            print("  ❌ データが見つかりません")
        
        # auth_usersテーブル
        print("\n2. auth_usersテーブル:")
        result = db.execute(text("SELECT id, coworker_id, password_hash FROM auth_users"))
        auth_users = result.fetchall()
        if auth_users:
            for row in auth_users:
                print(f"  ID: {row[0]}, Coworker_ID: {row[1]}, Hash: {row[2][:20]}...")
        else:
            print("  ❌ データが見つかりません")
        
        # JOINクエリのテスト
        print("\n3. JOIN クエリテスト (auth_users + coworkers):")
        result = db.execute(text("""
            SELECT au.id, au.coworker_id, c.name, c.email 
            FROM auth_users au 
            JOIN coworkers c ON au.coworker_id = c.id
        """))
        joined_data = result.fetchall()
        if joined_data:
            for row in joined_data:
                print(f"  AuthUser ID: {row[0]}, Coworker ID: {row[1]}, Name: {row[2]}, Email: {row[3]}")
        else:
            print("  ❌ JOINデータが見つかりません")

if __name__ == "__main__":
    try:
        check_database_data()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()