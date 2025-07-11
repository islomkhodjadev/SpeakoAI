import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from backend.core.config import settings

print("🧠 [models.py] Loading database setup...")

# Create engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)
print(f"⚙️ [models.py] Engine created: {engine}")

# Create async session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)
print(f"📦 [models.py] async_session factory created: {async_session} (type: {type(async_session)})")

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def init_db():
    print("🚀 [models.py] Running init_db...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ [models.py] Database schema created")

if __name__ == "__main__":
    asyncio.run(init_db())
