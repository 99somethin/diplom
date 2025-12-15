from app.models.user import User

from app.repository.abstract_repo import AbstractRepo

class AuthRepository(AbstractRepo):
    model = User