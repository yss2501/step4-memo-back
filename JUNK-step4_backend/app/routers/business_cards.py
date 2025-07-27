from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.database.connection import get_db
from app.models.models import BusinessCard
from app.schemas.schemas import BusinessCard as BusinessCardSchema, BusinessCardCreate, SearchRequest, SearchResponse

router = APIRouter()

@router.post("/", response_model=BusinessCardSchema)
async def create_business_card(card_data: BusinessCardCreate, db: Session = Depends(get_db)):
    """名刺情報の作成"""
    card = BusinessCard(**card_data.dict())
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@router.get("/", response_model=List[BusinessCardSchema])
async def get_business_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """名刺一覧の取得"""
    cards = db.query(BusinessCard).offset(skip).limit(limit).all()
    return cards

@router.post("/search", response_model=SearchResponse)
async def search_business_cards(search_data: SearchRequest, db: Session = Depends(get_db)):
    """外部担当者の検索"""
    offset = (search_data.page - 1) * search_data.per_page
    
    # 名前または会社名で部分一致検索
    query = db.query(BusinessCard).filter(
        or_(
            BusinessCard.name.ilike(f"%{search_data.keyword}%"),
            BusinessCard.company.ilike(f"%{search_data.keyword}%")
        )
    )
    
    total = query.count()
    cards = query.offset(offset).limit(search_data.per_page).all()
    
    items = []
    for card in cards:
        items.append({
            "id": card.id,
            "name": card.name,
            "company": card.company,
            "department": card.department or "",
            "position": card.position or ""
        })
    
    return SearchResponse(
        items=items,
        total=total,
        page=search_data.page,
        per_page=search_data.per_page,
        total_pages=(total + search_data.per_page - 1) // search_data.per_page
    )

@router.get("/{card_id}", response_model=BusinessCardSchema)
async def get_business_card(card_id: int, db: Session = Depends(get_db)):
    """名刺情報の詳細取得"""
    card = db.query(BusinessCard).filter(BusinessCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="名刺が見つかりません")
    return card