from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()


POSTGRES_URL = os.environ.get("POSTGRES_URL")


engine = create_engine("postgresql://postgres:123@postgres:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_engine = create_async_engine(
    "postgresql+asyncpg://postgres:123@postgres:5432/postgres", echo=True, future=True)

async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_db():
    async with async_session() as session:
        yield session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, index=True)
    price = Column(Float)
    fee = Column(Float)
    total = Column(Float)
    quantity = Column(Integer)
    status = Column(String)


Base.metadata.create_all(engine)
