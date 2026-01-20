from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory



@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGO_DB_URI)
    app.db_client = app.mongodb_conn[settings.MONGO_DB_NAME]
    
    llm_provider_factory =  LLMProviderFactory(settings)

    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.get_generation_model(model_id=settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.generation_client.get_embedding_model(model_id=settings.EMBEDING_MODEL_ID,
                                              embedding_size = settings.EMBEDING_MODEL_SIZE)
    
    yield
    app.mongodb_conn.close()

# Initialize FastAPI with the lifespan handler
app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)