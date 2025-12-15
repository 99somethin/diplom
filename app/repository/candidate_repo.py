from app.models.candidate import Candidate
from app.repository.abstract_repo import AbstractRepo

class CandidateRepository(AbstractRepo):
    model =  Candidate