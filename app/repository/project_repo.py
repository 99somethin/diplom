from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.repository.abstract_repo import AbstractRepo

class ProjectRepository(AbstractRepo):
    model = Project

    @classmethod
    async def delete(cls, db_session: AsyncSession, **filters):
        await db_session.execute(delete(cls.model).filter_by(**filters))
        return None