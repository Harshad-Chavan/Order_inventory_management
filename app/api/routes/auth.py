from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from typing import Annotated
from app.services.auth_service import oauth2_scheme
from app.db.session import get_db
from app.services.user_service import authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.core.security import create_access_token

router = APIRouter()

@router.post('/login', response_model=Token)
async def login_get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user.username)
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get('/get_token_info')
async def get_token_info(token : Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
