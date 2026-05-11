from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    import app.models  # noqa: garante que os modelos são registrados no Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
