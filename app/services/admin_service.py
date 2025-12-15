from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import TypeAdapter

from app.repository.admin_repo import AdminRepository
from app.schemas.user import UserBaseSchema

from app.core.exceptions import UserIsNotExist

class AdminService:

    async def get_active_users(self, db_session: AsyncSession):
        users = await AdminRepository.get_all(db_session, is_active=True)
        adapter = TypeAdapter(list[UserBaseSchema])
        return adapter.validate_python(users)
    

    async def get_profile(self, db_session: AsyncSession, user_id: int):
        user  = await AdminRepository.get_one_or_none(db_session, is_active=True, id=user_id)
        if user is None:
            raise UserIsNotExist
        return UserBaseSchema.model_validate(user)
    
    async def delete_user(self, db_session: AsyncSession, user_id: int):
        await AdminRepository.delete(db_session, user_id)
        return None
        


admin_service = AdminService()
