from datetime import datetime
from pydantic import BaseModel, Field


class MessageOut(BaseModel):
    id: int
    conversation_id: str
    role: str
    content: str
    emotion: str | None = None
    expression: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationOut(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageOut] = []

    model_config = {"from_attributes": True}


class ConversationListItem(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationListOut(BaseModel):
    conversations: list[ConversationListItem]


class ConversationCreateOut(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SendMessageIn(BaseModel):
    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    message: MessageOut
    response: MessageOut


class DeleteOut(BaseModel):
    detail: str = "deleted"
