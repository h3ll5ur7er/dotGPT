from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class Message(BaseModel):
    """Represents a single message in a chat conversation."""
    sender: str
    message: str
    timestamp: datetime
    
class ChatSettings(BaseModel):
    """Represents the settings for a chat."""
    name: str = Field(default="New Chat")
    id: UUID = Field(default_factory=uuid4)


    def __eq__(self, other):
        return self.name == other.name


class Chat(BaseModel):
    """Represents a chat conversation with a list of messages."""
    settings: ChatSettings
    messages: List[Message] = Field(default_factory=list)
    

class ChatStore(BaseModel):
    """Represents the store of all chat conversations."""
    chats: List[Chat] = Field(default_factory=list)
    active_chat: Optional[str] = None
