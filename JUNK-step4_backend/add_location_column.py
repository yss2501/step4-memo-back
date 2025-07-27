#!/usr/bin/env python3
"""
contactsテーブルにlocationカラムを追加するマイグレーションスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def add_location_column():
    """contactsテーブルにlocationカラムを追加"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        print("=== contactsテーブルの現在の構造を確認 ===")
        
        # テーブル構造を確認
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'contacts' 
            ORDER BY ordinal_position
        """))
        
        columns = result.fetchall()
        location_exists = False
        
        print("現在のカラム:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]}, nullable: {col[2]})")
            if col[0] == 'location':
                location_exists = True
        
        if location_exists:
            print("\n✅ locationカラムは既に存在します")
            return
        
        print("\n=== locationカラムを追加 ===")
        
        try:
            # locationカラムを追加
            db.execute(text("""
                ALTER TABLE contacts 
                ADD COLUMN location VARCHAR(255)
            """))
            
            db.commit()
            print("✅ locationカラムを正常に追加しました")
            
            # 追加後の確認
            print("\n=== 追加後の確認 ===")
            result = db.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'contacts' AND column_name = 'location'
            """))
            
            location_col = result.fetchone()
            if location_col:
                print(f"✅ location カラムが追加されました: {location_col[0]} ({location_col[1]}, nullable: {location_col[2]})")
            else:
                print("❌ locationカラムの追加に失敗しました")
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            db.rollback()

if __name__ == "__main__":
    try:
        add_location_column()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()