from src.api.v1.routes import auth_router
from fastapi import APIRouter


api_router = APIRouter()


api_router.include_router(auth_router)
