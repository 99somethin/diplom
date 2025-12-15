from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import TypeAdapter

from app.repository.answear_repo import AnswearRepository
from app.repository.project_repo import ProjectRepository

from app.core.exceptions import (
    AnswerIsNotFound,
    ProjectIsNotFound,
    AnswerIsAlreadyExist,
    NotAllowedToAddReview,
)
from app.schemas.answer import (
    AnswerOut,
    AnswerCreateIn,
    AnswerCreateOut,
    AnswerUpdateIn,
    AnswerUpdateOut,
    Feedback,
)


class AnswearService:

    async def get_candidate_answers(self, db_session: AsyncSession, cand_id: int):
        answers = await AnswearRepository.get_all(db_session, candidate_id=cand_id)
        adapter = TypeAdapter(list[AnswerOut])
        return adapter.validate_python(answers)

    async def get_project_answers(
        self, db_session: AsyncSession, project_id: int, employer_id: int
    ):
        answers = await AnswearRepository.get_project_answers(
            db_session, project_id, employer_id
        )
        adapter = TypeAdapter(list[AnswerOut])
        return adapter.validate_python(answers)

    async def get_candidate_project_answer(
        self, db_session: AsyncSession, proj_id: int, cand_id: int
    ):
        answer = await AnswearRepository.get_one_or_none(
            db_session, candidate_id=cand_id, project_id=proj_id
        )
        if answer is None:
            raise AnswerIsNotFound
        return AnswerOut.model_validate(answer)

    async def create_answer(
        self,
        db_session: AsyncSession,
        proj_id: int,
        answer_data: AnswerCreateIn,
        cand_id: int,
    ):
        project = await ProjectRepository.get_one_or_none(db_session, id=proj_id)
        if project is None:
            raise ProjectIsNotFound

        existing_answer = await AnswearRepository.get_one_or_none(
            db_session, candidate_id=cand_id, project_id=proj_id
        )
        if existing_answer is not None:
            raise AnswerIsAlreadyExist

        answer = await AnswearRepository.add(
            db_session,
            **answer_data.model_dump(),
            project_id=proj_id,
            candidate_id=cand_id
        )
        return AnswerCreateOut.model_validate(answer)

    async def add_review(
        self,
        db_session: AsyncSession,
        answer_id: int,
        feedback_data: Feedback,
        employer_id: int,
    ):
        answer = await AnswearRepository.get_answer_with_project(db_session, answer_id)
        if answer is None:
            raise AnswerIsNotFound

        if not answer.project or answer.project.employer_id != employer_id:
            raise NotAllowedToAddReview

        answer.review_feedback = feedback_data.review_feedback
        await AnswearRepository.update(db_session, answer)
        return AnswerOut.model_validate(answer)

    async def update_answer(
        self,
        db_session: AsyncSession,
        answer_id: int,
        update_data: AnswerUpdateIn,
        cand_id: int,
    ):
        answer = await AnswearRepository.get_one_or_none(
            db_session, candidate_id=cand_id, id=answer_id
        )
        if answer is None:
            raise AnswerIsNotFound

        payload = update_data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in payload.items():
            if hasattr(answer, key):
                setattr(answer, key, value)

        await AnswearRepository.update(db_session, answer)
        return AnswerOut.model_validate(answer)

    async def delete_answer(
        self, db_session: AsyncSession, answer_id: int, cand_id: int
    ):
        answer = await AnswearRepository.get_one_or_none(db_session, candidate_id=cand_id, id=answer_id)
        if answer is None:
            raise AnswerIsNotFound
        AnswearRepository.delete(db_session, candidate_id=cand_id, id=answer_id)       
        return None

answear_service = AnswearService()
