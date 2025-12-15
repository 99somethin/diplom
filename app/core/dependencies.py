from fastapi import Depends, Request, Response

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import get_async_db
from app.models.user import UserRole

from app.core.utils import verify_or_refresh_tokens

from app.repository.auth_repo import AuthRepository
from app.repository.employer_repo import EmployerRepository
from app.repository.candidate_repo import CandidateRepository
from app.core.exceptions import (
    InvalidToken,
    UserIsNotExist,
    InvalidTokenMissingSub,
    UserRoleNotAdmin,
    EmployerIsNotFound,
    UserRoleNotEmployer,
    CandidateIsNotExist,
    UserRoleNotCandidate,
)


async def get_current_user(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
):
    payload = verify_or_refresh_tokens(request, response)
    sub = payload.get("sub")
    if sub is None:
        raise InvalidTokenMissingSub

    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise InvalidToken

    user = await AuthRepository.get_one_or_none(db_session, is_active=True, id=user_id)
    if user is None:
        raise UserIsNotExist
    return user


async def get_current_admin(user=Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise UserRoleNotAdmin
    return user


async def get_current_employer(
    user=Depends(get_current_user),
    db_session: AsyncSession = Depends(get_async_db),
):
    if user.role != UserRole.employer:
        raise UserRoleNotEmployer

    employer = await EmployerRepository.get_one_or_none(db_session, user_id=user.id)
    if employer is None:
        raise EmployerIsNotFound
    return employer


async def get_current_candidate(
    user=Depends(get_current_user),
    db_session: AsyncSession = Depends(get_async_db),
):
    if user.role != UserRole.candidate:
        raise UserRoleNotCandidate
    candidate = await CandidateRepository.get_one_or_none(db_session, user_id=user.id)
    if candidate is None:
        raise CandidateIsNotExist
    return candidate
