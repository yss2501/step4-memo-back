from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.models.models import Coworker
from app.schemas.schemas import Coworker as CoworkerSchema, CoworkerCreate, SearchRequest, SearchResponse

router = APIRouter()

@router.post("/", response_model=CoworkerSchema)
async def create_coworker(coworker_data: CoworkerCreate, db: Session = Depends(get_db)):
    """社内メンバーの作成"""
    coworker = Coworker(**coworker_data.dict())
    db.add(coworker)
    db.commit()
    db.refresh(coworker)
    return coworker

@router.get("/", response_model=List[CoworkerSchema])
async def get_coworkers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """社内メンバー一覧の取得"""
    coworkers = db.query(Coworker).offset(skip).limit(limit).all()
    return coworkers

@router.post("/search", response_model=SearchResponse)
async def search_coworkers(search_data: SearchRequest, db: Session = Depends(get_db)):
    """社内メンバーの検索"""
    offset = (search_data.page - 1) * search_data.per_page
    
    # 名前で部分一致検索
    query = db.query(Coworker).filter(
        Coworker.name.ilike(f"%{search_data.keyword}%")
    )
    
    total = query.count()
    coworkers = query.offset(offset).limit(search_data.per_page).all()
    
    items = []
    for coworker in coworkers:
        items.append({
            "id": coworker.id,
            "name": coworker.name,
            "department": f"部署{coworker.department_id}" if coworker.department_id else "",
            "position": coworker.position or ""
        })
    
    return SearchResponse(
        items=items,
        total=total,
        page=search_data.page,
        per_page=search_data.per_page,
        total_pages=(total + search_data.per_page - 1) // search_data.per_page
    )

@router.get("/{coworker_id}", response_model=CoworkerSchema)
async def get_coworker(coworker_id: int, db: Session = Depends(get_db)):
    """社内メンバーの詳細取得"""
    coworker = db.query(Coworker).filter(Coworker.id == coworker_id).first()
    if not coworker:
        raise HTTPException(status_code=404, detail="社内メンバーが見つかりません")
    return coworker