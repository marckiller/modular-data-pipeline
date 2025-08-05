from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

#Agent registration

class AgentRegisterRequest(BaseModel):
    name: str
    description: Optional[str] = None
    config: Optional[dict] = None

class AgentRegisterResponse(BaseModel):
    id: int
    api_key: str
    name: str
    description: Optional[str] = None
    config: Optional[dict] = None
    created_at: datetime
    last_active: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

#Agent checks
class AgentInfoResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    config: Optional[dict] = None
    created_at: datetime
    last_active: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

#Reading creation and retrieval
class ReadingCreateRequest(BaseModel):
    data: dict
    timestamp: Optional[datetime] = None

class ReadingResponse(BaseModel):
    id: int
    agent_id: int
    received_at: datetime
    timestamp: datetime
    data: dict

    model_config = ConfigDict(from_attributes=True)

class AgentLastReadingResponse(BaseModel):
    id: int
    agent_id: int
    received_at: datetime
    timestamp: datetime
    data: dict

    model_config = ConfigDict(from_attributes=True)

class ListAgentsResponse(BaseModel):
    agents: List[AgentInfoResponse]

class AgentReadingsResponse(BaseModel):
    readings: List[ReadingResponse]



