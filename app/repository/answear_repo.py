from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.repository.abstract_repo import AbstractRepo
from app.models.answer import Answer
from app.models.project import Project

from sqlalchemy.orm import selectinload


class AnswearRepository(AbstractRepo):
    model = Answer

    @classmethod
    async def get_project_answers(
        cls, db_session: AsyncSession, proj_id: int, emp_id: int
    ):
        stmt = (
            select(cls.model)
            .join(Project, cls.model.project_id == Project.id)
            .where(Project.id == proj_id, Project.employer_id == emp_id)
        )
        db_request = await db_session.scalars(stmt)
        answers = db_request.all()
        return answers
    
    @classmethod
    async def get_answer_with_project(cls, db_session: AsyncSession, answer_id: int):
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.project))
            .where(cls.model.id == answer_id)
        )
        res = await db_session.scalars(stmt)
        answer = res.first()
        return answer
    
    @classmethod
    async def delete(cls, db_session: AsyncSession, **filters):
        await db_session.execute(delete(cls.model).filter_by(**filters))
        return None

