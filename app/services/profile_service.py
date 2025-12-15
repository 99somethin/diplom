from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRole
from app.services.candidate_service import candidate_service
from app.services.employer_service import employer_service

from app.schemas.unions import ProfileUnion

from app.core.exceptions import UnknownRole, InvalidRole

from app.repository.auth_repo import AuthRepository


class ProfileService:
    def __init__(self):
        self._map = {
            UserRole.candidate: candidate_service,
            UserRole.employer: employer_service,
        }

    def get_service(self, user, profile_role):
        role = user.role
        service = self._map.get(role)
        if not service:
            raise UnknownRole
        if role != profile_role:
            raise InvalidRole
        return service

    async def get_profile(self, user, db: AsyncSession):
        service = self.get_service(user, user.role)
        return await service.get_profile(user, db)

    async def create_profile(self, user, profile_data: ProfileUnion, db: AsyncSession):
        service = self.get_service(user, getattr(profile_data, "role", None))

        profile = await service.create_profile(user, profile_data, db)

        user.profile_completed = True
        await AuthRepository.update(db, user)
  
        return profile

    async def update_profile(self, user, profile_data, db: AsyncSession):
        service = self.get_service(user, profile_data.role)

        user_candidate = await service.update_profile(user, profile_data, db)
        return user_candidate


profile_service = ProfileService()
