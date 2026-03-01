import asyncio
import sys
from pathlib import Path

# Add project root to python path to avoid module errors
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine, Base
from app.models import user, chat # Import models to ensure they are registered with Base

async def init_db():
    async with engine.begin() as conn:
        print("Creating all tables in the database...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
