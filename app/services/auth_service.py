from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.auth_repo import AuthRepository

from app.core.exceptions import EmailIsBusyException, EmailWithNoUser, IncorrectPassword
from app.schemas.jwt import JWTCreateSchema
from app.core.utils import (
    create_hash_password,
    check_password,
    create_access_token,
    create_refresh_token,
)
from app.schemas.auth import (
    RegisterInSchema,
    LoginInSchema,
    RegisterOutSchema,
    LoginOutSchema,
)


class AuthService:

    async def registrate_service(
        self, user_data: RegisterInSchema, db_session: AsyncSession
    ):
        existed_user = await AuthRepository.get_one_or_none(
            db_session, is_active=True, email=user_data.email
        )

        if existed_user is not None:
            raise EmailIsBusyException

        hashed_pass = create_hash_password(user_data.password)
        model_data = user_data.model_dump(exclude="password")
        model_data.update({"hashed_password": hashed_pass})

        user = await AuthRepository.add(db_session, **model_data)

        return RegisterOutSchema.model_validate(user)

    async def login_service(
        self, login_data: LoginInSchema, response: Response, db_session: AsyncSession
    ):
        user = await AuthRepository.get_one_or_none(
            db_session, is_active=True, email=login_data.email
        )

        if user is None:
            raise EmailWithNoUser
        if not check_password(login_data.password, user.hashed_password):
            raise IncorrectPassword

        encode_data = JWTCreateSchema(
            sub=str(user.id), name=user.full_name, role=user.role
        )

        access_token = create_access_token(encode_data)
        refresh_token = create_refresh_token(encode_data)

        response.set_cookie(key="access_token", value=access_token)
        response.set_cookie(key="refresh_token", value=refresh_token)

        return LoginOutSchema.model_validate(user)

    async def logout_service(self, response: Response):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "sucessfull exit"}


auth_service = AuthService()
