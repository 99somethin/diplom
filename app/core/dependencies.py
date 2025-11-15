from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.models.user import User as UserModel, UserRole
from app.models.employer import Employer
from app.models.candidate import Candidate

from app.services.auth_service import verify_or_refresh_tokens


async def get_current_user(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
):
    payload = verify_or_refresh_tokens(request, response)
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid token: missing sub")

    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token subject")

    stmt = select(UserModel).where(UserModel.is_active == True, UserModel.id == user_id)
    db_request = await db_session.scalars(stmt)
    user = db_request.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )

    return user


async def get_current_admin(user=Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User role is not admin"
        )
    return user


async def get_current_employer(user=Depends(get_current_user), db_session: AsyncSession = Depends(get_async_db),):
    if user.role != UserRole.employer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User role is not employer"
        )
    stmt = select(Employer).where(Employer.user_id == user.id)
    db_request = await db_session.scalars(stmt)
    employer = db_request.first()

    if employer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )
    return employer


async def get_current_candidate(user=Depends(get_current_user), db_session: AsyncSession = Depends(get_async_db),):
    if user.role != UserRole.candidate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User role is not candidate"
        )
    stmt = select(Candidate).where(Candidate.user_id == user.id)
    db_request = await db_session.scalars(stmt)
    candidate = db_request.first()

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )
    return candidate