from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from typing import Annotated
from app.models.auth import RefreshToken
from app.models.user import User
from app.services.auth_service import oauth2_scheme
from app.db.session import get_db
from app.services.user_service import authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.core.security import create_access_token, create_refresh_token
from datetime import datetime

router = APIRouter()

@router.post('/login', response_model=Token)
async def login_get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user.username)
    refresh_token = create_refresh_token(data=user.id)

    db.add(
        RefreshToken(
            **refresh_token,
        )
    )

    await db.commit()

    return {
        "access_token": token,
        "refresh_token": refresh_token["token"],
        "token_type": "bearer"
    }

@router.get('/get_token_info')
async def get_token_info(token : Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.revoked == False,
        )
    )

    token_db = result.scalar_one_or_none()

    if not token_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_db.expires_at < datetime.now(tz=token_db.expires_at.tzinfo):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user_result = await db.execute(
        select(User).where(User.id == token_db.user_id)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(subject=user.username)

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }