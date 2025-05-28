from typing import Annotated

from pydantic import BaseModel, Field


class BoxTypeResponse(BaseModel):
    """
    Response schema for box type.
    """

    id: Annotated[int, Field(description="Box type ID")]
    name: Annotated[str, Field(description="Box type name")]

    model_config = {"from_attributes": True}
