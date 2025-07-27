#!/usr/bin/env python3
"""
contactsテーブルの制約を修正するスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def fix_contacts_constraints():
    """contactsテーブルの制約を仕様書に合わせて修正"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        print("=== contactsテーブルの制約を確認 ===")
        
        # 制約の確認
        result = db.execute(text("""
            SELECT column_name, is_nullable, data_type
            FROM information_schema.columns 
            WHERE table_name = 'contacts'
            ORDER BY ordinal_position
        """))
        
        columns = result.fetchall()
        for col in columns:
            print(f"  {col[0]}: nullable={col[1]}, type={col[2]}")
        
        print("\n=== 不要なカラムの削除と制約の修正 ===")
        
        try:
            # business_card_idカラムを削除（contact_personテーブルで管理）
            print("business_card_id カラムを削除中...")
            db.execute(text("ALTER TABLE contacts DROP COLUMN IF EXISTS business_card_id"))
            print("✅ business_card_id カラムを削除しました")
            
            # coworker_idをNULLABLEに変更
            print("coworker_id制約を変更中...")
            db.execute(text("ALTER TABLE contacts ALTER COLUMN coworker_id DROP NOT NULL"))
            print("✅ coworker_id制約を変更しました")
            
            db.commit()
            print("\n✅ 制約の修正が完了しました")
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            db.rollback()
            raise
        
        # 修正後の確認
        print("\n=== 修正後の確認 ===")
        result = db.execute(text("""
            SELECT column_name, is_nullable, data_type
            FROM information_schema.columns 
            WHERE table_name = 'contacts'
            ORDER BY ordinal_position
        """))
        
        print("修正後のカラム:")
        for col in result.fetchall():
            print(f"  {col[0]}: nullable={col[1]}, type={col[2]}")

if __name__ == "__main__":
    try:
        fix_contacts_constraints()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()