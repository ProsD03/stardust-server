import uuid
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class MessageObject(BaseModel):
    role: RoleEnum = Field(description="Role of entity that sent the message. Must be either user, assistant, or system")
    content: str = Field(description="Message content")

class CompletionsRequest(BaseModel):
    model: str = Field(description="Requested model to generate the completion")
    prompt: List[MessageObject] | str = Field(description="Prompt to start the generation, either a single message or an array of messages")
    max_tokens: int | None = Field(description="Maximum number of tokens to generate")
    temperature: float | None = Field(description="Temperature to use in the generation")
    stream: bool | None = Field(description="Whether the generation should be streamed")

class FinishReasonEnum(str, Enum):
    stop = "stop"
    length = "length"
    content_filter = "content_filter"

class ChoiceObject(BaseModel):
    text: str = Field(description="Generated text for this choice")
    index: int = Field(description="Index of the choice, usually 0", default=0)
    finish_reason: FinishReasonEnum | None = Field(description="Reason for completion finish. Must be either stop, length, or content_filter")

class UsageObject(BaseModel):
    prompt_tokens: int = Field(description="Number of tokens used by the prompt (system prompt and messages). Defaults to 0 if the provider does not give usage info", default=0)
    completion_tokens: int = Field(description="Number of tokens generated. Defaults to 0 if the provider does not give usage info", default=0)
    total_tokens: int = Field(description="Total number of tokens used by the completion. Defaults to 0 if the provider does not give usage info", default=0)

class CompletionsResponse(BaseModel):
    id: str = Field(description="ID of the completion request", default=f"cmpl-{uuid.uuid4()}")
    object: str = Field(description="Type of object, usually text_completion", default="text_completion")
    created: int = Field(description="Creation date as epoch timestamp", default=datetime.now().timestamp())
    model: str = Field(description="Name of model that generated the completion")
    choices: List[ChoiceObject] = Field(description="List of choice objects for this completion")
    usage: UsageObject = Field(description="Usage object for this completion", default=UsageObject())

class AsyncCompletionsResponse(BaseModel):
    id: str = Field(description="ID of the completion request", default=f"cmpl-{uuid.uuid4()}")
    object: str = Field(description="Type of object, usually text_completion", default="text_completion")
    created: int = Field(description="Creation date as epoch timestamp", default=datetime.now().timestamp())
    model: str = Field(description="Name of model that generated the completion")
    choices: List[ChoiceObject] = Field(description="List of choice objects for this completion")



