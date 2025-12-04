from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_db
from src.api.v1.controllers.auth_controller import (
    refresh_access_token_controller,
    user_login_controller,
    user_register_controller,
)
from src.api.v1.schemas.user_schema import LoginSchema, UserCreate, UserResponse

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
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,  # 7 days
            path="/auth/refresh-token",
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/refresh-token")
async def refresh_token_endpoint(
    response: Response, request: Request, db: AsyncSession = Depends(get_db)
):
    try:
        #    get the refresh token from the request
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh Token Not Found",
            )

        # again get the refresh token and the access token

        access_token, refresh_token = await refresh_access_token_controller(
            db=db, refresh_token=refresh_token
        )

        # set the response
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth/refresh-token",
            max_age=7 * 24 * 60 * 60,
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
