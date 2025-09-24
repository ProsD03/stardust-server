from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

class ModelObject(BaseModel):
    id: str = Field(description="Name of the LLM model")
    object: str = Field(description="Type of object, usually model", default="model")
    created: datetime = Field(description="Creation date")
    owned_by: str = Field(description="Owner of model, usually stardust", default="stardust")

class ModelsResponse(BaseModel):
    object: str = Field(description="Type of object, usually list", default="list")
    data: List[ModelObject] = Field(description="List of models")
