from fastapi import FastAPI
from app.api.routes import health_check

app = FastAPI(title="Order and Inventory Management API", version="1.0.0")

app.include_router(health_check.router, prefix="/health_check", tags=["health_check"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
