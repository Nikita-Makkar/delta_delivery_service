from fastapi import FastAPI

from delivery_service.application.exceptions import ApplicationError
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.infrastructure.logger.factory import LoggerFactory
from delivery_service.presentation.exceptions import app_error_handler
from delivery_service.presentation.routes.boxes import router as box_router


def create_app() -> FastAPI:
    """
    Creates and configures FastAPI app with routes and exception handlers.
    """

    app = FastAPI()

    logger: ILogger = LoggerFactory().get_logger()
    app.state.logger = logger

    app.include_router(box_router)

    app.add_exception_handler(ApplicationError, app_error_handler)

    return app


app = create_app()
