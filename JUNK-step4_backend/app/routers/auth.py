from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import AuthUser, Coworker
from app.schemas.schemas import LoginRequest, LoginResponse
from app.utils.auth import verify_password, create_access_token
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """ログイン処理"""
    # ユーザーの検索（coworker_idで検索）
    auth_user = db.query(AuthUser).join(Coworker).filter(
        Coworker.id == login_data.user_id
    ).first()
    
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ログインできませんでした"
        )
    
    # パスワード検証
    if not verify_password(login_data.password, auth_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ログインできませんでした"
        )
    
    # 最終ログイン日時の更新
    auth_user.last_login = datetime.utcnow()
    db.commit()
    
    # JWTトークンの作成
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(auth_user.coworker.id)}, 
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=auth_user.coworker
    )

@router.post("/logout")
async def logout():
    """ログアウト処理"""
    return {"message": "ログアウトしました"}