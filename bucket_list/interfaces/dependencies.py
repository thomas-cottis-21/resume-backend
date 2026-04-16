from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bucket_list.application.commands.add_to_bucket_list import AddToBucketList
from bucket_list.application.commands.create_destination import CreateDestination
from bucket_list.application.commands.delete_destination import DeleteDestination
from bucket_list.application.commands.delete_visit import DeleteVisit
from bucket_list.application.commands.log_visit import LogVisit
from bucket_list.application.commands.remove_from_bucket_list import RemoveFromBucketList
from bucket_list.application.commands.update_bucket_list_item import UpdateBucketListItem
from bucket_list.application.commands.update_destination import UpdateDestination
from bucket_list.application.queries.get_bucket_list_item import GetBucketListItem
from bucket_list.application.queries.get_destination import GetDestination
from bucket_list.application.queries.get_visit import GetVisit
from bucket_list.application.queries.list_bucket_list_items import ListBucketListItems
from bucket_list.application.queries.list_bucket_list_statuses import ListBucketListStatuses
from bucket_list.application.queries.list_destination_categories import ListDestinationCategories
from bucket_list.application.queries.list_destinations import ListDestinations
from bucket_list.application.queries.list_visits import ListVisits
from bucket_list.infrastructure.repositories.bucket_list_item_repository import (
    SqlAlchemyBucketListItemRepository,
)
from bucket_list.infrastructure.repositories.destination_repository import (
    SqlAlchemyDestinationRepository,
)
from bucket_list.infrastructure.repositories.status_repository import SqlAlchemyStatusRepository
from bucket_list.infrastructure.repositories.visit_repository import SqlAlchemyVisitRepository
from core.database.session import get_db_session

# ── Query factories ────────────────────────────────────────────────────────────


async def get_list_destination_categories(
    session: AsyncSession = Depends(get_db_session),
) -> ListDestinationCategories:
    return ListDestinationCategories(SqlAlchemyStatusRepository(session))


async def get_list_bucket_list_statuses(
    session: AsyncSession = Depends(get_db_session),
) -> ListBucketListStatuses:
    return ListBucketListStatuses(SqlAlchemyStatusRepository(session))


async def get_list_destinations(
    session: AsyncSession = Depends(get_db_session),
) -> ListDestinations:
    return ListDestinations(SqlAlchemyDestinationRepository(session))


async def get_destination_query(
    session: AsyncSession = Depends(get_db_session),
) -> GetDestination:
    return GetDestination(SqlAlchemyDestinationRepository(session))


async def get_list_bucket_list_items(
    session: AsyncSession = Depends(get_db_session),
) -> ListBucketListItems:
    return ListBucketListItems(SqlAlchemyBucketListItemRepository(session))


async def get_bucket_list_item_query(
    session: AsyncSession = Depends(get_db_session),
) -> GetBucketListItem:
    return GetBucketListItem(SqlAlchemyBucketListItemRepository(session))


async def get_list_visits(
    session: AsyncSession = Depends(get_db_session),
) -> ListVisits:
    return ListVisits(SqlAlchemyVisitRepository(session))


async def get_visit_query(
    session: AsyncSession = Depends(get_db_session),
) -> GetVisit:
    return GetVisit(SqlAlchemyVisitRepository(session))


# ── Command factories ──────────────────────────────────────────────────────────


async def get_create_destination(
    session: AsyncSession = Depends(get_db_session),
) -> CreateDestination:
    return CreateDestination(SqlAlchemyDestinationRepository(session))


async def get_update_destination(
    session: AsyncSession = Depends(get_db_session),
) -> UpdateDestination:
    return UpdateDestination(SqlAlchemyDestinationRepository(session))


async def get_delete_destination(
    session: AsyncSession = Depends(get_db_session),
) -> DeleteDestination:
    return DeleteDestination(SqlAlchemyDestinationRepository(session))


async def get_add_to_bucket_list(
    session: AsyncSession = Depends(get_db_session),
) -> AddToBucketList:
    return AddToBucketList(
        SqlAlchemyBucketListItemRepository(session),
        SqlAlchemyDestinationRepository(session),
        SqlAlchemyStatusRepository(session),
    )


async def get_update_bucket_list_item(
    session: AsyncSession = Depends(get_db_session),
) -> UpdateBucketListItem:
    return UpdateBucketListItem(
        SqlAlchemyBucketListItemRepository(session),
        SqlAlchemyStatusRepository(session),
    )


async def get_remove_from_bucket_list(
    session: AsyncSession = Depends(get_db_session),
) -> RemoveFromBucketList:
    return RemoveFromBucketList(SqlAlchemyBucketListItemRepository(session))


async def get_log_visit(
    session: AsyncSession = Depends(get_db_session),
) -> LogVisit:
    return LogVisit(
        SqlAlchemyVisitRepository(session),
        SqlAlchemyDestinationRepository(session),
    )


async def get_delete_visit(
    session: AsyncSession = Depends(get_db_session),
) -> DeleteVisit:
    return DeleteVisit(SqlAlchemyVisitRepository(session))
