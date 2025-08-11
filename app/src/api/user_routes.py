from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.src.containers.container import Container
from app.src.core.config import config
from app.src.core.jwt_auth import auth
from app.src.schemas.auth_schema import (
    LoginSchema,
    RefreshTokenSchema,
    RegisterSchema,
    TokenResponseSchema,
)
from app.src.schemas.user_schema import UserLoginResponse, UserRegisterResponse
from app.src.services.user_service import UserService

router = APIRouter(prefix="/users")


@router.post("/register", response_model=UserRegisterResponse)
@inject
async def user_register(
    user_data: RegisterSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserRegisterResponse:
    """Register new user"""
    try:
        print("secret key", config.SECRET_KEY)
        new_user = await user_service.register_user(user_data)
        return UserRegisterResponse(user=new_user)
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post("/login", response_model=UserLoginResponse)
@inject
async def user_login(
    login_data: LoginSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserLoginResponse:
    """Login user"""
    try:
        user = await user_service.login_user(login_data)
        # print('User', user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post("/refresh-token", response_model=TokenResponseSchema)
async def refresh_access_token(
    token_data: RefreshTokenSchema,
) -> TokenResponseSchema:
    """Оновлює access token за допомогою refresh token"""
    try:
        new_access_token = auth.refresh_access_token(token_data.refresh_token)
        return TokenResponseSchema(access_token=new_access_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
