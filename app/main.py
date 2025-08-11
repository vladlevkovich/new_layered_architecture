from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app.src.api import (
    cart_router,
    menu_router,
    order_router,
    report_router,
    user_router,
)
from app.src.containers.container import Container
from app.src.core import scheduler
from app.src.middleware.auth import get_current_user
from app.src.utils import singleton
from app.src.utils.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_error_handler(
        request: Request, exc: UserAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"message": f"User with this email {exc.name} already exists"},
        )


def register_invalid_credentials_error(app: FastAPI) -> None:
    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_error_handler(
        request: Request, exc: InvalidCredentialsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"message": f"Invalid credentials for {exc.name}"},
        )


def register_user_not_found_error(app: FastAPI) -> None:
    @app.exception_handler(UserNotFoundError)
    async def user_not_found_error(
        request: Request, exc: UserNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"message": f"User '{exc.name}' not found"},
        )


@singleton
class CreateApp:
    def __init__(self) -> None:
        self.container = Container()
        self.container.container_config.db.url.from_env("DB_URL")
        # self.scheduler = AsyncIOScheduler()

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
            try:
                print("Starting scheduler")
                scheduler.start()
                yield
                print("Shutdown scheduler")
                scheduler.shutdown()
            except Exception as e:
                print(f"Scheduler failed: {str(e)}")

        self.app = FastAPI(
            title="Online Restaurant",
            description="Web application for online restaurant ordering",
            version="1.0.0",
            lifespan=lifespan,
        )
        self.db = self.container.db

        self.app.include_router(user_router)
        self.app.include_router(menu_router, dependencies=[Depends(get_current_user)])
        self.app.include_router(cart_router, dependencies=[Depends(get_current_user)])
        self.app.include_router(order_router, dependencies=[Depends(get_current_user)])
        self.app.include_router(report_router)

        # self.app.add_middleware(AuthMiddleware)
        register_exception_handlers(self.app)
        register_invalid_credentials_error(self.app)
        register_user_not_found_error(self.app)


application = CreateApp()
app = application.app
db = application.db
