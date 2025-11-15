from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_async_db, get_current_employer
from app.models.project import Project as ProjectModel
from app.models.employer import Employer
from app.schemas.project import (
    ProjectMinOut,
    ProjectFullOut,
    ProjectCreateIn,
    ProjectCreateOut,
    ProjectUpdateIn,
    ProjectUpdateOut,
)

from typing import List

router = APIRouter(prefix="/projects", tags=["Open projects"])


@router.get("/", response_model=List[ProjectMinOut])
async def get_projects(db_session: AsyncSession = Depends(get_async_db)):
    stmt = select(ProjectModel)
    db_request = await db_session.scalars(stmt)
    projects = db_request.all()

    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Projects not found"
        )

    return projects


@router.get("/employer_projects", response_model=List[ProjectMinOut])
async def get_projects(
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(ProjectModel).where(ProjectModel.employer_id == employer.id)
    db_request = await db_session.scalars(stmt)
    projects = db_request.all()

    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Projects not found"
        )

    return projects


@router.get("/{project_id}", response_model=ProjectFullOut)
async def get_full_project(
    project_id: int, db_session: AsyncSession = Depends(get_async_db)
):
    stmt = select(ProjectModel).where(ProjectModel.id == project_id)
    db_request = await db_session.scalars(stmt)
    project = db_request.first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Projects not found"
        )

    return project


@router.post("/", response_model=ProjectCreateOut)
async def create_project(
    project: ProjectCreateIn,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    project = ProjectModel(**project.model_dump(), employer_id=employer.id)

    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    return project


@router.patch("/{project_id}", response_model=ProjectUpdateOut)
async def update_project(
    project_id: int,
    update_data: ProjectUpdateIn,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(ProjectModel).where(
        ProjectModel.employer_id == employer.id, ProjectModel.id == project_id
    )
    db_request = await db_session.scalars(stmt)
    project = db_request.first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Projects not found"
        )

    payload = update_data.model_dump(exclude_unset=True, exclude_none=True)

    for forbidden in ("id", "employer_id"):
        payload.pop(forbidden, None)

    for key, value in payload.items():
        if hasattr(project, key):
            setattr(project, key, value)

    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    return project


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    stmt = select(ProjectModel).where(
        ProjectModel.employer_id == employer.id, ProjectModel.id == project_id
    )
    result = await db_session.scalars(stmt)
    project = result.first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    await db_session.execute(delete(ProjectModel).where(ProjectModel.id == project_id))
    await db_session.commit()

    return {"message": "deleted successfully"}
