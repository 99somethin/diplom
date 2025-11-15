from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    get_async_db,
    get_current_candidate,
    get_current_employer,
)
from app.models.answer import Answer as AnswerModel
from app.models.candidate import Candidate
from app.models.employer import Employer
from app.models.project import Project
from app.schemas.answer import (
    AnswerOut,
    AnswerCreateIn,
    AnswerCreateOut,
    AnswerUpdateIn,
    AnswerUpdateOut,
    Feedback,
)

from typing import List

router = APIRouter(prefix="/answers", tags=["Answer's endpoints"])


@router.get("/candidate", response_model=List[AnswerOut])
async def get_candidate_answers(
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(AnswerModel).where(AnswerModel.candidate_id == candidate.id)
    db_request = await db_session.scalars(stmt)
    answers = db_request.all()

    return answers


@router.get("/project/{project_id}", response_model=List[AnswerOut])
async def get_project_answers(
    project_id: int,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = (
        select(AnswerModel)
        .join(Project, AnswerModel.project_id == Project.id)
        .where(Project.id == project_id, Project.employer_id == employer.id)
    )
    db_request = await db_session.scalars(stmt)
    answers = db_request.all()

    return answers


@router.get("/project/{project_id}/candidate", response_model=AnswerOut)
async def get_candidate_project_answer(
    project_id: int,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(AnswerModel).where(
        AnswerModel.candidate_id == candidate.id, AnswerModel.project_id == project_id
    )
    db_request = await db_session.scalars(stmt)
    answer = db_request.first()

    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )

    return answer


@router.post("/{project_id}", response_model=AnswerCreateOut)
async def create_answer(
    project_id: int,
    answer_data: AnswerCreateIn,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(Project).where(Project.id == project_id)
    db_request = await db_session.scalars(stmt)
    project = db_request.first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    existing_answer = await db_session.scalar(
        select(AnswerModel).where(
            AnswerModel.candidate_id == candidate.id,
            AnswerModel.project_id == project_id,
        )
    )

    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Вы уже отправили ответ на этот проект."
        )

    answer = AnswerModel(
        **answer_data.model_dump(), project_id=project_id, candidate_id=candidate.id
    )

    db_session.add(answer)
    await db_session.commit()
    return answer


@router.patch("/feedback/{answer_id}", response_model=AnswerOut)
async def add_review_feedback(
    answer_id: int,
    feedback_data: Feedback,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(AnswerModel).options(selectinload(AnswerModel.project)).where(AnswerModel.id == answer_id)
    res = await db_session.scalars(stmt)
    answer = res.first()
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")

    if not answer.project or answer.project.employer_id != employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to review this answer")
    
    answer.review_feedback = feedback_data.review_feedback
    await db_session.commit()

    return answer


@router.patch("/{answer_id}", response_model=AnswerUpdateOut)
async def update_answer(
    answer_id: int,
    update_data: AnswerUpdateIn,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(AnswerModel).where(
        AnswerModel.candidate_id == candidate.id, AnswerModel.id == answer_id
    )
    db_request = await db_session.scalars(stmt)
    answer = db_request.first()

    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )

    payload = update_data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in payload.items():
        if hasattr(answer, key):
            setattr(answer, key, value)

    await db_session.commit()
    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_200_OK)
async def delete_answer(
    answer_id: int,
    candidate: Candidate = Depends(get_current_candidate),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(AnswerModel).where(
        AnswerModel.candidate_id == candidate.id, AnswerModel.id == answer_id
    )
    result = await db_session.scalars(stmt)
    answer = result.first()

    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )

    await db_session.execute(delete(AnswerModel).where(AnswerModel.id == answer_id))
    await db_session.commit()

    return {"message": "deleted successfully"}
