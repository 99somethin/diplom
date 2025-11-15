from fastapi import HTTPException, Request, Response, status

from datetime import datetime, timezone, timedelta
from pathlib import Path
import bcrypt

import traceback

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.core.config import settings
from app.schemas.jwt import JWTCreateSchema

PRIVATE_KEY = Path(settings.PRIVATE_KEY_PATH).read_text()
PUBLIC_KEY = Path(settings.PUBLIC_KEY_PATH).read_text()


def create_hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return password.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
    payload: JWTCreateSchema, private_key=PRIVATE_KEY, algorithm=settings.ALGORITHM
):
    to_encode = payload.model_dump()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, private_key, algorithm)


def create_refresh_token(
    payload: JWTCreateSchema, private_key=PRIVATE_KEY, algorithm=settings.ALGORITHM
):
    to_encode = payload.model_dump()

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, private_key, algorithm)


def decode_tokens(token: str, public_key=PUBLIC_KEY, algorithm=settings.ALGORITHM):
    try:
        payload = jwt.decode(jwt=token,key=public_key, algorithms=[algorithm])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def verify_or_refresh_tokens(request: Request, response: Response) -> dict:
    access_token = request.cookies.get("access_token")

    payload = None
    if access_token:
        try:
            payload = decode_tokens(access_token)
        except HTTPException:
            payload = None

    if not payload:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        try:
            decode_refresh = decode_tokens(refresh_token)
        except HTTPException:
            raise HTTPException(
                status_code=401, detail="Refresh token invalid or expired"
            )

        new_access_token = create_access_token(JWTCreateSchema(**decode_refresh))
        new_refresh_token = create_refresh_token(JWTCreateSchema(**decode_refresh))

        response.set_cookie(key="access_token", value=new_access_token)
        response.set_cookie(key="refresh_token", value=new_refresh_token)

        payload = decode_refresh

    return payload
