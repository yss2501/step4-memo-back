#!/usr/bin/env python3
"""
locationフィールドのテストスクリプト
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Contact, Coworker
from datetime import datetime, date

def test_location_field():
    """locationフィールドをテスト"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        print("=== locationフィールドテスト ===")
        
        # テスト用のContactレコードを作成
        test_contact = Contact(
            contact_date=date.today(),
            location="テスト会議室A",  # locationフィールドのテスト
            title="テスト面談",
            summary_text="テスト用の要約",
            raw_text="テスト用の詳細内容",
            status=0,  # 下書き
            department_id=1,
            coworker_id=1
        )
        
        try:
            # データベースに保存
            db.add(test_contact)
            db.commit()
            db.refresh(test_contact)
            
            print(f"✅ テストContactを作成: ID={test_contact.id}")
            print(f"   Location: {test_contact.location}")
            print(f"   Title: {test_contact.title}")
            
            # データを取得して確認
            saved_contact = db.query(Contact).filter(Contact.id == test_contact.id).first()
            if saved_contact and saved_contact.location == "テスト会議室A":
                print("✅ locationフィールドが正常に保存・取得されました")
            else:
                print(f"❌ locationフィールドの保存に問題があります: {saved_contact.location if saved_contact else 'None'}")
            
            # テストデータを削除
            db.delete(test_contact)
            db.commit()
            print("✅ テストデータを削除しました")
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            db.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        test_location_field()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()