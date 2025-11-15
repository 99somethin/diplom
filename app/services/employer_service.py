from fastapi import HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employer import Employer
from app.models.user import User as UserModel
from app.schemas.employer import EmployerBase, EmployerCreateSchema
from app.schemas.unions import UserEmployerSchema, UserEmployerUpdateSchema


class Employer_Service:
    async def get_profile(self, user, db: AsyncSession):
        stmt = select(Employer).where(Employer.user_id == user.id)
        res = await db.scalars(stmt)
        employer = res.first()
        if not employer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employer profile not found",
            )

        return UserEmployerSchema.model_validate({"user": user, "employer": employer})

    async def create_profile(
        self, user, profile_data: EmployerCreateSchema, db: AsyncSession
    ):
        stmt = select(Employer).where(Employer.user_id == user.id)
        db_request = await db.scalars(stmt)
        result = db_request.first()

        if result is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        employer = Employer(
            company_name=profile_data.company_name,
            company_description=profile_data.company_description,
            industry=profile_data.industry, 
            location=profile_data.location,
            user_id=user.id,
        )

        db.add(employer)
        await db.flush()
        await db.refresh(employer)

        return EmployerBase.model_validate(employer)

    async def update_profile(
        self, user, update_data: UserEmployerUpdateSchema, db: AsyncSession
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

        employer_update = update_data.employer.model_dump(exclude_unset=True)

        if employer_update:
            stmt = (
                update(Employer)
                .where(Employer.user_id == user.id)
                .values(**employer_update)
            )
            await db.execute(stmt)

        stmt = select(Employer).where(Employer.user_id == user.id)
        res = await db.scalars(stmt)
        employer = res.first()

        return UserEmployerUpdateSchema.model_validate({"user": user, "employer": employer})


employer_service = Employer_Service()
