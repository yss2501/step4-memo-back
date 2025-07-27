from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

# 面談-担当者関連テーブル（多対多）
contact_person_table = Table(
    'contact_person',
    Base.metadata,
    Column('contact_id', Integer, ForeignKey('contacts.id', ondelete='CASCADE'), primary_key=True),
    Column('business_card_id', Integer, ForeignKey('business_cards.id', ondelete='CASCADE'), primary_key=True)
)

# 面談-同席者関連テーブル（多対多）
contact_companions_table = Table(
    'contact_companions',
    Base.metadata,
    Column('contact_id', Integer, ForeignKey('contacts.id', ondelete='CASCADE'), primary_key=True),
    Column('coworker_id', Integer, ForeignKey('coworkers.id', ondelete='CASCADE'), primary_key=True)
)

class BusinessCard(Base):
    """名刺テーブル（外部担当者情報）"""
    __tablename__ = "business_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    department = Column(String(255))
    position = Column(String(255))
    memo = Column(Text)
    
    # リレーション
    contacts = relationship("Contact", secondary=contact_person_table, back_populates="persons")

class Coworker(Base):
    """社内メンバーテーブル"""
    __tablename__ = "coworkers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    position = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    sso_id = Column(String(255), unique=True)
    department_id = Column(Integer, index=True)
    
    # リレーション
    auth_user = relationship("AuthUser", back_populates="coworker", uselist=False)
    created_contacts = relationship("Contact", back_populates="coworker")
    attended_contacts = relationship("Contact", secondary=contact_companions_table, back_populates="companions")

class AuthUser(Base):
    """認証ユーザーテーブル"""
    __tablename__ = "auth_users"
    
    id = Column(Integer, primary_key=True, index=True)
    coworker_id = Column(Integer, ForeignKey("coworkers.id", ondelete="CASCADE"), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime)
    
    # リレーション
    coworker = relationship("Coworker", back_populates="auth_user")

class Contact(Base):
    """面談記録テーブル（メイン）"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_date = Column(Date)
    location = Column(String(255))  # 面談場所
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String(255))
    summary_text = Column(Text)
    raw_text = Column(Text)
    details = Column(Text)
    status = Column(Integer, nullable=False, default=0, index=True)  # 1:保存完了、0:一時保存、9:破棄
    department_id = Column(Integer, index=True)
    coworker_id = Column(Integer, ForeignKey("coworkers.id"), index=True)
    
    # リレーション
    coworker = relationship("Coworker", back_populates="created_contacts")
    persons = relationship("BusinessCard", secondary=contact_person_table, back_populates="contacts")
    companions = relationship("Coworker", secondary=contact_companions_table, back_populates="attended_contacts")