from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from resume.application.commands.add_project import AddProject, AddProjectInput
from resume.application.commands.delete_project import DeleteProject
from resume.application.commands.reorder_projects import ReorderProjects
from resume.application.commands.update_project import UpdateProject, UpdateProjectInput
from resume.application.dtos import ReorderItem
from resume.application.queries.get_project import GetProject
from resume.application.queries.list_projects import ListProjects
from core.exceptions import NotFoundError
from resume.interfaces.dependencies import (
    get_add_project,
    get_delete_project,
    get_list_projects,
    get_project,
    get_reorder_projects,
    get_update_project,
)
from resume.interfaces.mappers import project_to_response
from resume.interfaces.schemas import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
    ReorderRequest,
)

router = APIRouter(prefix="/resumes/{resume_id}/projects", tags=["projects"])


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    resume_id: UUID,
    use_case: ListProjects = Depends(get_list_projects),
) -> list[ProjectResponse]:
    results = await use_case.execute(resume_id)
    return [project_to_response(r) for r in results]


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def add_project(
    resume_id: UUID,
    body: ProjectCreateRequest,
    use_case: AddProject = Depends(get_add_project),
) -> ProjectResponse:
    result = await use_case.execute(
        AddProjectInput(
            resume_id=resume_id,
            name=body.name,
            description=body.description,
            github_url=body.github_url,
            live_url=body.live_url,
            sort_order=body.sort_order,
            technology_ids=[(tid, i) for i, tid in enumerate(body.technology_ids)],
        )
    )
    return project_to_response(result)


@router.post("/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_projects(
    resume_id: UUID,
    body: ReorderRequest,
    use_case: ReorderProjects = Depends(get_reorder_projects),
) -> None:
    await use_case.execute([ReorderItem(id=item.id, sort_order=item.sort_order) for item in body.items])


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_route(
    resume_id: UUID,
    project_id: UUID,
    use_case: GetProject = Depends(get_project),
) -> ProjectResponse:
    try:
        result = await use_case.execute(project_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return project_to_response(result)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    resume_id: UUID,
    project_id: UUID,
    body: ProjectUpdateRequest,
    use_case: UpdateProject = Depends(get_update_project),
) -> ProjectResponse:
    try:
        result = await use_case.execute(
            UpdateProjectInput(
                project_id=project_id,
                name=body.name,
                description=body.description,
                github_url=body.github_url,
                live_url=body.live_url,
                sort_order=body.sort_order,
                technology_ids=[(tid, i) for i, tid in enumerate(body.technology_ids)],
            )
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return project_to_response(result)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    resume_id: UUID,
    project_id: UUID,
    use_case: DeleteProject = Depends(get_delete_project),
) -> None:
    try:
        await use_case.execute(project_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
