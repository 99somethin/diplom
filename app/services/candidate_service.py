from fastapi import HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.candidate import CandidateCreateSchema, CandidateBase
from app.schemas.unions import UserCandidateSchema, UserCandidateUpdateSchema
from app.models.candidate import Candidate
from app.models.user import UserRole, User as UserModel


class Candidate_Service:
    async def get_profile(self, user, db: AsyncSession):
        stmt = select(Candidate).where(Candidate.user_id == user.id)
        res = await db.scalars(stmt)
        candidate = res.first()
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate profile not found",
            )

        return UserCandidateSchema.model_validate(
            {"user": user, "candidate": candidate}
        )

    async def create_profile(
        self, user, profile_data: CandidateCreateSchema, db: AsyncSession
    ):
        stmt = select(Candidate).where(Candidate.user_id == user.id)
        res = await db.scalars(stmt)
        existing = res.first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )

        candidate = Candidate(
            bio=profile_data.bio,
            resume_link=profile_data.resume_link,
            user_id=user.id,
        )

        db.add(candidate)
        await db.flush()
        await db.refresh(candidate)

        return CandidateBase.model_validate(candidate)

    async def update_profile(
        self, user, update_data: UserCandidateUpdateSchema, db: AsyncSession
    ):
        user_update = update_data.user.model_dump(exclude_unset=True)

        email = user_update.get("email", False)
        if email:
            stmt = select(UserModel).where(UserModel.email == email)
            res = await db.scalars(stmt)
            email_exist = res.first()

            if email_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )
            user.email = email
        if user_update.get("full_name", False):
            user.full_name = user_update.get("full_name")

        db.add(user)
        await db.flush()

        candidate_update = update_data.candidate.model_dump(exclude_unset=True)

        if candidate_update:
            stmt = (
                update(Candidate)
                .where(Candidate.user_id == user.id)
                .values(**candidate_update)
            )
            await db.execute(stmt)

        stmt = select(Candidate).where(Candidate.user_id == user.id)
        res = await db.scalars(stmt)
        candidate = res.first()

        return UserCandidateUpdateSchema.model_validate({"user": user, "candidate": candidate})


candidate_service = Candidate_Service()

