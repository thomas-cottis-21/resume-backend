from fastapi import APIRouter

from bucket_list.interfaces.routers.bucket_list import router as bucket_list_router
from bucket_list.interfaces.routers.destinations import router as destinations_router
from bucket_list.interfaces.routers.visits import router as visits_router

bucket_list_router_root = APIRouter()

bucket_list_router_root.include_router(destinations_router)
bucket_list_router_root.include_router(bucket_list_router)
bucket_list_router_root.include_router(visits_router)
