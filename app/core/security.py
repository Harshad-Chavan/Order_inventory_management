import datetime
from app.core.settings import settings
from pwdlib import PasswordHash
from jose import jwt

# Tuned for web apps (OWASP-friendly defaults)
password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password,hashed_password)

def create_access_token(subject: str) -> str:
    now = datetime.datetime.utcnow()
    expire = now + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire, "iat": now}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
