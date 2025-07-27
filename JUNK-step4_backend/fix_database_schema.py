#!/usr/bin/env python3
"""
データベーススキーマを修正するスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def fix_database_schema():
    """データベーススキーマを仕様書と一致させる"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        print("=== contactsテーブルの現在の構造を確認 ===")
        
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'contacts' 
            ORDER BY ordinal_position
        """))
        
        current_columns = {col[0]: (col[1], col[2]) for col in result.fetchall()}
        
        print("現在のカラム:")
        for col_name, (data_type, nullable) in current_columns.items():
            print(f"  - {col_name} ({data_type}, nullable: {nullable})")
        
        # 必要なカラムを定義
        required_columns = {
            'id': 'integer',
            'contact_date': 'date', 
            'location': 'character varying(255)',
            'created_at': 'timestamp without time zone',
            'title': 'character varying(255)',
            'summary_text': 'text',
            'raw_text': 'text',
            'details': 'text',  # 追加が必要
            'status': 'integer',
            'department_id': 'integer',
            'coworker_id': 'integer'
        }
        
        print("\n=== 不足しているカラムを追加 ===")
        
        changes_made = False
        
        for col_name, expected_type in required_columns.items():
            if col_name not in current_columns:
                print(f"追加: {col_name} ({expected_type})")
                try:
                    if col_name == 'details':
                        db.execute(text("ALTER TABLE contacts ADD COLUMN details TEXT"))
                    elif col_name == 'location':
                        db.execute(text("ALTER TABLE contacts ADD COLUMN location VARCHAR(255)"))
                    elif col_name == 'title' and 'title' not in current_columns:
                        db.execute(text("ALTER TABLE contacts ADD COLUMN title VARCHAR(255)"))
                    
                    changes_made = True
                    print(f"✅ {col_name} カラムを追加しました")
                except Exception as e:
                    print(f"❌ {col_name} カラムの追加に失敗: {e}")
        
        # title カラムのデータ型を修正（TEXTからVARCHAR(255)に）
        if 'title' in current_columns:
            current_title_type = current_columns['title'][0]
            if current_title_type == 'text':
                print("title カラムの型をTEXTからVARCHAR(255)に変更中...")
                try:
                    db.execute(text("ALTER TABLE contacts ALTER COLUMN title TYPE VARCHAR(255)"))
                    changes_made = True
                    print("✅ title カラムの型を変更しました")
                except Exception as e:
                    print(f"❌ title カラムの型変更に失敗: {e}")
        
        if changes_made:
            db.commit()
            print("\n✅ データベーススキーマを更新しました")
        else:
            print("\n✅ スキーマは既に最新です")
        
        # 更新後の確認
        print("\n=== 更新後の確認 ===")
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'contacts' 
            ORDER BY ordinal_position
        """))
        
        print("更新後のカラム:")
        for col in result.fetchall():
            print(f"  - {col[0]} ({col[1]}, nullable: {col[2]})")

if __name__ == "__main__":
    try:
        fix_database_schema()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()