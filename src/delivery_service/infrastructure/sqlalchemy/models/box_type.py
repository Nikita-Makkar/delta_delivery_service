from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from delivery_service.infrastructure.sqlalchemy.database import Base

if TYPE_CHECKING:
    from delivery_service.infrastructure.sqlalchemy.models.box import BoxModel


class BoxTypeModel(Base):
    """
    SQLAlchemy model for box_types table.
    """

    __tablename__ = "box_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)

    boxes: Mapped[list["BoxModel"]] = relationship(
        "BoxModel",
        back_populates="box_type",
        cascade="all, delete",
        passive_deletes=True
    )
