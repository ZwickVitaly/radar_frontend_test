from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_async_engine(db_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
