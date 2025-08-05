from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException
from datetime import datetime
from app.utils.security import generate_api_key

from app.db import schemas 

def create_agent_in_db(agent: schemas.AgentRegisterRequest, db: Session) -> models.Agent:
    api_key = generate_api_key()
    db_agent = models.Agent(api_key=api_key, **agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def add_agent_readings(
    reading: schemas.ReadingCreateRequest,
    db: Session,
    current_agent: models.Agent
) -> dict:
    """
    Persist a new reading for the given agent.  If the agent provided a
    timestamp, use it; otherwise fall back to the current UTC time.  Also
    update the agent's ``last_active`` field to reflect that it just sent
    data.
    """
    ts = reading.timestamp or datetime.utcnow()
    db_reading = models.Reading(
        agent_id=current_agent.id,
        data=reading.data,
        timestamp=ts
    )
    db.add(db_reading)
    # bump last_active to now
    current_agent.last_active = datetime.utcnow()
    db.commit()
    return {"status": "reading accepted"}

def ask_for_ping(
    db: Session,
    current_agent: models.Agent
) -> dict:
    current_agent.last_active = datetime.utcnow()
    db.commit()
    return {"status": "pong"}

def get_agents_last_reading(
    db: Session,
    current_agent: models.Agent
) -> schemas.AgentLastReadingResponse | None:
    last_reading = db.query(models.Reading).filter(models.Reading.agent_id == current_agent.id).order_by(models.Reading.received_at.desc()).first()
    if not last_reading:
        raise HTTPException(status_code=404, detail="No readings found for this agent")
    return schemas.AgentLastReadingResponse.from_orm(last_reading)