from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/readings", response_model=schemas.ReadingResponse)
def create_reading(reading: schemas.ReadingCreateRequest, db: Session = Depends(get_db)):
    db_reading = models.Reading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.get("/readings/{reading_id}", response_model=schemas.ReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    db_reading = db.query(models.Reading).filter(models.Reading.id == reading_id).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return db_reading

@router.get("/agents/{agent_id}/readings", response_model=list[schemas.ReadingResponse])
def list_agents_readings(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()

    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    readings = db.query(models.Reading).filter(models.Reading.agent_id == agent_id).all()
    return readings

@router.get("/agents/{agent_id}/readings/latest", response_model=list[schemas.ReadingResponse])
def get_agents_latest_readings(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()

    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    latest_readings = db.query(models.Reading).filter(models.Reading.agent_id == agent_id).order_by(models.Reading.recieved_at.desc()).limit(10).all()
    return latest_readings
