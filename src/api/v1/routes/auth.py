from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.deps import get_db
from src.api.v1.schemas.user_schema import LoginSchema, UserCreate, UserResponse
from src.api.v1.controllers.auth_controller import (
    user_login_controller,
    user_register_controller,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse)
async def register(payload: UserCreate, db=Depends(get_db)):
    return await user_register_controller(payload, db)


@auth_router.post("/login")
async def login(payload: LoginSchema, response: Response, db=Depends(get_db)):
    try:
        #  get the access and refresh token
        access_token, refresh_token = await user_login_controller(payload, db)

        # set the http only cookie for refresh token
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,  # 7 days
            path="/auth/refresh-token",
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
