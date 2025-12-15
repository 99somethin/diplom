from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.candidate import CandidateCreateSchema, CandidateBase
from app.schemas.unions import UserCandidateSchema, UserCandidateUpdateSchema

from app.repository.candidate_repo import CandidateRepository
from app.core.exceptions import (
    CandidateIsNotExist,
    CandidateIsAlreadyExist,
    EmailIsBusyException,
)
from app.repository.auth_repo import AuthRepository


class CandidateService:
    async def get_profile(self, user, db: AsyncSession):
        candidate = await CandidateRepository.get_one_or_none(db, user_id=user.id)
        if candidate is None:
            raise CandidateIsNotExist

        return UserCandidateSchema.model_validate(
            {"user": user, "candidate": candidate}
        )

    async def create_profile(
        self, user, profile_data: CandidateCreateSchema, db: AsyncSession
    ):
        existing = await CandidateRepository.get_one_or_none(db, user_id=user.id)
        if existing:
            raise CandidateIsAlreadyExist

        candidate = await CandidateRepository.add(
            db,
            bio=profile_data.bio,
            resume_link=profile_data.resume_link,
            user_id=user.id,
        )
        return CandidateBase.model_validate(candidate)

    async def update_profile(
        self, user, update_data: UserCandidateUpdateSchema, db: AsyncSession
    ):
        user_update = update_data.user.model_dump(exclude_unset=True)

        received_email = user_update.get("email", False)
        if received_email:
            email_exist = await AuthRepository.get_one_or_none(db, email=received_email)
            if email_exist:
                raise EmailIsBusyException
            user.email = received_email
        if user_update.get("full_name", False):
            user.full_name = user_update.get("full_name")
        await AuthRepository.update(db, user)

        candidate = await CandidateRepository.get_one_or_none(user_id=user.id)
        candidate_update = update_data.candidate.model_dump(exclude_unset=True)

        for field, value in candidate_update.items():
            setattr(candidate, field, value)
        await CandidateRepository.update(db, candidate)

        return UserCandidateUpdateSchema.model_validate(
            {"user": user, "candidate": candidate}
        )


candidate_service = CandidateService()
