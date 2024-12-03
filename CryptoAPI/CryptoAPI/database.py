from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from good_guard import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
Base = declarative_base()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session