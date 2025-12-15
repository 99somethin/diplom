from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_async_db, get_current_employer
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

from app.services.project_service import project_service

router = APIRouter(prefix="/projects", tags=["Open projects"])


@router.get("/", response_model=List[ProjectMinOut])
async def get_projects(db_session: AsyncSession = Depends(get_async_db)):
    projects = await project_service.get_projects(db_session)
    return projects


@router.get("/employer_projects", response_model=List[ProjectMinOut])
async def get_employer_projects(
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    projects = await project_service.get_employer_projects(db_session, employer.id)
    return projects


@router.get("/{project_id}", response_model=ProjectFullOut)
async def get_full_project(
    project_id: int, db_session: AsyncSession = Depends(get_async_db)
):
    project = await project_service.get_full_project(db_session, project_id)
    return project


@router.post("/", response_model=ProjectCreateOut)
async def create_project(
    project: ProjectCreateIn,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    project = await project_service.create_project(db_session, project, employer.id)
    return project


@router.patch("/{project_id}", response_model=ProjectUpdateOut)
async def update_project(
    project_id: int,
    update_data: ProjectUpdateIn,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    project = await project_service.update_project(
        db_session, project_id, update_data, employer.id
    )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int,
    employer: Employer = Depends(get_current_employer),
    db_session: AsyncSession = Depends(get_async_db),
):
    await project_service.delete_project(db_session, project_id, employer.id)
    return {"message": "deleted successfully"}
