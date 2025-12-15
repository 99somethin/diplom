from app.models.employer import Employer

from app.repository.abstract_repo import AbstractRepo

class EmployerRepository(AbstractRepo):
    model = Employer