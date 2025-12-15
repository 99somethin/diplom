from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import TypeAdapter

from app.repository.project_repo import ProjectRepository
from app.core.exceptions import ProjectIsNotFound

from app.schemas.project import (
    ProjectMinOut,
    ProjectFullOut,
    ProjectCreateIn,
    ProjectCreateOut,
    ProjectUpdateIn,
    ProjectUpdateOut,
)


class ProjectService:

    async def get_projects(self, db_session: AsyncSession):
        projects = await ProjectRepository.get_all(db_session)
        if not projects:
            raise ProjectIsNotFound

        adapter = TypeAdapter(list[ProjectMinOut])
        return adapter.validate_python(projects)

    async def get_employer_projects(self, db_session: AsyncSession, empl_id: int):
        projects = await ProjectRepository.get_all(db_session, employer_id=empl_id)
        if not projects:
            raise ProjectIsNotFound

        adapter = TypeAdapter(list[ProjectMinOut])
        return adapter.validate_python(projects)

    async def get_full_project(self, db_session: AsyncSession, project_id: int):
        project = await ProjectRepository.get_one_or_none(db_session, id == project_id)
        if not project:
            raise ProjectIsNotFound

        return ProjectFullOut.model_validate(project)

    async def create_project(
        self, db_session: AsyncSession, project: ProjectCreateIn, empl_id: int
    ):
        project_model = await ProjectRepository.add(
            db_session, **project.model_dump(), employer_id=empl_id
        )
        return ProjectCreateOut.model_validate(project_model)

    async def update_project(
        self,
        db_session: AsyncSession,
        project_id: int,
        update_data: ProjectUpdateIn,
        empl_id: int,
    ):
        project = await ProjectRepository.get_one_or_none(
            db_session, employer_id=empl_id, id=project_id
        )
        if project is None:
            raise ProjectIsNotFound

        payload = update_data.model_dump(exclude_unset=True, exclude_none=True)
        for forbidden in ("id", "employer_id"):
            payload.pop(forbidden, None)

        for key, value in payload.items():
            if hasattr(project, key):
                setattr(project, key, value)

        await ProjectRepository.update(db_session, project)
        return ProjectUpdateOut.model_validate(project)

    async def delete_project(
        self, db_session: AsyncSession, project_id: int, empl_id: int
    ):
        project = await ProjectRepository.get_one_or_none(
            db_session, employer_id=empl_id, id=project_id
        )
        if project is None:
            raise ProjectIsNotFound

        await ProjectRepository.delete(db_session, id=project_id)
        return None


project_service = ProjectService()
