from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.services.auth_service import get_current_user, oauth2_scheme
from typing import Annotated

from app.db.session import get_db

router = APIRouter()

@router.post("/register_user",response_model=UserResponse)
async def register_user(data: UserCreate,db: AsyncSession = Depends(get_db)):
        try:
            return await create_user(data.username, data.email, data.password, db)
        except Exception as e:
            raise HTTPException(status_code=400, detail="User creation failed")

@router.get("/user_details")
async def user_details(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return current_user