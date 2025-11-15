from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.schemas.unions import (
    ProfileUnion,
    UserProfileSchema,
    UserProfileUpdateSchema,
)
from app.core.dependencies import get_current_user
from app.services.profile_service import profile_service


router = APIRouter(prefix="/profile", tags=["User's profile endpoints"])


@router.get("/", response_model=UserProfileSchema)
async def get_profile(
    current_user=Depends(get_current_user),
    db_session: AsyncSession = Depends(get_async_db),
):
    result = await profile_service.get_profile(current_user, db_session)
    return result


@router.post("/", response_model=ProfileUnion)
async def create_profile(
    profile_data: ProfileUnion,
    current_user=Depends(get_current_user),
    db_session: AsyncSession = Depends(get_async_db),
):
    result = await profile_service.create_profile(
        current_user, profile_data, db_session
    )
    return result


@router.patch("/", response_model=UserProfileUpdateSchema)
async def change_profile(
    profile_data: UserProfileUpdateSchema,
    current_user=Depends(get_current_user),
    db_session: AsyncSession = Depends(get_async_db),
):
    result = await profile_service.update_profile(
        current_user, profile_data, db_session
    )
    return result
