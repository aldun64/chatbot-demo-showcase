from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv 
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an asynchronous session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get a database session
async def get_db():
    async with async_session() as session:
        yield session
