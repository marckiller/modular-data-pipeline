from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import models, schemas
from app.db.database import get_db
from app.utils.security import verify_admin_token

router = APIRouter()

@router.get("/admin/agents", response_model=list[schemas.AgentInfoResponse], dependencies=[Depends(verify_admin_token)])
def list_agents(db: Session = Depends(get_db)):
    return db.query(models.Agent).all()

@router.get("/admin/agents/{agent_id}", response_model=schemas.AgentInfoResponse, dependencies=[Depends(verify_admin_token)])
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.get("/admin/agents/{agent_id}/readings", response_model=list[schemas.ReadingResponse], dependencies=[Depends(verify_admin_token)])
def list_agent_readings(
    agent_id: int,
    db: Session = Depends(get_db),
    limit: int | None = Query(None, gt=0),
    from_date: datetime | None = None,
    to_date: datetime | None = None
):
    query = db.query(models.Reading).filter(models.Reading.agent_id == agent_id)
    
    if from_date:
        query = query.filter(models.Reading.received_at >= from_date)
    if to_date:
        query = query.filter(models.Reading.received_at <= to_date)

    query = query.order_by(models.Reading.received_at.desc())

    if limit:
        query = query.limit(limit)

    return query.all()

@router.get("/admin/agents/{agent_id}/readings/latest", response_model=schemas.ReadingResponse, dependencies=[Depends(verify_admin_token)])
def get_agent_latest_reading(agent_id: int, db: Session = Depends(get_db)):
    reading = db.query(models.Reading).filter(models.Reading.agent_id == agent_id).order_by(models.Reading.received_at.desc()).first()
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found for agent")
    return reading

@router.get("/admin/readings/{reading_id}", response_model=schemas.ReadingResponse, dependencies=[Depends(verify_admin_token)])
def get_reading_by_id(reading_id: int, db: Session = Depends(get_db)):
    reading = db.query(models.Reading).filter(models.Reading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading