from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, contacts, business_cards, coworkers
from app.database.connection import engine, Base
from app.routers.auth import router as auth_router

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="面談アプリ API",
    description="外部面談を管理するためのAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Next.jsの開発サーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの追加
app.include_router(auth.router, prefix="/api/auth", tags=["認証"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["面談記録"])
app.include_router(business_cards.router, prefix="/api/business-cards", tags=["名刺"])
app.include_router(coworkers.router, prefix="/api/coworkers", tags=["社内メンバー"])

@app.get("/")
async def root():
    return {"message": "面談アプリ API サーバーが起動中です"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug/db")
async def debug_db():
    """データベース接続のデバッグ"""
    try:
        from app.database.connection import SessionLocal
        from app.models.models import Coworker, AuthUser
        
        with SessionLocal() as db:
            coworker_count = db.query(Coworker).count()
            auth_user_count = db.query(AuthUser).count()
            
            return {
                "status": "ok",
                "coworkers": coworker_count,
                "auth_users": auth_user_count
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__
        }

@app.get("/debug/auth")
async def debug_auth():
    """認証モジュールのデバッグ"""
    try:
        from app.utils.auth import get_password_hash, verify_password
        
        test_password = "password"
        hashed = get_password_hash(test_password)
        is_valid = verify_password(test_password, hashed)
        
        return {
            "status": "ok",
            "password_hash_test": is_valid,
            "hash_length": len(hashed)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__
        }