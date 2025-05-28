import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from delivery_service.infrastructure.sqlalchemy.database import Base

if TYPE_CHECKING:
    from delivery_service.infrastructure.sqlalchemy.models.box_type import \
        BoxTypeModel


class BoxModel(Base):
    """
    SQLAlchemy model for boxes table.
    """

    __tablename__ = "boxes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)

    user_id: Mapped[str] = mapped_column(
        String(36), nullable=False, index=True
    )

    box_type_id: Mapped[int] = mapped_column(
        ForeignKey("box_types.id"), nullable=False
    )
    box_type: Mapped["BoxTypeModel"] = relationship(
        back_populates="boxes"
    )

    weight: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    price_currency: Mapped[str] = mapped_column(
        String(length=3), nullable=False
    )

    delivery_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    delivery_currency: Mapped[str | None] = mapped_column(
        String(length=3), nullable=True
    )

