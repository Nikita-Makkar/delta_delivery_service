from fastapi import Request

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.infrastructure.sqlalchemy.unit_of_work import \
    SQLAlchemyUnitOfWork


def get_uow() -> IUnitOfWork:
    """
    Get a unit of work.
    """
    return SQLAlchemyUnitOfWork()


def get_logger_from_app(request: Request) -> ILogger:
    """
    Get app logger.
    """
    return request.app.state.logger
