from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.models.user import User as UserModel
from app.schemas.auth import (
    RegisterInSchema,
    RegisterOutSchema,
    LoginInSchema,
    LoginOutSchema,
)
from app.schemas.jwt import JWTCreateSchema
from app.services.auth_service import (
    create_hash_password,
    check_password,
    create_access_token,
    create_refresh_token,
)

from typing import List

router = APIRouter(prefix="/auth", tags=["Authentification and authorization"])


@router.post("/register", response_model=RegisterOutSchema)
async def registrate_user(
    user_data: RegisterInSchema, db_session: AsyncSession = Depends(get_async_db)
):
    stmt = select(UserModel).where(
        UserModel.is_active == True, UserModel.email == user_data.email
    )
    db_request = await db_session.scalars(stmt)
    existed_user = db_request.first()

    if existed_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is busy"
        )

    hashed_pass = create_hash_password(user_data.password)

    user = UserModel(
        email=user_data.email,
        hashed_password=hashed_pass,
        full_name=user_data.full_name,
        role=user_data.role,
        profile_completed=False,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@router.post("/login", response_model=LoginOutSchema)
async def login(
    login_data: LoginInSchema,
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(UserModel).where(
        UserModel.is_active == True, UserModel.email == login_data.email
    )
    db_request = await db_session.scalars(stmt)
    user = db_request.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not check_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    encode_data = JWTCreateSchema(sub=str(user.id), name=user.full_name, role=user.role)

    access_token = create_access_token(encode_data)
    refresh_token = create_refresh_token(encode_data)

    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)

    return user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "sucessfull exit"}
