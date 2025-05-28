from typing import Annotated, Optional

from pydantic import BaseModel, Field


class BoxResponse(BaseModel):
    """
    Response schema for box with delivery price.
    """

    id: Annotated[str, Field(description="Box ID")]
    name: Annotated[str, Field(description="Box name")]
    weight: Annotated[float, Field(description="Weight in kg")]
    box_type: Annotated[
        str,
        Field(description="Box type"),
    ]
    price_usd: Annotated[float, Field(description="Price box in USD")]
    delivery_price_rub: Annotated[
        Optional[float],
        Field(
            description="Delivery price in RUB, or null if not calculated yet"
        ),
    ]
