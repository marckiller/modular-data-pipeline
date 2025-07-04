from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import get_db

from app.utils.security import generate_api_key, get_current_agent
from app.db.schemas import AgentRegisterRequest, AgentRegisterResponse, AgentLastReadingResponse

router = APIRouter()

@router.post("/agent/register", response_model=schemas.AgentRegisterResponse)
def create_agent(agent: schemas.AgentRegisterRequest, db: Session = Depends(get_db)):
    api_key = generate_api_key()
    db_agent = models.Agent(api_key=api_key, **agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.post("/agent/readings")
def agent_readings(
    reading: schemas.ReadingCreateRequest,
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(get_current_agent)
):
    db_reading = models.Reading(agent_id=current_agent.id, data=reading.data)
    db.add(db_reading)
    db.commit()
    return {"status": "reading accepted"}

@router.get("/agent/info", response_model=schemas.AgentInfoResponse)
def get_agent_info(
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(get_current_agent)
):
    return current_agent

@router.get("/agent/ping")
def ping_agent(
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(get_current_agent)
):
    return {"status": "pong"}

@router.get("/agent/last_reading")
def get_last_reading(
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(get_current_agent)
):
    last_reading = db.query(models.Reading).filter(models.Reading.agent_id == current_agent.id).order_by(models.Reading.received_at.desc()).first()
    if not last_reading:
        raise HTTPException(status_code=404, detail="No readings found for this agent")
    return schemas.AgentLastReadingResponse.from_orm(last_reading)