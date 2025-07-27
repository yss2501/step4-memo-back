from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from app.database.connection import get_db
from app.models.models import Contact, BusinessCard, Coworker
from sqlalchemy.orm import joinedload
from app.schemas.schemas import Contact as ContactSchema, ContactCreate, ContactUpdate, SearchRequest, SearchResponse, SummaryRequest, SummaryResponse
from app.services.openai_service import summarize_meeting_content
from app.utils.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=ContactSchema)
async def create_contact(contact_data: ContactCreate, current_user: Coworker = Depends(get_current_user), db: Session = Depends(get_db)):
    """新規面談記録の作成"""
    # 面談記録の作成
    contact = Contact(
        contact_date=contact_data.contact_date,
        location=contact_data.location,
        title=contact_data.title,
        summary_text=contact_data.summary_text,
        raw_text=contact_data.raw_text,
        details=contact_data.details,
        status=contact_data.status,
        department_id=current_user.department_id,
        coworker_id=current_user.id
    )
    
    db.add(contact)
    db.flush()  # IDを取得するためにflush
    
    # 担当者の関連付け
    if contact_data.person_ids:
        persons = db.query(BusinessCard).filter(BusinessCard.id.in_(contact_data.person_ids)).all()
        contact.persons = persons
    
    # 同席者の関連付け
    if contact_data.companion_ids:
        companions = db.query(Coworker).filter(Coworker.id.in_(contact_data.companion_ids)).all()
        contact.companions = companions
    
    db.commit()
    db.refresh(contact)
    
    # リレーションデータを含めて再取得
    contact = db.query(Contact).options(
        joinedload(Contact.coworker),
        joinedload(Contact.persons),
        joinedload(Contact.companions)
    ).filter(Contact.id == contact.id).first()
    
    return contact

@router.put("/{contact_id}", response_model=ContactSchema)
async def update_contact(contact_id: int, contact_data: ContactUpdate, current_user: Coworker = Depends(get_current_user), db: Session = Depends(get_db)):
    """面談記録の更新"""
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.coworker_id == current_user.id)
    ).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="面談記録が見つかりません")
    
    # データの更新
    for field, value in contact_data.dict(exclude_unset=True, exclude={'person_ids', 'companion_ids'}).items():
        setattr(contact, field, value)
    
    # 担当者の更新
    if contact_data.person_ids is not None:
        persons = db.query(BusinessCard).filter(BusinessCard.id.in_(contact_data.person_ids)).all()
        contact.persons = persons
    
    # 同席者の更新
    if contact_data.companion_ids is not None:
        companions = db.query(Coworker).filter(Coworker.id.in_(contact_data.companion_ids)).all()
        contact.companions = companions
    
    db.commit()
    db.refresh(contact)
    
    # リレーションデータを含めて再取得
    contact = db.query(Contact).options(
        joinedload(Contact.coworker),
        joinedload(Contact.persons),
        joinedload(Contact.companions)
    ).filter(Contact.id == contact.id).first()
    
    return contact

@router.get("/drafts", response_model=List[ContactSchema])
async def get_drafts(current_user: Coworker = Depends(get_current_user), page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    """下書き一覧の取得"""
    offset = (page - 1) * per_page
    
    drafts = db.query(Contact).options(
        joinedload(Contact.coworker),
        joinedload(Contact.persons),
        joinedload(Contact.companions)
    ).filter(
        and_(Contact.coworker_id == current_user.id, Contact.status == 0)
    ).order_by(Contact.contact_date.desc()).offset(offset).limit(per_page).all()
    
    return drafts

@router.get("/history", response_model=List[ContactSchema])
async def get_history(current_user: Coworker = Depends(get_current_user), page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    """作成履歴の取得"""
    offset = (page - 1) * per_page
    
    history = db.query(Contact).options(
        joinedload(Contact.coworker),
        joinedload(Contact.persons),
        joinedload(Contact.companions)
    ).filter(
        and_(Contact.coworker_id == current_user.id, Contact.status == 1)
    ).order_by(Contact.contact_date.desc()).offset(offset).limit(per_page).all()
    
    return history

@router.post("/search", response_model=List[ContactSchema])
async def search_contacts(search_data: SearchRequest, current_user: Coworker = Depends(get_current_user), db: Session = Depends(get_db)):
    """面談記録の検索"""
    offset = (search_data.page - 1) * search_data.per_page
    
    # 検索クエリの構築
    query = db.query(Contact).options(
        joinedload(Contact.coworker),
        joinedload(Contact.persons),
        joinedload(Contact.companions)
    ).filter(
        and_(
            Contact.department_id == current_user.department_id,
            Contact.status == 1,
            or_(
                Contact.title.ilike(f"%{search_data.keyword}%"),
                Contact.persons.any(BusinessCard.name.ilike(f"%{search_data.keyword}%"))
            )
        )
    ).order_by(Contact.contact_date.desc())
    
    contacts = query.offset(offset).limit(search_data.per_page).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactSchema)
async def get_contact(contact_id: int, current_user: Coworker = Depends(get_current_user), db: Session = Depends(get_db)):
    """面談記録の詳細取得"""
    contact = db.query(Contact).options(
        joinedload(Contact.coworker),
        joinedload(Contact.persons),
        joinedload(Contact.companions)
    ).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="面談記録が見つかりません")
    
    # 部署単位での閲覧権限チェック
    if contact.department_id != current_user.department_id and contact.coworker_id != current_user.id:
        raise HTTPException(status_code=403, detail="閲覧権限がありません")
    
    return contact

@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, current_user: Coworker = Depends(get_current_user), db: Session = Depends(get_db)):
    """面談記録の削除（status=9に設定）"""
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.coworker_id == current_user.id)
    ).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="面談記録が見つかりません")
    
    contact.status = 9
    db.commit()
    
    return {"message": "面談記録を破棄しました"}

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_content(summary_data: SummaryRequest):
    """OpenAIによる面談内容の要約"""
    if not summary_data.text or not summary_data.text.strip():
        raise HTTPException(status_code=400, detail="要約する内容が入力されていません")
    
    if len(summary_data.text) > 10000:
        raise HTTPException(status_code=400, detail="入力テキストが長すぎます（10,000文字以下にしてください）")
    
    try:
        summary = await summarize_meeting_content(summary_data.text)
        return SummaryResponse(summary=summary)
    except Exception as e:
        # ログ出力
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"要約生成エラー: {str(e)}")
        
        raise HTTPException(status_code=500, detail=f"要約の生成に失敗しました: {str(e)}")