from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import get_db

from app.utils.security import get_current_agent
from app.db.schemas import AgentRegisterRequest, AgentRegisterResponse, AgentLastReadingResponse
from app.services.agents_service import get_agents_last_reading,ask_for_ping, create_agent_in_db, add_agent_readings

router = APIRouter()

@router.post("/agent/register", response_model=schemas.AgentRegisterResponse)
def create_agent(agent: schemas.AgentRegisterRequest, db: Session = Depends(get_db)):
    return create_agent_in_db(agent, db)

@router.post("/agent/readings")
def agent_readings(
    reading: schemas.ReadingCreateRequest,
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(get_current_agent)
):
    return add_agent_readings(reading, db, current_agent)

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
    return ask_for_ping(db, current_agent)

@router.get("/agent/last_reading")
def get_last_reading(
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(get_current_agent)
):
    return get_agents_last_reading(db, current_agent)