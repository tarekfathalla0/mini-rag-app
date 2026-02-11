from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongodb_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)
    vector_db_provider_factory = VectorDBProviderFactory(settings)

    # generation provider
    app.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)
    # embedding provider
    app.embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_SIZE)

    # vector db provider
    app.vector_db_client = vector_db_provider_factory.create(settings.VECTOR_DB_BACKEND)
    app.vector_db_client.connect()

@app.on_event("shutdown")  
async def shutdown_span():
    app.mongodb_conn.close()
    app.vector_db_client.disconnect()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
