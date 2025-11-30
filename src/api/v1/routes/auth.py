from fastapi import APIRouter, Depends

from src.api.deps import get_db
from src.api.v1.schemas.user_schema import UserCreate, UserResponse
from src.api.v1.controllers.auth_controller import user_register_controller

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse)
async def register(payload: UserCreate, db=Depends(get_db)):
    try:
        return await user_register_controller(payload, db)
    except Exception as e:
        import traceback

        traceback.print_exc()
