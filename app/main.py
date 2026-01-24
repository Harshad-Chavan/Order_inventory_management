from fastapi import FastAPI
from app.api.routes import health_check, user, auth
from app.core.settings import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.include_router(health_check.router, prefix="/health_check", tags=["health_check"])
app.include_router(user.router, prefix="/user", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
