from app.db.database import async_session_maker


async def get_async_db():
    async with async_session_maker() as session:
        async with session.begin():
            try:
                yield session
            finally:
                pass
