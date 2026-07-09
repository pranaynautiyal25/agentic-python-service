from pydantic import BaseModel, Field


class InputOne(BaseModel):
    messy_note: str = Field(..., description="Messy meeting notes")
    what_to_do: str = Field(..., description="What the user wants done")


class UserRequest(BaseModel):
    input_one: InputOne


class HumanInputData(BaseModel):
    recipient_name: str = Field(..., description="Recipient name")
    recipient_email: str | None = Field(None, description="Recipient email")
    sender_name: str = Field(..., description="Sender name")
    subject: str = Field(..., description="Mail subject")
    key_points: str = Field(..., description="Key points for the email")
    tone: str = Field("professional", description="Email tone")


class HumanInputRequest(BaseModel):
    input_one: InputOne
    human_input: HumanInputData