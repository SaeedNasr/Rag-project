from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGO_DB_URI)
    app.db_client = app.mongodb_conn[settings.MONGO_DB_NAME]
    
    yield
    app.mongodb_conn.close()

# Initialize FastAPI with the lifespan handler
app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)