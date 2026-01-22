from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Order and Inventory Management API", version="1.0.0")

@app.get("/")
def main():
    return {"message": "Hello, World!"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0",    port=8888)