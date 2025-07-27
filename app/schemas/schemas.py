from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

# 基本スキーマ
class BusinessCardBase(BaseModel):
    name: str
    company: str
    department: Optional[str] = None
    position: Optional[str] = None
    memo: Optional[str] = None

class BusinessCardCreate(BusinessCardBase):
    pass

class BusinessCard(BusinessCardBase):
    id: int
    
    class Config:
        from_attributes = True

class CoworkerBase(BaseModel):
    name: str
    position: Optional[str] = None
    email: str
    sso_id: Optional[str] = None
    department_id: Optional[int] = None

class CoworkerCreate(CoworkerBase):
    pass

class Coworker(CoworkerBase):
    id: int
    
    class Config:
        from_attributes = True

class AuthUserCreate(BaseModel):
    coworker_id: int
    password: str

class AuthUser(BaseModel):
    id: int
    coworker_id: int
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    contact_date: Optional[date] = None
    location: Optional[str] = None
    title: Optional[str] = None
    summary_text: Optional[str] = None
    raw_text: Optional[str] = None
    details: Optional[str] = None
    status: int = 0
    department_id: Optional[int] = None

class ContactCreate(ContactBase):
    person_ids: List[int] = []
    companion_ids: List[int] = []

class ContactUpdate(ContactBase):
    person_ids: Optional[List[int]] = None
    companion_ids: Optional[List[int]] = None

class Contact(ContactBase):
    id: int
    coworker_id: Optional[int] = None
    created_at: datetime
    persons: List[BusinessCard] = []
    companions: List[Coworker] = []
    coworker: Optional[Coworker] = None
    
    class Config:
        from_attributes = True

# 認証関連
class LoginRequest(BaseModel):
    user_id: int
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: Coworker

# 検索関連
class SearchRequest(BaseModel):
    keyword: str
    page: int = 1
    per_page: int = 5

class SearchResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    per_page: int
    total_pages: int

# OpenAI要約関連
class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str