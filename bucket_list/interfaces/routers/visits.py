from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from bucket_list.application.commands.delete_visit import DeleteVisit
from bucket_list.application.commands.log_visit import LogVisit, LogVisitInput
from bucket_list.application.queries.get_visit import GetVisit
from bucket_list.application.queries.list_visits import ListVisits
from bucket_list.interfaces.dependencies import (
    get_delete_visit,
    get_list_visits,
    get_log_visit,
    get_visit_query,
)
from bucket_list.interfaces.mappers import visit_to_response
from bucket_list.interfaces.schemas import VisitCreateRequest, VisitResponse
from core.exceptions import NotFoundError

router = APIRouter(tags=["bucket-list"])


@router.get("/users/{user_id}/visits", response_model=list[VisitResponse])
async def list_visits(
    user_id: UUID,
    use_case: ListVisits = Depends(get_list_visits),
) -> list[VisitResponse]:
    results = await use_case.execute(user_id)
    return [visit_to_response(r) for r in results]


@router.post(
    "/users/{user_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
async def log_visit(
    user_id: UUID,
    body: VisitCreateRequest,
    use_case: LogVisit = Depends(get_log_visit),
) -> VisitResponse:
    try:
        result = await use_case.execute(
            LogVisitInput(
                user_id=user_id,
                destination_id=body.destination_id,
                visited_at=body.visited_at,
                notes=body.notes,
            )
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return visit_to_response(result)


@router.get("/users/{user_id}/visits/{visit_id}", response_model=VisitResponse)
async def get_visit(
    user_id: UUID,
    visit_id: UUID,
    use_case: GetVisit = Depends(get_visit_query),
) -> VisitResponse:
    try:
        result = await use_case.execute(visit_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return visit_to_response(result)


@router.delete("/users/{user_id}/visits/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visit(
    user_id: UUID,
    visit_id: UUID,
    use_case: DeleteVisit = Depends(get_delete_visit),
) -> None:
    try:
        await use_case.execute(visit_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
