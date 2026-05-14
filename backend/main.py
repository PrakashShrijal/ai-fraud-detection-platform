from fastapi import FastAPI

from backend.routes.transaction_routes import router
from backend.routes.websocket_routes import router as websocket_router
from backend.routes.auth_routes import router as auth_router

from backend.database.db import engine
from backend.models.transaction_db_model import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

app.include_router(websocket_router)

app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Fraud Detection Platform Running"
    }