from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.core.dependencies import get_current_admin
from app.models.user import User as UserModel
from app.schemas.user import UserBaseSchema

from typing import List

from app.services.admin_service import admin_service

router = APIRouter(prefix="/admin", tags=["Admin's endpoints"])


@router.get("/users", response_model=List[UserBaseSchema])
async def get_users(
    admin_user: UserModel = Depends(get_current_admin),
    db_session: AsyncSession = Depends(get_async_db),
):
    users = await admin_service.get_active_users(db_session)
    return users


@router.get("/users/{user_id}", response_model=UserBaseSchema)
async def get_user_profile(
    user_id: int,
    admin_user: UserModel = Depends(get_current_admin),
    db_session: AsyncSession = Depends(get_async_db),
):
    user = await admin_service.get_profile(db_session, user_id)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    admin_user: UserModel = Depends(get_current_admin),
    db_session: AsyncSession = Depends(get_async_db),
):
    await admin_service.delete_user(db_session, user_id)
    return {"message": "user deleted"}
