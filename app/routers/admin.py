from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.core.dependencies import get_current_admin
from app.models.user import User as UserModel
from app.schemas.user import UserBaseSchema

from typing import List

router = APIRouter(prefix="/admin", tags=["Admin's endpoints"])


@router.get("/", response_model=List[UserBaseSchema])
async def get_users(
    user: UserModel = Depends(get_current_admin),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(UserModel).where(UserModel.is_active == True)
    db_request = await db_session.scalars(stmt)
    users = db_request.all()
    return users


@router.get("/users/{user_id}")
async def get_user_profile(
    user_id: int,
    user: UserModel = Depends(get_current_admin),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(UserModel).where(UserModel.is_active == True, UserModel.id == user_id)
    db_request = await db_session.scalars(stmt)
    user = db_request.first()
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    user: UserModel = Depends(get_current_admin),
    db_session: AsyncSession = Depends(get_async_db),
):
    await db_session.execute(delete(UserModel).where(UserModel.id == user_id))
    db_session.commit()

    return {"message": "user deleted"}
