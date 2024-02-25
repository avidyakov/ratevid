from fastapi import APIRouter

from api.currency import router

api_router = APIRouter()
api_router.include_router(router)
