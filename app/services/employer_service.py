from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.employer import EmployerBase, EmployerCreateSchema
from app.schemas.unions import UserEmployerSchema, UserEmployerUpdateSchema

from app.repository.employer_repo import EmployerRepository
from app.repository.auth_repo import AuthRepository
from app.core.exceptions import (
    EmployerIsNotFound,
    EmployereIsAlreadyExist,
    EmailIsBusyException,
)


class EmployerService:
    async def get_profile(self, user, db: AsyncSession):
        employer = await EmployerRepository.get_one_or_none(db, user_id=user.id)
        if employer is None:
            raise EmployerIsNotFound

        return UserEmployerSchema.model_validate({"user": user, "employer": employer})

    async def create_profile(
        self, user, profile_data: EmployerCreateSchema, db: AsyncSession
    ):
        result = await EmployerRepository.get_one_or_none(db, user_id=user.id)
        if result is not None:
            raise EmployereIsAlreadyExist

        employer = await EmployerRepository.add(
            db,
            company_name=profile_data.company_name,
            company_description=profile_data.company_description,
            industry=profile_data.industry,
            location=profile_data.location,
            user_id=user.id,
        )
        return EmployerBase.model_validate(employer)

    async def update_profile(
        self, user, update_data: UserEmployerUpdateSchema, db: AsyncSession
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

        employer_update = update_data.employer.model_dump(exclude_unset=True)
        employer = await EmployerRepository.get_one_or_none(db, user_id=user.id)

        for field, value in employer_update.values():
            setattr(employer, field, value)

        await EmployerRepository.update(db, employer)

        return UserEmployerUpdateSchema.model_validate(
            {"user": user, "employer": employer}
        )


employer_service = EmployerService()
