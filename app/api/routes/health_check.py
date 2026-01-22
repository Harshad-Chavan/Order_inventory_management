from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import APIRouter

from app.db.session import get_db

router = APIRouter()

@router.get("/app")
def health_check_app():
    return {"message": "System is running,API is healthy"}

@router.get("/db")
async def health_check_app(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="DB connection failed")
