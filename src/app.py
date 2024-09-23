import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.db_init import init_db
from src.routes import router
from application.logger import setup_logging

@asynccontextmanager
async def app_life(_: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=app_life) 
app.include_router(router)

if __name__ == "__main__":
    setup_logging()
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
