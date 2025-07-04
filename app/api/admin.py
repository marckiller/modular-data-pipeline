from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import models, schemas
from app.db.database import get_db
from app.utils.security import verify_admin_token

from app.services.admin_service import list_readings_for_agent, get_reading_by_id, get_latest_reading_for_agent, list_all_agents, get_agent_by_id, list_readings_for_agent

router = APIRouter()

@router.get("/admin/agents", response_model=list[schemas.AgentInfoResponse], dependencies=[Depends(verify_admin_token)])
def list_agents(db: Session = Depends(get_db)):
    return list_all_agents(db)

@router.get("/admin/agents/{agent_id}", response_model=schemas.AgentInfoResponse, dependencies=[Depends(verify_admin_token)])
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    return get_agent_by_id(agent_id, db)

from app.services.admin_service import list_readings_for_agent

@router.get("/admin/agents/{agent_id}/readings", response_model=list[schemas.ReadingResponse], dependencies=[Depends(verify_admin_token)])
def list_agent_readings(
    agent_id: int,
    db: Session = Depends(get_db),
    limit: int | None = Query(None, gt=0),
    from_date: datetime | None = None,
    to_date: datetime | None = None):
    return list_readings_for_agent(agent_id, db, limit, from_date, to_date)

@router.get("/admin/agents/{agent_id}/readings/latest", response_model=schemas.ReadingResponse, dependencies=[Depends(verify_admin_token)])
def get_agent_latest_reading(agent_id: int, db: Session = Depends(get_db)):
    return get_latest_reading_for_agent(agent_id, db)

@router.get("/admin/readings/{reading_id}", response_model=schemas.ReadingResponse, dependencies=[Depends(verify_admin_token)])
def read_reading_by_id(reading_id: int, db: Session = Depends(get_db)):
    return get_reading_by_id(reading_id, db)