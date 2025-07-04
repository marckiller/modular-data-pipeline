from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AgentCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    config: Optional[dict] = None

class AgentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    config: Optional[dict] = None
    created_at: datetime
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReadingCreateRequest(BaseModel):
    agent_id: int
    data: dict

class ReadingResponse(BaseModel):
    id: int
    agent_id: int
    received_at: datetime
    data: dict

    class Config:
        from_attributes = True
