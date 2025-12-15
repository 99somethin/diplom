from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.schemas.auth import (
    RegisterInSchema,
    RegisterOutSchema,
    LoginInSchema,
    LoginOutSchema,
)
from app.services.auth_service import auth_service


router = APIRouter(prefix="/auth", tags=["Authentification and authorization"])


@router.post(
    "/register", response_model=RegisterOutSchema, status_code=status.HTTP_201_CREATED
)
async def registrate_user(
    user_data: RegisterInSchema, db_session: AsyncSession = Depends(get_async_db)
):
    user = await auth_service.registrate_service(user_data, db_session)
    return user


@router.post("/login", response_model=LoginOutSchema)
async def login(
    login_data: LoginInSchema,
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
):
    user = await auth_service.login_service(login_data, response, db_session)
    return user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
):
    await auth_service.logout_service(response)
    return {"detail": "Logged out successfully"}
