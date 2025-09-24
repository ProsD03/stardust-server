from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    status: str = Field(default="error", description="Status of response, usually error for this type")
    error_code: str = Field(description="Significative, Unique Error code")
