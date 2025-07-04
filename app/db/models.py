from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base

class Agent(Base):
    """
    Represents a data-collecting agent (e.g., scraper or worker).
    Stores configuration and metadata about its activity.
    
    Fields:
    - id: Unique identifier for the agent (int)
    - name: Human-readable name for the agent (str)
    - description: Optional description of what the agent does (str, optional)
    - config: Optional configuration as JSON (dict or list)
    - created_at: Timestamp of agent registration (datetime)
    - last_active: Timestamp of last activity from the agent (datetime, optional)
    """
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    config = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, nullable=True)

    readings = relationship("Reading", back_populates="agent")

class Reading(Base):
    """
    Represents a single data reading submitted by an agent.
    
    Fields:
    - id: Unique identifier for the reading (int)
    - agent_id: Foreign key linking to the submitting agent (int)
    - timestamp: When the data was originally collected by the agent (datetime)
    - received_at: When the data was received by the API (datetime)
    - data: The actual data payload (any JSON-serializable structure: dict, list, number, etc.)
    """
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON, nullable=False)

    agent = relationship("Agent", back_populates="readings")
