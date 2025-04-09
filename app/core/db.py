from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), future=True, echo=True
)


async def init_db() -> None:
    async with AsyncSession(engine) as session:
        rs = await session.execute(text("SELECT * FROM station"))
        for station in rs:
            path = f"ws://{settings.API_URL}/{station[1]}"
            await session.execute(
                text(f"UPDATE station SET url = '{path}' WHERE id = {station[0]}")
            )

        truncate_lap = text("TRUNCATE lap")
        await session.execute(truncate_lap)
        truncate_detection = text("TRUNCATE detection")
        await session.execute(truncate_detection)

        await session.commit()


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.commit()
