from typing import Annotated

from pydantic import BaseModel, Field


class RegisterBox(BaseModel):
    """
    Schemas for box registration.
    """

    name: Annotated[
        str, Field(min_length=1, max_length=255, description="Box name")
    ]
    weight: Annotated[float, Field(gt=0, description="Wight  box in kg")]
    box_type_id: Annotated[int, Field(gt=0, description="Box type ID")]
    price_usd: Annotated[float, Field(gt=0, description="Price box in USD")]


class RegisterBoxResponse(BaseModel):
    """
    Schemas box ID after successful registration.
    """

    box_id: str
