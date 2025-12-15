from abc import ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepo(ABC):
    model = None

    @classmethod
    async def get_one_or_none(cls, db_session: AsyncSession, **filters):
        stmt = select(cls.model).filter_by(**filters)
        db_request = await db_session.scalars(stmt)
        return db_request.first()

    @classmethod
    async def get_all(cls, db_session: AsyncSession, **filters):
        stmt = select(cls.model).filter_by(**filters)
        db_request = await db_session.scalars(stmt)
        return db_request.all()

    @classmethod
    async def update(cls, db_session: AsyncSession, obj):
        db_session.add(obj)
        await db_session.flush()
        await db_session.refresh(obj)
        return obj

    @classmethod
    async def add(cls, db_session: AsyncSession, **model_data):
        obj = cls.model(**model_data)
        db_session.add(obj)
        await db_session.flush()
        await db_session.refresh(obj)
        return obj
    
    
