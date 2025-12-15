from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.repository.abstract_repo import AbstractRepo

class AdminRepository(AbstractRepo):
    model = User

    @classmethod
    async def delete(cls, db_session: AsyncSession, user_id: int):
        await db_session.execute(delete(cls.model).where(cls.model.id == user_id))
        return None
        