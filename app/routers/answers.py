from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    get_async_db,
    get_current_candidate,
    get_current_employer,
)
from app.models.candidate import Candidate
from app.models.employer import Employer
from app.schemas.answer import (
    AnswerOut,
    AnswerCreateIn,
    AnswerCreateOut,
    AnswerUpdateIn,
    AnswerUpdateOut,
    Feedback,
)

from typing import List

from app.services.answear_service import answear_service

router = APIRouter(prefix="/answers", tags=["Answer's endpoints"])


@router.get("/candidate", response_model=List[AnswerOut])
async def get_candidate_answers(
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    answers = await answear_service.get_candidate_answers(db_session, candidate.id)
    return answers


@router.get("/project/{project_id}", response_model=List[AnswerOut])
async def get_project_answers(
    project_id: int,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    answers = await answear_service.get_project_answers(
        db_session, project_id, employer.id
    )
    return answers


@router.get("/project/{project_id}/candidate", response_model=AnswerOut)
async def get_candidate_project_answer(
    project_id: int,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    answer = answear_service.get_candidate_project_answer(
        db_session, project_id, candidate.id
    )
    return answer


@router.post("/{project_id}", response_model=AnswerCreateOut)
async def create_answer(
    project_id: int,
    answer_data: AnswerCreateIn,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    answer = await answear_service.create_answer(
        db_session, project_id, answer_data, candidate.id
    )
    return answer


@router.patch("/feedback/{answer_id}", response_model=AnswerOut)
async def add_review_feedback(
    answer_id: int,
    feedback_data: Feedback,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    answer = await answear_service.add_review(
        db_session, answer_id, feedback_data, employer.id
    )
    return answer


@router.patch("/{answer_id}", response_model=AnswerUpdateOut)
async def update_answer(
    answer_id: int,
    update_data: AnswerUpdateIn,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    answer = await answear_service.update_answer(
        db_session, answer_id, update_data, candidate.id
    )
    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_200_OK)
async def delete_answer(
    answer_id: int,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    await answear_service.delete_answer(db_session, answer_id, candidate.id)
    return {"message": "deleted successfully"}
