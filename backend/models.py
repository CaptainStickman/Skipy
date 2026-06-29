from pydantic import BaseModel
from typing import List, Literal


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    """What the frontend sends us: the full conversation so far."""
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    """Non-streaming response shape (used if streaming is off)."""
    reply: str
