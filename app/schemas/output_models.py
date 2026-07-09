from typing import Any, Literal
from pydantic import BaseModel, Field


class StepData(BaseModel):
    step: str = Field(..., description="Step name")
    kind: Literal["text", "url"] = Field(..., description="Type of output")
    title: str = Field(..., description="Display title")
    data: Any = Field(..., description="Main content")
    url: str | None = Field(None, description="Clickable URL")


class FinalResponse(BaseModel):
    outputs: list[StepData] = Field(default_factory=list)
    document_url: str | None = None
    human_input_url: str | None = None
    human_input_subject: str | None = None
    human_input_body: str | None = None
    mail_status: str | None = None
    mail_message: str | None = None