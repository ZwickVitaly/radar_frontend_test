from contextlib import asynccontextmanager

from fastapi import FastAPI
from api import router
from get_cats import get_cats
from generate_products import create_products
from db_models import Product, User
from db import engine, Base
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_products()
    get_cats()
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

origins = ["0.0.0.0:8000", "localhost", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

