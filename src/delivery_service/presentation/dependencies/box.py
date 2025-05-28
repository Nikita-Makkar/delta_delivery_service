from typing import cast

from fastapi import Depends

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.application.repositories.box_type_repository import \
    IBoxTypeRepository
from delivery_service.application.use_cases.get_box import GetBoxUseCase
from delivery_service.application.use_cases.get_box_types import \
    GetBoxTypesUseCase
from delivery_service.application.use_cases.get_user_boxes import \
    GetUserBoxesUseCase
from delivery_service.infrastructure.rabbitmq.producer import BoxProducer
from delivery_service.infrastructure.sqlalchemy.repositories.box import \
    BoxRepository
from delivery_service.infrastructure.sqlalchemy.repositories.box_type import \
    BoxTypeRepository
from delivery_service.presentation.dependencies.base import (
    get_logger_from_app, get_uow)


def get_box_repo() -> type[IBoxRepository]:
    """
    Returns  Box repository class.
    """
    return cast(type[IBoxRepository], BoxRepository)


def get_box_types_repo() -> type[IBoxTypeRepository]:
    """
    Returns Box type repository class.
    """
    return cast(type[IBoxTypeRepository], BoxTypeRepository)


def get_box_producer(
    logger: ILogger = Depends(get_logger_from_app),
) -> BoxProducer:
    """
    Returns configured RabbitMQ producer.
    """
    return BoxProducer(logger)


def get_box_uc(
    uow: IUnitOfWork = Depends(get_uow),
    repository: type[IBoxRepository] = Depends(get_box_repo),
    logger: ILogger = Depends(get_logger_from_app),
) -> GetBoxUseCase:
    """
    Provides GetBoxUseCase with dependencies.
    """
    return GetBoxUseCase(uow, repository, logger)


def get_user_boxes_uc(
    uow: IUnitOfWork = Depends(get_uow),
    repository: type[IBoxRepository] = Depends(get_box_repo),
    logger: ILogger = Depends(get_logger_from_app),
) -> GetUserBoxesUseCase:
    """
    Provides GetUserBoxesUseCase with dependencies.
    """
    return GetUserBoxesUseCase(uow, repository, logger)


def get_box_types_uc(
    uow: IUnitOfWork = Depends(get_uow),
    repository: type[IBoxTypeRepository] = Depends(get_box_types_repo),
    logger: ILogger = Depends(get_logger_from_app),
) -> GetBoxTypesUseCase:
    """
    Provides GetBoxTypesUseCase with dependencies.
    """
    return GetBoxTypesUseCase(uow, repository, logger)
