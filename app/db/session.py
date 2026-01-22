import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from dotenv import load_dotenv

load_dotenv(verbose=True)

def create_postgres_engine():
    DATABASE_URL = f"{os.getenv("DATABASE_URL")}"
    return create_async_engine(DATABASE_URL)

engine = create_postgres_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session